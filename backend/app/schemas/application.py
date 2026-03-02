from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    """软著申请状态枚举"""
    DRAFT = "draft"  # 草稿 - 用户填写基本信息
    GENERATING = "generating"  # 生成中 - AI 正在生成材料
    GENERATED = "generated"  # 已生成 - 材料已生成，待审核
    READY = "ready"  # 准备提交 - 用户审核通过，准备申请
    SUBMITTED = "submitted"  # 已提交 - 已向版权局提交
    APPROVED = "approved"  # 已通过 - 版权局审批通过
    REJECTED = "rejected"  # 已驳回 - 版权局驳回
    ARCHIVED = "archived"  # 已归档


# 允许的状态转换（有向图）
ALLOWED_STATUS_TRANSITIONS = {
    ApplicationStatus.DRAFT: [
        ApplicationStatus.GENERATING,  # 开始生成
        ApplicationStatus.ARCHIVED,  # 放弃申请
    ],
    ApplicationStatus.GENERATING: [
        ApplicationStatus.GENERATED,  # 生成完成
        ApplicationStatus.DRAFT,  # 生成失败，回到草稿
    ],
    ApplicationStatus.GENERATED: [
        ApplicationStatus.READY,  # 审核通过
        ApplicationStatus.GENERATING,  # 重新生成
        ApplicationStatus.DRAFT,  # 返回编辑
    ],
    ApplicationStatus.READY: [
        ApplicationStatus.SUBMITTED,  # 提交申请
        ApplicationStatus.GENERATED,  # 返回审核
    ],
    ApplicationStatus.SUBMITTED: [
        ApplicationStatus.APPROVED,  # 审批通过
        ApplicationStatus.REJECTED,  # 审批驳回
    ],
    ApplicationStatus.REJECTED: [
        ApplicationStatus.DRAFT,  # 重新修改
        ApplicationStatus.ARCHIVED,  # 放弃
    ],
    ApplicationStatus.APPROVED: [
        ApplicationStatus.ARCHIVED,  # 归档
    ],
    ApplicationStatus.ARCHIVED: [],  # 终态，不可转换
}


class ApplicationCreate(BaseModel):
    # Required
    software_name: str
    software_short_name: str
    main_features: str
    # Basic optional
    software_version: str | None = None
    software_category: str | None = None
    runtime_platform: str | None = None
    completion_date: str | None = None
    software_description: str | None = None
    # Development info
    development_language: str | None = None
    code_line_count: str | None = None
    development_method: str | None = None
    dev_hardware: str | None = None
    dev_os: str | None = None
    dev_tools: str | None = None
    # Runtime environment
    runtime_hardware: str | None = None
    runtime_software: str | None = None
    # Technical features
    technical_features: str | None = None
    module_design: str | None = None
    development_purpose: str | None = None
    target_industry: str | None = None
    # Rights info
    work_type: str | None = None
    rights_acquisition: str | None = None
    rights_scope: str | None = None
    publish_status: str | None = None
    first_publish_date: str | None = None
    first_publish_location: str | None = None
    # Generation options
    generate_source_code: bool = True
    generate_db_design: bool = True
    generate_diagrams: bool = True
    # Applicant info
    applicant_name: str | None = None
    applicant_type: str | None = None
    nationality: str | None = None
    province: str | None = None
    city: str | None = None


class ApplicationUpdate(BaseModel):
    # Required (all optional for update)
    software_name: str | None = None
    software_short_name: str | None = None
    main_features: str | None = None
    # Basic optional
    software_version: str | None = None
    software_category: str | None = None
    runtime_platform: str | None = None
    completion_date: str | None = None
    software_description: str | None = None
    # Development info
    development_language: str | None = None
    code_line_count: str | None = None
    development_method: str | None = None
    dev_hardware: str | None = None
    dev_os: str | None = None
    dev_tools: str | None = None
    # Runtime environment
    runtime_hardware: str | None = None
    runtime_software: str | None = None
    # Technical features
    technical_features: str | None = None
    module_design: str | None = None
    development_purpose: str | None = None
    target_industry: str | None = None
    # Rights info
    work_type: str | None = None
    rights_acquisition: str | None = None
    rights_scope: str | None = None
    publish_status: str | None = None
    first_publish_date: str | None = None
    first_publish_location: str | None = None
    # Generation options
    generate_source_code: bool | None = None
    generate_db_design: bool | None = None
    generate_diagrams: bool | None = None
    # Applicant info
    applicant_name: str | None = None
    applicant_type: str | None = None
    nationality: str | None = None
    province: str | None = None
    city: str | None = None


class StatusTransitionRequest(BaseModel):
    """状态转换请求"""
    target_status: ApplicationStatus = Field(..., description="目标状态")
    comment: str | None = Field(None, max_length=500, description="备注信息（如驳回原因等）")


class ApplicationResponse(BaseModel):
    id: int
    status: str
    # Required
    software_name: str | None = None
    software_short_name: str | None = None
    main_features: str | None = None
    # Basic optional
    software_version: str | None = None
    software_category: str | None = None
    runtime_platform: str | None = None
    completion_date: str | None = None
    software_description: str | None = None
    # Development info
    development_language: str | None = None
    code_line_count: str | None = None
    development_method: str | None = None
    dev_hardware: str | None = None
    dev_os: str | None = None
    dev_tools: str | None = None
    # Runtime environment
    runtime_hardware: str | None = None
    runtime_software: str | None = None
    # Technical features
    technical_features: str | None = None
    module_design: str | None = None
    development_purpose: str | None = None
    target_industry: str | None = None
    # Rights info
    work_type: str | None = None
    rights_acquisition: str | None = None
    rights_scope: str | None = None
    publish_status: str | None = None
    first_publish_date: str | None = None
    first_publish_location: str | None = None
    # Generation options
    generate_source_code: bool = True
    generate_db_design: bool = True
    generate_diagrams: bool = True
    # Applicant info
    applicant_name: str | None = None
    applicant_type: str | None = None
    nationality: str | None = None
    province: str | None = None
    city: str | None = None
    # Timestamps
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
