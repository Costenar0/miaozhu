"""Diagram generators for software copyright documents.

Uses ReportLab Graphics API to produce vector diagrams (no extra dependencies).
Drawings can be added directly to a ReportLab platypus story.
"""

import json
import logging
import re
from typing import Optional

from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import cm

logger = logging.getLogger(__name__)

_CN_FONT = "STSong-Light"

# ── Color palette ─────────────────────────────────────────────
_C_NAV    = HexColor("#1B2A4A")
_C_SB     = HexColor("#2C3E50")
_C_ACCENT = HexColor("#409EFF")
_C_BG     = HexColor("#F5F7FA")
_C_BORDER = HexColor("#DCDFE6")
_C_TEXT   = HexColor("#303133")
_C_TEXT2  = HexColor("#909399")

_LAYER_PALETTE = [
    (HexColor("#2D7DD2"), HexColor("#EBF4FF")),  # blue  – presentation
    (HexColor("#2A9D5C"), HexColor("#EAFAF1")),  # green – business
    (HexColor("#E07B2A"), HexColor("#FEF5E7")),  # orange– data access
    (HexColor("#7B5EA7"), HexColor("#F5EEF8")),  # purple– storage
    (HexColor("#C0392B"), HexColor("#FDEDEC")),  # red   – external
]

# ── Layout constants ───────────────────────────────────────────
_ARCH_W  = 16.46 * cm   # fits A4 content width
_UI_W    = 14.0  * cm
_UI_H    = 9.5   * cm
_NAV_H   = 0.85  * cm
_SB_W    = 2.8   * cm


def _reg_fonts() -> None:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    if _CN_FONT not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(UnicodeCIDFont(_CN_FONT))


def parse_diagram_json(content: str) -> Optional[dict]:
    """Parse JSON from LLM section content, stripping markdown code fences."""
    if not content:
        return None
    text = content.strip()
    if text.startswith("```"):
        inner, in_block = [], False
        for line in text.split("\n"):
            if line.strip().startswith("```"):
                in_block = not in_block
                continue
            if in_block:
                inner.append(line)
        text = "\n".join(inner).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r'\{[\s\S]*\}', text)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
    logger.warning("Could not parse diagram JSON from section content")
    return None


# ── Architecture Diagram ──────────────────────────────────────

