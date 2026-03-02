import asyncio
import logging
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_db
from app.models.application import Application
from app.models.generation import GenerationTask, GenerationSection
from app.schemas.generation import (
    GenerateRequest,
    TaskUpdateRequest,
    RegenerateRequest,
    SectionUpdate,
    TaskResponse,
    SectionResponse,
)
from app.services.generation.sections import (
    MANUAL_SECTIONS, SOURCE_CODE_SECTIONS, DB_DESIGN_SECTIONS, META_SECTIONS,
)
from app.services.moderation import check_extra_prompt

logger = logging.getLogger(__name__)

router = APIRouter(tags=["AI 生成"])


def _build_section_list(
    generate_source_code: bool,
    generate_db_design: bool,
    generate_diagrams: bool = False,
):
    """根据选项构建要生成的 section 列表"""
    sections = list(MANUAL_SECTIONS)
    if generate_db_design:
        sections += DB_DESIGN_SECTIONS
    sections += SOURCE_CODE_SECTIONS
    sections += META_SECTIONS
    # 图表现已内嵌到手册章节正文中（通过 prompt 指令），无需独立 section
    return sections


@router.post(
    "/applications/{app_id}/generate",
    response_model=TaskResponse,
    status_code=201,
)
async def start_generation(
    app_id: int,
    data: GenerateRequest,
    db: AsyncSession = Depends(get_db),
):
    """提交生成任务，后台定时调度器会自动执行"""
    result = await db.execute(
        select(Application).where(Application.id == app_id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="申请不存在")

    # 审查额外指令
    if data.extra_prompt:
        passed, reason = await check_extra_prompt(data.extra_prompt)
        if not passed:
            raise HTTPException(
                status_code=400,
                detail=f"额外指令内容不符合要求：{reason or '请输入与软著申请材料相关的指令'}",
            )

    sec_defs = _build_section_list(
        app.generate_source_code, app.generate_db_design, app.generate_diagrams
    )

    task = GenerationTask(
        application_id=app_id,
        status="pending",
        extra_prompt=data.extra_prompt,
        generate_source_code=app.generate_source_code,
        generate_db_design=app.generate_db_design,
        generate_diagrams=app.generate_diagrams,
        total_sections=len(sec_defs),
        completed_sections=0,
    )
    db.add(task)
    await db.flush()

    # 更新 Application 状态为 generating
    app.status = "generating"

    for sec_def in sec_defs:
        db.add(GenerationSection(
            task_id=task.id,
            section_key=sec_def.key,
            title=sec_def.title,
            section_order=sec_def.order,
            status="pending",
        ))

    await db.commit()

    result = await db.execute(
        select(GenerationTask)
        .where(GenerationTask.id == task.id)
        .options(selectinload(GenerationTask.sections))
    )
    return result.scalar_one()


@router.get(
    "/applications/{app_id}/generation",
    response_model=TaskResponse,
)
async def get_generation(
    app_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取最新生成任务状态"""
    result = await db.execute(
        select(Application).where(Application.id == app_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="申请不存在")

    result = await db.execute(
        select(GenerationTask)
        .where(GenerationTask.application_id == app_id)
        .options(selectinload(GenerationTask.sections))
        .order_by(GenerationTask.created_at.desc())
        .limit(1)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="尚未生成")
    return task


@router.put(
    "/applications/{app_id}/generation",
    response_model=TaskResponse,
)
async def update_task(
    app_id: int,
    data: TaskUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    """编辑任务元数据（仅在非运行状态可编辑）"""
    result = await db.execute(
        select(GenerationTask)
        .where(GenerationTask.application_id == app_id)
        .options(selectinload(GenerationTask.sections))
        .order_by(GenerationTask.created_at.desc())
        .limit(1)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="尚未生成")
    if task.status in ("pending", "running"):
        raise HTTPException(status_code=400, detail="任务进行中，无法编辑")

    if data.extra_prompt is not None:
        passed, reason = await check_extra_prompt(data.extra_prompt)
        if not passed:
            raise HTTPException(
                status_code=400,
                detail=f"额外指令内容不符合要求：{reason or '请输入与软著申请材料相关的指令'}",
            )
        task.extra_prompt = data.extra_prompt

    await db.commit()

    result = await db.execute(
        select(GenerationTask)
        .where(GenerationTask.id == task.id)
        .options(selectinload(GenerationTask.sections))
    )
    return result.scalar_one()


@router.put(
    "/generation-sections/{section_id}",
    response_model=SectionResponse,
)
async def update_section(
    section_id: int,
    data: SectionUpdate,
    db: AsyncSession = Depends(get_db),
):
    """手动编辑章节内容"""
    section = await _get_section(db, section_id)
    section.content = data.content
    await db.commit()
    await db.refresh(section)
    return section


@router.post(
    "/generation-sections/{section_id}/regenerate",
    response_model=SectionResponse,
)
async def regenerate_section(
    section_id: int,
    data: RegenerateRequest,
    db: AsyncSession = Depends(get_db),
):
    """提交单章节重新生成，后台定时调度器会自动执行"""
    section = await _get_section(db, section_id)

    # 审查额外指令
    if data.extra_prompt:
        passed, reason = await check_extra_prompt(data.extra_prompt)
        if not passed:
            raise HTTPException(
                status_code=400,
                detail=f"额外指令内容不符合要求：{reason or '请输入与软著申请材料相关的指令'}",
            )

    section.status = "pending"
    section.extra_prompt = data.extra_prompt
    section.error_message = None
    await db.commit()
    await db.refresh(section)
    return section




_WORD_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


@router.get("/applications/{app_id}/export/manual/word")
async def export_manual_word(
    app_id: int,
    db: AsyncSession = Depends(get_db),
):
    """导出「文档鉴别材料」Word"""
    from app.services.document_export import export_manual_to_word

    app, sections = await _get_export_data(db, app_id)
    buf = await asyncio.to_thread(export_manual_to_word, app, sections)

    filename = f"{app.software_name or 'export'}_文档鉴别材料.docx"
    return StreamingResponse(
        buf, media_type=_WORD_MEDIA_TYPE,
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"},
    )


@router.get("/applications/{app_id}/export/source-code/word")
async def export_source_code_word(
    app_id: int,
    db: AsyncSession = Depends(get_db),
):
    """导出「源程序鉴别材料」Word"""
    from app.services.document_export import export_source_code_to_word

    app, sections = await _get_export_data(db, app_id)
    buf = await asyncio.to_thread(export_source_code_to_word, app, sections)

    filename = f"{app.software_name or 'export'}_源程序鉴别材料.docx"
    return StreamingResponse(
        buf, media_type=_WORD_MEDIA_TYPE,
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"},
    )


@router.get("/applications/{app_id}/export/manual/pdf")
async def export_manual_pdf(
    app_id: int,
    db: AsyncSession = Depends(get_db),
):
    """导出「文档鉴别材料」PDF"""
    from app.services.document_export import export_manual_to_pdf

    app, sections = await _get_export_data(db, app_id)
    buf = await asyncio.to_thread(export_manual_to_pdf, app, sections)

    filename = f"{app.software_name or 'export'}_文档鉴别材料.pdf"
    return StreamingResponse(
        buf, media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"},
    )


@router.get("/applications/{app_id}/export/source-code/pdf")
async def export_source_code_pdf(
    app_id: int,
    db: AsyncSession = Depends(get_db),
):
    """导出「源程序鉴别材料」PDF"""
    from app.services.document_export import export_source_code_to_pdf

    app, sections = await _get_export_data(db, app_id)
    buf = await asyncio.to_thread(export_source_code_to_pdf, app, sections)

    filename = f"{app.software_name or 'export'}_源程序鉴别材料.pdf"
    return StreamingResponse(
        buf, media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"},
    )


@router.get("/applications/{app_id}/export/word")
async def export_word(
    app_id: int,
    db: AsyncSession = Depends(get_db),
):
    """导出合并 Word 文档（向后兼容）"""
    from app.services.document_export import export_to_word

    app, sections = await _get_export_data(db, app_id)
    buf = await asyncio.to_thread(export_to_word, app, sections)

    filename = f"{app.software_name or 'export'}_软著材料.docx"
    return StreamingResponse(
        buf, media_type=_WORD_MEDIA_TYPE,
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"},
    )


@router.get("/applications/{app_id}/export/pdf")
async def export_pdf(
    app_id: int,
    db: AsyncSession = Depends(get_db),
):
    """导出合并 PDF 文档（向后兼容）"""
    from app.services.document_export import export_to_pdf

    app, sections = await _get_export_data(db, app_id)
    buf = await asyncio.to_thread(export_to_pdf, app, sections)

    filename = f"{app.software_name or 'export'}_软著材料.pdf"
    return StreamingResponse(
        buf, media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"},
    )


async def _get_section(
    db: AsyncSession, section_id: int
) -> GenerationSection:
    result = await db.execute(
        select(GenerationSection).where(GenerationSection.id == section_id)
    )
    section = result.scalar_one_or_none()
    if not section:
        raise HTTPException(status_code=404, detail="章节不存在")
    return section


async def _get_export_data(
    db: AsyncSession, app_id: int
) -> tuple[Application, list[GenerationSection]]:
    result = await db.execute(
        select(Application).where(Application.id == app_id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="申请不存在")

    result = await db.execute(
        select(GenerationTask)
        .where(GenerationTask.application_id == app_id)
        .order_by(GenerationTask.created_at.desc())
        .limit(1)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="尚未生成")

    result = await db.execute(
        select(GenerationSection)
        .where(
            GenerationSection.task_id == task.id,
            GenerationSection.status == "completed",
        )
        .order_by(GenerationSection.section_order)
    )
    sections = list(result.scalars().all())
    if not sections:
        raise HTTPException(status_code=400, detail="没有已完成的章节可供导出")
    return app, sections
