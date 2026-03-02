from pydantic import BaseModel
from datetime import datetime


class DashboardStats(BaseModel):
    total_applications: int
    draft_count: int
    completed_count: int


class RecentApplication(BaseModel):
    id: int
    software_name: str | None
    status: str
    created_at: datetime