def render_arch_diagram(data: dict) -> Optional[Drawing]:
    """Render system architecture diagram as a ReportLab Drawing.

    Expected JSON format::

        {
          "title": "XX系统架构图",
          "layers": [
            {"name": "前端展示层", "items": ["Web管理端", "移动H5"]},
            {"name": "业务逻辑层", "items": ["用户管理", "商品管理", "报表"]},
            {"name": "数据访问层", "items": ["API网关", "Redis缓存"]},
            {"name": "数据存储层", "items": ["MySQL", "文件存储"]}
          ]
        }

    Returns a ``Drawing`` that can be appended directly to a platypus story.
    """
    _reg_fonts()
    layers = data.get("layers", [])
    if not layers:
        return None

    LAYER_H = 2.0 * cm
    GAP     = 0.45 * cm
    PAD     = 0.5  * cm
    LABEL_W = 2.5  * cm
    TITLE_H = 1.2  * cm
    n       = len(layers)

    total_h = PAD + TITLE_H + n * LAYER_H + (n - 1) * GAP + PAD
    d = Drawing(_ARCH_W, total_h)

    # Background
    d.add(Rect(0, 0, _ARCH_W, total_h, fillColor=_C_BG, strokeColor=None))

    # Title
    d.add(String(
        _ARCH_W / 2, total_h - PAD - TITLE_H / 2 - 5,
        data.get("title", "系统架构图"),
        fontName=_CN_FONT, fontSize=13, fillColor=_C_NAV, textAnchor="middle",
    ))

    for i, layer in enumerate(layers):
        dark, light = _LAYER_PALETTE[i % len(_LAYER_PALETTE)]
        # y_bottom in ReportLab coordinates (origin = bottom-left)
        y     = total_h - PAD - TITLE_H - (i + 1) * LAYER_H - i * GAP
        name  = layer.get("name", f"第{i + 1}层")
        items = layer.get("items", [])

        # Label box (dark, left side)
        d.add(Rect(PAD, y, LABEL_W, LAYER_H,
                   fillColor=dark, strokeColor=None, rx=4, ry=4))
        d.add(String(
            PAD + LABEL_W / 2, y + LAYER_H / 2 - 5, name,
            fontName=_CN_FONT, fontSize=9, fillColor=white, textAnchor="middle",
        ))

        # Items container (light, right side)
        ix = PAD + LABEL_W + 0.3 * cm
        iw = _ARCH_W - ix - PAD
        d.add(Rect(ix, y, iw, LAYER_H,
                   fillColor=light, strokeColor=dark, strokeWidth=0.5,
                   rx=4, ry=4))

        # Item chips
        if items:
            chip_gap = 0.2 * cm
            chip_h   = LAYER_H - 0.5 * cm
            chip_w   = (iw - chip_gap * (len(items) + 1)) / max(len(items), 1)
            for j, item in enumerate(items):
                cx = ix + chip_gap + j * (chip_w + chip_gap)
                cy = y + (LAYER_H - chip_h) / 2
                d.add(Rect(cx, cy, chip_w, chip_h,
                           fillColor=dark, strokeColor=None, rx=3, ry=3))
                label = item[:8] if len(item) > 8 else item
                d.add(String(
                    cx + chip_w / 2, cy + chip_h / 2 - 4, label,
                    fontName=_CN_FONT, fontSize=8, fillColor=white, textAnchor="middle",
                ))

        # Downward arrow connector between layers
        if i < n - 1:
            ax = _ARCH_W / 2
            d.add(Line(ax, y, ax, y - GAP, strokeColor=_C_TEXT2, strokeWidth=1.2))
            d.add(Polygon(
                [ax - 4, y - GAP + 5, ax + 4, y - GAP + 5, ax, y - GAP],
                fillColor=_C_TEXT2, strokeColor=None,
            ))

    return d


# ── UI Screen Mockups ────────────────────────────────────────

def _txt(d: Drawing, x, y, text: str, size=8, color=None, anchor="start"):
    if color is None:
        color = _C_TEXT
    if len(text) > 12:
        text = text[:11] + "…"
    d.add(String(x, y, text, fontName=_CN_FONT, fontSize=size,
                 fillColor=color, textAnchor=anchor))


def _nav(d: Drawing, title: str, items: list):
    H = _UI_H
    d.add(Rect(0, H - _NAV_H, _UI_W, _NAV_H, fillColor=_C_NAV, strokeColor=None))
    d.add(Rect(0.25 * cm, H - _NAV_H + 0.18 * cm, 0.5 * cm, 0.5 * cm,
               fillColor=_C_ACCENT, strokeColor=None, rx=2, ry=2))
    _txt(d, 0.9 * cm, H - _NAV_H + 0.26 * cm, title, 8, white)
    x = 5.5 * cm
    for item in items[:5]:
        _txt(d, x, H - _NAV_H + 0.26 * cm, item[:4], 7, HexColor("#BDC3C7"))
        x += 1.8 * cm


def _sidebar(d: Drawing, items: list):
    d.add(Rect(0, 0, _SB_W, _UI_H - _NAV_H, fillColor=_C_SB, strokeColor=None))
    for i, item in enumerate(items[:8]):
        sy = _UI_H - _NAV_H - 0.6 * cm - i * 0.65 * cm
        if sy < 0.1 * cm:
            break
        if i == 0:
            d.add(Rect(0.1 * cm, sy - 0.08 * cm, _SB_W - 0.2 * cm, 0.48 * cm,
                       fillColor=_C_ACCENT, strokeColor=None, rx=2, ry=2))
            _txt(d, 0.4 * cm, sy + 0.06 * cm, item, 7, white)
        else:
            _txt(d, 0.4 * cm, sy + 0.06 * cm, item, 7, HexColor("#BDC3C7"))


