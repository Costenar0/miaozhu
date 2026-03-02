from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.dependencies import get_db
from app.models.application import Application
from app.schemas.dashboard import DashboardStats, RecentApplication

router = APIRouter(prefix="/dashboard", tags=["仪表盘"])


@router.get("/stats", response_model=DashboardStats)
async def get_stats(
    db: AsyncSession = Depends(get_db),
):
    base = select(func.count()).select_from(Application)

    total = (await db.execute(base)).scalar() or 0
    draft = (await db.execute(base.where(Application.status == "draft"))).scalar() or 0
    completed = (await db.execute(base.where(Application.status == "completed"))).scalar() or 0

    return DashboardStats(
        total_applications=total,
        draft_count=draft,
        completed_count=completed,
    )


@router.get("/recent", response_model=list[RecentApplication])
async def get_recent(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application)
        .order_by(Application.created_at.desc())
        .limit(5)
    )
    apps = result.scalars().all()
    return [
        RecentApplication(
            id=a.id,
            software_name=a.software_name,
            status=a.status,
            created_at=a.created_at,
        )
        for a in apps
    ]
