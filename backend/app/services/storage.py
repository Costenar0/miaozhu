"""本地文件存储服务 — 替代 OSS"""

import logging
import os
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger(__name__)


def _get_export_dir() -> Path:
    base = Path(settings.EXPORT_DATA_DIR)
    if not base.is_absolute():
        base = Path(os.getcwd()) / base
    base.mkdir(parents=True, exist_ok=True)
    return base


def save_file(file_path: str, data: bytes) -> int:
    """保存文件到本地存储，返回文件大小（字节）"""
    full_path = _get_export_dir() / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_bytes(data)
    logger.info("Saved file: %s (%d bytes)", full_path, len(data))
    return len(data)


def get_full_path(file_path: str) -> Path:
    """获取文件的完整路径"""
    return _get_export_dir() / file_path