def _content_rect(has_sb: bool) -> tuple:
    cx = _SB_W if has_sb else 0
    return cx, 0, _UI_W - cx, _UI_H - _NAV_H


def _login(d: Drawing):
    cx, cy, cw, ch = _content_rect(False)
    cw2, ch2 = 5 * cm, 5 * cm
    bx, by = cx + (cw - cw2) / 2, cy + (ch - ch2) / 2
    d.add(Rect(bx, by, cw2, ch2,
               fillColor=white, strokeColor=_C_BORDER, strokeWidth=0.5, rx=6, ry=6))
    _txt(d, cx + cw / 2, by + ch2 - 0.7 * cm, "用户登录", 11, _C_NAV, "middle")
    for i, lbl in enumerate(["用 户 名", "密    码"]):
        fy = by + ch2 - 1.6 * cm - i * 1.3 * cm
        d.add(Rect(bx + 0.4 * cm, fy, cw2 - 0.8 * cm, 0.55 * cm,
                   fillColor=_C_BG, strokeColor=_C_BORDER, strokeWidth=0.5, rx=3, ry=3))
        _txt(d, bx + 0.65 * cm, fy + 0.15 * cm, lbl, 7, _C_TEXT2)
    btn_y = by + 0.5 * cm
    d.add(Rect(bx + 0.4 * cm, btn_y, cw2 - 0.8 * cm, 0.6 * cm,
               fillColor=_C_ACCENT, strokeColor=None, rx=3, ry=3))
    _txt(d, bx + cw2 / 2, btn_y + 0.18 * cm, "登  录", 9, white, "middle")


def _dashboard(d: Drawing, has_sb: bool, cards: list):
    cx, cy, cw, ch = _content_rect(has_sb)
    # Breadcrumb
    d.add(Rect(cx, cy + ch - 0.5 * cm, cw, 0.5 * cm,
               fillColor=white, strokeColor=_C_BORDER, strokeWidth=0.3))
    _txt(d, cx + 0.3 * cm, cy + ch - 0.36 * cm, "首页  /  数据概览", 7, _C_TEXT2)
    # Stat cards (2 × 2 grid)
    n_col, n_row = 2, 2
    pad = 0.25 * cm
    cw2 = (cw - pad * (n_col + 1)) / n_col
    ch2 = 1.2 * cm
    labels = (cards or ["统计1", "统计2", "统计3", "统计4"])[:4]
    for idx in range(n_col * n_row):
        col = idx % n_col
        row = idx // n_col
        kx = cx + pad + col * (cw2 + pad)
        ky = cy + ch - 0.5 * cm - pad - (row + 1) * ch2 - row * pad
        c_dark = _LAYER_PALETTE[idx % len(_LAYER_PALETTE)][0]
        d.add(Rect(kx, ky, cw2, ch2,
                   fillColor=white, strokeColor=_C_BORDER, strokeWidth=0.5, rx=4, ry=4))
        d.add(Rect(kx, ky + ch2 - 0.25 * cm, 0.18 * cm, 0.25 * cm,
                   fillColor=c_dark, strokeColor=None))
        _txt(d, kx + 0.3 * cm, ky + ch2 - 0.42 * cm, labels[idx], 7, _C_TEXT2)
        _txt(d, kx + 0.3 * cm, ky + 0.22 * cm, "—  —", 9, c_dark)
    # Chart placeholder
    chart_top = cy + ch - 0.5 * cm - pad - n_row * (ch2 + pad)
    chart_h   = chart_top - cy - pad
    if chart_h > cm:
        d.add(Rect(cx + pad, cy + pad, cw - pad * 2, chart_h,
                   fillColor=white, strokeColor=_C_BORDER, strokeWidth=0.5, rx=4, ry=4))
        _txt(d, cx + cw / 2, cy + pad + chart_h / 2 - 4, "数据统计图表", 8, _C_TEXT2, "middle")
        bw = (cw - pad * 4) / 7
        for bi in range(6):
            bx2 = cx + pad * 2 + bi * (bw + 0.1 * cm)
            bh2 = (0.3 + bi * 0.08) * cm
            d.add(Rect(bx2, cy + pad + 0.3 * cm, bw * 0.6, bh2,
                       fillColor=_C_ACCENT, strokeColor=None, rx=1, ry=1))


