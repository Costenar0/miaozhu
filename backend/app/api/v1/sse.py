"""
SSE（Server-Sent Events）端点：替代前端轮询，实时推送生成进度和导出任务状态。
"""

import asyncio
import json
import logging
from typing import Optional

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import async_session
from app.models.application import Application
from app.models.generation import GenerationTask
from app.models.export_task import ExportTask
from app.schemas.generation import TaskResponse, TaskProgressResponse
from app.schemas.export_task import ExportTaskResponse
from app.api.v1.exports import _validate_and_fix_task_consistency

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sse", tags=["SSE"])

SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",
    "Connection": "keep-alive",
}


def _serialize_task(task) -> str:
    """序列化任务进度（轻量级，不包含章节完整内容）"""
    return TaskProgressResponse.model_validate(task).model_dump_json()


def _serialize_exports(items, total: int) -> str:
    return json.dumps({
        "items": [ExportTaskResponse.model_validate(i).model_dump(mode="json") for i in items],
        "total": total,
    }, ensure_ascii=False)


@router.get("/generation/{app_id}")
async def generation_stream(
    app_id: int,
):
    """SSE 推送生成任务进度，状态变化时才发送，完成后关闭连接。"""

    async def event_generator():
        last_json = ""
        try:
            while True:
                async with async_session() as db:
                    # 验证申请存在
                    result = await db.execute(
                        select(Application).where(Application.id == app_id)
                    )
                    if not result.scalar_one_or_none():
                        yield f"data: {json.dumps({'error': '申请不存在'})}\n\n"
                        return

                    result = await db.execute(
                        select(GenerationTask)
                        .where(GenerationTask.application_id == app_id)
                        .options(selectinload(GenerationTask.sections))
                        .order_by(GenerationTask.created_at.desc())
                        .limit(1)
                    )
                    task = result.scalar_one_or_none()

                if not task:
                    yield f"data: {json.dumps({'error': '尚未生成'})}\n\n"
                    return

                current_json = _serialize_task(task)
                if current_json != last_json:
                    yield f"data: {current_json}\n\n"
                    last_json = current_json

                # 检查是否全部完成
                is_running = (
                    task.status in ("pending", "running")
                    or any(s.status in ("pending", "running") for s in task.sections)
                )
                if not is_running:
                    return

                await asyncio.sleep(2)

        except asyncio.CancelledError:
            logger.debug("SSE generation stream closed by client (app_id=%d)", app_id)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )


@router.get("/export-tasks")
async def export_tasks_stream(
    app_id: Optional[int] = Query(None),
    page: int = Query(1),
    page_size: int = Query(20),
):
    """SSE 推送导出任务状态。app_id 有值时只推该申请的任务，否则推全部任务。"""
    page_size = min(page_size, 100)

    async def event_generator():
        last_json = ""
        try:
            while True:
                async with async_session() as db:
                    if app_id:
                        # 特定申请的最新导出（用于 CopyrightGenerateView）
                        result = await db.execute(
                            select(ExportTask)
                            .where(ExportTask.application_id == app_id)
                            .order_by(desc(ExportTask.created_at))
                            .limit(20)
                        )
                        items = list(result.scalars().all())
                        total = len(items)
                    else:
                        # 全部导出（用于 DownloadRecordsView，分页）
                        from sqlalchemy import func
                        offset = (page - 1) * page_size

                        total_result = await db.execute(
                            select(func.count(ExportTask.id))
                        )
                        total = total_result.scalar()

                        result = await db.execute(
                            select(ExportTask)
                            .order_by(desc(ExportTask.created_at))
                            .offset(offset)
                            .limit(page_size)
                        )
                        items = list(result.scalars().all())

                    # 数据一致性检查和修复
                    await _validate_and_fix_task_consistency(items, db)

                current_json = _serialize_exports(items, total)
                if current_json != last_json:
                    yield f"data: {current_json}\n\n"
                    last_json = current_json

                # 无 pending/processing 任务时关闭连接
                has_active = any(i.status in ("pending", "processing") for i in items)
                if not has_active:
                    return

                await asyncio.sleep(3)

        except asyncio.CancelledError:
            logger.debug("SSE export-tasks stream closed by client")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )
