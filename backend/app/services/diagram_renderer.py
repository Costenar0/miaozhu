"""
图表渲染服务

架构图 / UML 类图：通过 Kroki.io 公共 API 将 Mermaid / PlantUML 代码渲染为 PNG
功能界面图：通过 Playwright 将 HTML 模板截图为 PNG

服务器依赖（部署时安装）：
    pip install playwright httpx
    playwright install chromium
    playwright install-deps chromium
"""

import io
import logging
import re

import httpx

logger = logging.getLogger(__name__)

KROKI_URL = "https://kroki.io"
KROKI_TIMEOUT = 30  # seconds


# ── Kroki.io 渲染 ──────────────────────────────────────────────────────────

def _kroki_render(diagram_type: str, source: str) -> bytes:
    """调用 Kroki.io 公共 API，将图表代码渲染为 PNG 字节。"""
    with httpx.Client(timeout=KROKI_TIMEOUT) as client:
        resp = client.post(
            f"{KROKI_URL}/{diagram_type}/png",
            json={"diagram_source": source},
        )
        resp.raise_for_status()
        return resp.content


def render_mermaid(source: str) -> bytes:
    """渲染 Mermaid 图表代码 → PNG"""
    return _kroki_render("mermaid", source)


def render_plantuml(source: str) -> bytes:
    """渲染 PlantUML 代码 → PNG"""
    return _kroki_render("plantuml", source)


def render_d2(source: str) -> bytes:
    """渲染 D2 架构图代码 → PNG（分层容器更清晰，适合展示 Nginx/网关/应用/缓存/数据库）"""
    return _kroki_render("d2", source)


# ── Playwright HTML 截图 ───────────────────────────────────────────────────

def render_html_screenshot(html: str, width: int = 750, height: int = 560) -> bytes:
    """用 Playwright 无头浏览器将 HTML 字符串截图为 PNG 字节。

    默认使用 750×560 视口（与 prompt 中 HTML 模板尺寸对应），
    device_scale_factor=2 输出 Retina 质量（实际像素 1500×1120）。
    """
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=2,
        )
        page.set_content(html, wait_until="networkidle")
        data = page.screenshot(full_page=False)
        browser.close()
    return data


# ── 内容解析 ───────────────────────────────────────────────────────────────

def _extract_code_block(content: str, lang: str = "") -> str:
    """从 markdown 代码块中提取内容，失败则返回原文。"""
    pattern = rf"```{lang}\s*([\s\S]*?)```"
    m = re.search(pattern, content, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # 尝试通用代码块
    m = re.search(r"```\s*([\s\S]*?)```", content)
    if m:
        return m.group(1).strip()
    return content.strip()


# ── 主入口：section_key → PNG bytes ───────────────────────────────────────

def render_diagram_section(section_key: str, content: str) -> bytes | None:
    """
    根据 section_key 和 LLM 生成的内容，渲染为 PNG 字节。
    返回 None 表示内容为空或渲染失败。
    """
    if not content or not content.strip():
        return None

    try:
        if section_key == "arch_diagram":
            code = _extract_code_block(content, "mermaid")
            return render_mermaid(code)

        elif section_key == "uml_diagram":
            code = _extract_code_block(content, "plantuml")
            if not code.startswith("@startuml"):
                code = f"@startuml\n{code}\n@enduml"
            return render_plantuml(code)

        elif section_key == "ui_diagrams":
            html = _extract_code_block(content, "html")
            return render_html_screenshot(html)

    except Exception as e:
        logger.warning("render_diagram_section(%s) failed: %s", section_key, e)
        return None

    return None