def _list_view(d: Drawing, has_sb: bool, columns: list):
    cx, cy, cw, ch = _content_rect(has_sb)
    pad = 0.25 * cm
    # Toolbar
    d.add(Rect(cx, cy + ch - 0.5 * cm, cw, 0.5 * cm,
               fillColor=white, strokeColor=_C_BORDER, strokeWidth=0.3))
    d.add(Rect(cx + pad, cy + ch - 0.42 * cm, 2.3 * cm, 0.34 * cm,
               fillColor=_C_BG, strokeColor=_C_BORDER, strokeWidth=0.3, rx=2, ry=2))
    _txt(d, cx + pad + 0.15 * cm, cy + ch - 0.36 * cm, "搜索...", 7, _C_TEXT2)
    d.add(Rect(cx + cw - 1.5 * cm, cy + ch - 0.42 * cm, 1.2 * cm, 0.34 * cm,
               fillColor=_C_ACCENT, strokeColor=None, rx=2, ry=2))
    _txt(d, cx + cw - 0.9 * cm, cy + ch - 0.36 * cm, "+ 新增", 7, white, "middle")
    # Table header
    cols = columns[:5] if columns else ["名称", "状态", "时间", "操作"]
    table_h = ch - 0.5 * cm - 0.1 * cm
    row_h   = min(0.6 * cm, table_h / max(len(cols), 1))
    col_w   = (cw - pad * 2) / len(cols)
    hdr_y   = cy + table_h - row_h
    d.add(Rect(cx, hdr_y, cw, row_h,
               fillColor=_C_BG, strokeColor=_C_BORDER, strokeWidth=0.3))
    for ci, col in enumerate(cols):
        _txt(d, cx + pad + ci * col_w, hdr_y + 0.15 * cm, col, 7, _C_TEXT2)
    # Data rows
    n_rows = int((table_h - row_h) / row_h)
    for ri in range(min(n_rows, 5)):
        ry = hdr_y - (ri + 1) * row_h
        if ry < cy:
            break
        d.add(Rect(cx, ry, cw, row_h,
                   fillColor=white if ri % 2 == 0 else _C_BG,
                   strokeColor=_C_BORDER, strokeWidth=0.2))
        for ci in range(len(cols)):
            if ci == len(cols) - 1:
                d.add(Rect(cx + pad + ci * col_w, ry + 0.12 * cm, 0.6 * cm, 0.32 * cm,
                           fillColor=HexColor("#ECF5FF"),
                           strokeColor=_C_ACCENT, strokeWidth=0.3, rx=2, ry=2))
                _txt(d, cx + pad + ci * col_w + 0.3 * cm, ry + 0.18 * cm,
                     "编辑", 6, _C_ACCENT, "middle")
            else:
                _txt(d, cx + pad + ci * col_w, ry + 0.18 * cm, f"数据{ri + 1}", 7, _C_TEXT)


