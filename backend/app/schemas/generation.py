from pydantic import BaseModel
from datetime import datetime


class GenerateRequest(BaseModel):
    extra_prompt: str | None = None


class TaskUpdateRequest(BaseModel):
    extra_prompt: str | None = None


class RegenerateRequest(BaseModel):
    extra_prompt: str | None = None


class SectionUpdate(BaseModel):
    content: str


class SectionResponse(BaseModel):
    id: int
    task_id: int
    section_key: str
    title: str
    content: str | None = None
    section_order: int
    status: str
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SectionProgressResponse(BaseModel):
    """轻量级章节进度响应（用于SSE推送，不包含完整内容）"""
    id: int
    section_key: str
    title: str
    section_order: int
    status: str

    model_config = {"from_attributes": True}


class TaskResponse(BaseModel):
    id: int
    application_id: int
    status: str
    extra_prompt: str | None = None
    generate_source_code: bool = True
    generate_db_design: bool = True
    generate_diagrams: bool = False
    total_sections: int
    completed_sections: int
    created_at: datetime
    updated_at: datetime
    sections: list[SectionResponse] = []

    model_config = {"from_attributes": True}


class TaskProgressResponse(BaseModel):
    """轻量级任务进度响应（用于SSE推送）"""
    id: int
    application_id: int
    status: str
    total_sections: int
    completed_sections: int
    updated_at: datetime
    sections: list[SectionProgressResponse] = []

    model_config = {"from_attributes": True}
