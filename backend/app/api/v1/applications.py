from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.dependencies import get_db
from app.models.application import Application
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationStatus,
    StatusTransitionRequest,
    ALLOWED_STATUS_TRANSITIONS,
)

router = APIRouter(prefix="/applications", tags=["软著申请"])


@router.get("")
async def list_applications(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    page_size = min(page_size, 100)
    offset = (page - 1) * page_size

    total_result = await db.execute(
        select(func.count(Application.id))
    )
    total = total_result.scalar()

    result = await db.execute(
        select(Application)
        .order_by(Application.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    items = result.scalars().all()
    return {"items": [ApplicationResponse.model_validate(i) for i in items], "total": total}


@router.post("", response_model=ApplicationResponse, status_code=201)
async def create_application(
    data: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
):
    # Rate limit: max 100 applications per day
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    result = await db.execute(
        select(func.count(Application.id)).where(
            Application.created_at >= today_start,
        )
    )
    if result.scalar() >= 100:
        raise HTTPException(status_code=429, detail="今日创建申请数已达上限（100 个/天）")

    app = Application(
        status="draft",
        **data.model_dump(exclude_none=True),
    )
    db.add(app)
    await db.commit()
    await db.refresh(app)
    return app


@router.get("/{app_id}", response_model=ApplicationResponse)
async def get_application(
    app_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application).where(Application.id == app_id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="申请不存在")
    return app


@router.put("/{app_id}", response_model=ApplicationResponse)
async def update_application(
    app_id: int,
    data: ApplicationUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application).where(Application.id == app_id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="申请不存在")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(app, key, value)
    await db.commit()
    await db.refresh(app)
    return app


@router.delete("/{app_id}")
async def delete_application(
    app_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application).where(Application.id == app_id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="申请不存在")
    await db.delete(app)
    await db.commit()
    return {"message": "已删除"}


@router.post("/{app_id}/status", response_model=ApplicationResponse)
async def transition_application_status(
    app_id: int,
    request: StatusTransitionRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    状态转换 API

    允许的状态转换：
    - draft → generating（开始生成）/ archived（放弃）
    - generating → generated（生成完成）/ draft（生成失败）
    - generated → ready（审核通过）/ generating（重新生成）/ draft（返回编辑）
    - ready → submitted（提交申请）/ generated（返回审核）
    - submitted → approved（审批通过）/ rejected（审批驳回）
    - rejected → draft（重新修改）/ archived（放弃）
    - approved → archived（归档）
    - archived → 终态，不可转换
    """
    # 查询申请
    result = await db.execute(
        select(Application).where(Application.id == app_id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="申请不存在")

    # 解析当前状态
    try:
        current_status = ApplicationStatus(app.status)
    except ValueError:
        # 兼容旧数据，默认为 draft
        current_status = ApplicationStatus.DRAFT
        app.status = current_status.value

    # 检查目标状态是否允许
    if current_status not in ALLOWED_STATUS_TRANSITIONS:
        raise HTTPException(
            status_code=400,
            detail=f"当前状态 {current_status.value} 不支持状态转换"
        )

    allowed_targets = ALLOWED_STATUS_TRANSITIONS[current_status]
    if request.target_status not in allowed_targets:
        allowed_list = ", ".join([s.value for s in allowed_targets])
        raise HTTPException(
            status_code=400,
            detail=f"不允许从 {current_status.value} 转换到 {request.target_status.value}。"
                   f"允许的目标状态：{allowed_list}"
        )

    # 执行状态转换
    app.status = request.target_status.value
    await db.commit()
    await db.refresh(app)

    return app


@router.get("/status/flow")
async def get_status_flow():
    """
    获取状态流转图

    返回所有可能的状态转换，用于前端展示状态流程图
    """
    flow = {}
    for status, targets in ALLOWED_STATUS_TRANSITIONS.items():
        flow[status.value] = {
            "label": _get_status_label(status),
            "targets": [
                {"value": t.value, "label": _get_status_label(t)}
                for t in targets
            ]
        }
    return flow


def _get_status_label(status: ApplicationStatus) -> str:
    """获取状态的中文标签"""
    labels = {
        ApplicationStatus.DRAFT: "草稿",
        ApplicationStatus.GENERATING: "生成中",
        ApplicationStatus.GENERATED: "已生成",
        ApplicationStatus.READY: "准备提交",
        ApplicationStatus.SUBMITTED: "已提交",
        ApplicationStatus.APPROVED: "已通过",
        ApplicationStatus.REJECTED: "已驳回",
        ApplicationStatus.ARCHIVED: "已归档",
    }
    return labels.get(status, status.value)