def _form_view(d: Drawing, has_sb: bool, fields: list):
    cx, cy, cw, ch = _content_rect(has_sb)
    pad = 0.3 * cm
    d.add(Rect(cx + pad, cy + pad, cw - pad * 2, ch - pad,
               fillColor=white, strokeColor=_C_BORDER, strokeWidth=0.5, rx=4, ry=4))
    flds    = fields[:6] if fields else ["名称", "类型", "描述", "状态"]
    label_w = 2.0 * cm
    field_h = 0.5 * cm
    gap     = 0.35 * cm
    start_y = cy + ch - pad - 0.5 * cm
    for i, f in enumerate(flds):
        fy = start_y - i * (field_h + gap)
        if fy < cy + pad + 0.9 * cm:
            break
        _txt(d, cx + pad * 2, fy + 0.12 * cm, f + "：", 7, _C_TEXT2)
        d.add(Rect(cx + pad * 2 + label_w, fy, cw - pad * 3 - label_w, field_h,
                   fillColor=_C_BG, strokeColor=_C_BORDER, strokeWidth=0.3, rx=2, ry=2))
    # Buttons
    by = cy + pad + 0.3 * cm
    d.add(Rect(cx + pad * 2, by, 1.5 * cm, 0.5 * cm,
               fillColor=_C_ACCENT, strokeColor=None, rx=3, ry=3))
    _txt(d, cx + pad * 2 + 0.75 * cm, by + 0.13 * cm, "提  交", 8, white, "middle")
    d.add(Rect(cx + pad * 2 + 1.7 * cm, by, 1.2 * cm, 0.5 * cm,
               fillColor=white, strokeColor=_C_BORDER, strokeWidth=0.5, rx=3, ry=3))
    _txt(d, cx + pad * 2 + 2.3 * cm, by + 0.13 * cm, "取  消", 8, _C_TEXT2, "middle")


def render_ui_screens(data: dict) -> list:
    """Render UI screen mockups as a list of (title, Drawing) tuples.

    Expected JSON format::

        {
          "screens": [
            {"title": "系统登录", "type": "login"},
            {"title": "系统首页", "type": "dashboard",
             "nav": ["首页","用户管理"], "sidebar": ["概览","统计"],
             "cards": ["用户 1,234", "订单 56", "收入 ¥12,345", "待处理 8"]},
            {"title": "数据列表", "type": "list",
             "nav": ["首页","用户管理"], "sidebar": ["列表","归档"],
             "columns": ["名称","状态","时间","操作"]},
            {"title": "编辑信息", "type": "form",
             "nav": ["首页","用户管理"], "sidebar": ["列表","归档"],
             "fields": ["名称","类型","描述","状态"]}
          ]
        }
    """
    _reg_fonts()
    screens = data.get("screens", [])
    if not screens:
        return []

    results = []
    for screen in screens[:6]:
        title  = screen.get("title", "功能界面")
        stype  = screen.get("type", "default")
        nav    = screen.get("nav", [])
        sidebar = screen.get("sidebar", [])
        has_sb  = bool(sidebar)

        d = Drawing(_UI_W, _UI_H)
        # Outer frame + content background
        d.add(Rect(0, 0, _UI_W, _UI_H,
                   fillColor=white, strokeColor=_C_BORDER, strokeWidth=0.8, rx=4, ry=4))
        cx2 = _SB_W if has_sb else 0
        d.add(Rect(cx2, 0, _UI_W - cx2, _UI_H - _NAV_H, fillColor=_C_BG, strokeColor=None))

        _nav(d, title, nav)
        if has_sb:
            _sidebar(d, sidebar)

        if stype == "login":
            _login(d)
        elif stype == "dashboard":
            _dashboard(d, has_sb, screen.get("cards", []))
        elif stype == "list":
            _list_view(d, has_sb, screen.get("columns", []))
        elif stype == "form":
            _form_view(d, has_sb, screen.get("fields", []))
        else:
            _cx, _cy, _cw, _ch = _content_rect(has_sb)
            _txt(d, _cx + _cw / 2, _cy + _ch / 2 - 4,
                 f"【{title}】", 10, _C_TEXT2, "middle")

        results.append((title, d))

    return results
