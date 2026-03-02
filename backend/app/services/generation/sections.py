from dataclasses import dataclass


@dataclass(frozen=True)
class SectionDef:
    key: str
    title: str
    order: int
    max_tokens: int
    group: str = "manual"  # manual / source_code / db_design / meta


# 操作说明书章节（目标：总计 55 页，每页约 30 行）
MANUAL_SECTIONS: list[SectionDef] = [
    SectionDef(key="manual_introduction", title="引言", order=1, max_tokens=16384, group="manual"),
    SectionDef(key="manual_overview",     title="软件概述", order=2, max_tokens=24576, group="manual"),  # 含架构图+类图
    SectionDef(key="manual_environment",  title="运行环境", order=3, max_tokens=16384, group="manual"),
    SectionDef(key="manual_installation", title="安装与配置", order=4, max_tokens=16384, group="manual"),
    SectionDef(key="manual_functions_1",  title="功能详述（上）", order=5, max_tokens=32768, group="manual"),  # 含每功能HTML
    SectionDef(key="manual_functions_2",  title="功能详述（下）", order=6, max_tokens=32768, group="manual"),  # 含每功能HTML
    SectionDef(key="manual_security",     title="安全管理与权限控制", order=7, max_tokens=16384, group="manual"),
    SectionDef(key="manual_other_notes",  title="其他说明", order=8, max_tokens=16384, group="manual"),
]

# 数据库设计章节
DB_DESIGN_SECTIONS: list[SectionDef] = [
    SectionDef(key="db_design", title="数据库设计", order=9, max_tokens=16384, group="db_design"),
]

# 源程序代码章节（目标：总计 60 页，每页 50 行）
SOURCE_CODE_SECTIONS: list[SectionDef] = [
    SectionDef(key="source_code_front", title="源程序代码（前30页）", order=10, max_tokens=16384, group="source_code"),
    SectionDef(key="source_code_back", title="源程序代码（后30页）", order=11, max_tokens=16384, group="source_code"),
]

# 元数据章节（始终包含）
META_SECTIONS: list[SectionDef] = [
    SectionDef(key="form_autofill", title="申请表字段自动填充", order=99, max_tokens=2048, group="meta"),
]

# 图片章节（可选，勾选「生成图表」后纳入主生成流程）
DIAGRAM_SECTIONS: list[SectionDef] = [
    SectionDef(key="arch_diagram",  title="系统架构图", order=20, max_tokens=8192,  group="diagram"),
    SectionDef(key="uml_diagram",   title="UML类图",   order=21, max_tokens=8192,  group="diagram"),
    SectionDef(key="ui_diagrams",   title="功能界面图", order=22, max_tokens=16384, group="diagram"),
]

# 完整列表
SECTIONS: list[SectionDef] = (
    MANUAL_SECTIONS + DB_DESIGN_SECTIONS + SOURCE_CODE_SECTIONS + META_SECTIONS + DIAGRAM_SECTIONS
)

SECTION_MAP: dict[str, SectionDef] = {s.key: s for s in SECTIONS}

# 旧版 section key 向后兼容
SECTION_MAP["manual_functions"] = SectionDef(
    key="manual_functions", title="功能详述", order=5, max_tokens=8192, group="manual",
)
# ui_diagrams 旧 key 向后兼容（旧任务只有 arch_diagram + ui_diagrams，没有 uml_diagram）
# SECTION_MAP 已包含，此处无需重复
