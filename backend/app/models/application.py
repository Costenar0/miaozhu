from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(50), default="draft")

    # Required
    software_name: Mapped[str] = mapped_column(String(255), nullable=True)
    software_short_name: Mapped[str] = mapped_column(String(100), nullable=True)
    main_features: Mapped[str] = mapped_column(Text, nullable=True)

    # Basic optional
    software_version: Mapped[str] = mapped_column(String(50), nullable=True)
    software_category: Mapped[str] = mapped_column(String(100), nullable=True)
    runtime_platform: Mapped[str] = mapped_column(String(255), nullable=True)
    completion_date: Mapped[str] = mapped_column(String(20), nullable=True)
    software_description: Mapped[str] = mapped_column(Text, nullable=True)

    # Development info
    development_language: Mapped[str] = mapped_column(String(255), nullable=True)
    code_line_count: Mapped[str] = mapped_column(String(50), nullable=True)
    development_method: Mapped[str] = mapped_column(String(50), nullable=True)
    dev_hardware: Mapped[str] = mapped_column(String(255), nullable=True)
    dev_os: Mapped[str] = mapped_column(String(255), nullable=True)
    dev_tools: Mapped[str] = mapped_column(String(255), nullable=True)

    # Runtime environment
    runtime_hardware: Mapped[str] = mapped_column(String(255), nullable=True)
    runtime_software: Mapped[str] = mapped_column(String(255), nullable=True)

    # Technical features
    technical_features: Mapped[str] = mapped_column(String(255), nullable=True)
    module_design: Mapped[str] = mapped_column(Text, nullable=True)
    development_purpose: Mapped[str] = mapped_column(Text, nullable=True)
    target_industry: Mapped[str] = mapped_column(String(255), nullable=True)

    # Rights info
    work_type: Mapped[str] = mapped_column(String(50), nullable=True)
    rights_acquisition: Mapped[str] = mapped_column(String(50), nullable=True)
    rights_scope: Mapped[str] = mapped_column(String(50), nullable=True)
    publish_status: Mapped[str] = mapped_column(String(50), nullable=True)
    first_publish_date: Mapped[str] = mapped_column(String(20), nullable=True)
    first_publish_location: Mapped[str] = mapped_column(String(255), nullable=True)

    # Generation options
    generate_source_code: Mapped[bool] = mapped_column(Boolean, default=True)
    generate_db_design: Mapped[bool] = mapped_column(Boolean, default=True)
    generate_diagrams: Mapped[bool] = mapped_column(Boolean, default=False)

    # Applicant info
    applicant_name: Mapped[str] = mapped_column(String(255), nullable=True)
    applicant_type: Mapped[str] = mapped_column(String(50), nullable=True)
    nationality: Mapped[str] = mapped_column(String(100), nullable=True)
    province: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)

    # Generated docs
    generated_source_code: Mapped[str] = mapped_column(Text, nullable=True)
    generated_manual: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
