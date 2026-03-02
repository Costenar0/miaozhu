# 秒著 - AI 软件著作权申请材料生成系统

一个基于 AI 的软件著作权申请材料自动生成系统，帮助用户快速生成规范的软著申请文档。

---

## ✨ 功能特性

### 核心功能

- **智能材料生成**
  - AI 自动生成操作说明书（60+ 页，30+ 行/页）
  - AI 自动生成源程序代码（60+ 页，50+ 行/页）
  - AI 自动生成数据库设计文档
  - 支持自定义生成指令

- **文档导出**
  - Word 格式导出（符合软著申请格式要求）
  - PDF 格式导出（带目录、自动分页）
  - 封面页符合版权局规范
  - 自动编号和层次结构

- **状态管理**
  - 完整的申请状态流转（草稿 → 生成中 → 已生成 → 准备提交 → 已提交 → 已通过）
  - 状态转换权限控制
  - 自动状态同步

- **实时进度**
  - SSE（Server-Sent Events）实时推送生成进度
  - 章节级别的状态跟踪
  - 错误自动重试机制

### 技术亮点

- **异步架构**：FastAPI + SQLAlchemy 异步 ORM
- **并发控制**：信号量限制 LLM 并发调用
- **分布式锁**：Redis 实现多 worker 调度器协调
- **超时保护**：30 分钟超时自动清理
- **Markdown 解析**：Mistletoe 精确解析，正确区分标题和列表
- **重试机制**：网络错误自动重试（2s, 5s, 10s 间隔）

---

## 🏗️ 技术架构

### 后端技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| Web 框架 | FastAPI | 高性能异步 Python Web 框架 |
| 数据库 | MySQL 8.0 | 主数据存储 |
| ORM | SQLAlchemy 2.x | 异步 ORM，类型安全 |
| 缓存 | Redis | 分布式锁、nonce 验证 |
| 数据库迁移 | Alembic | 版本化管理数据库结构 |
| ASGI 服务器 | Gunicorn + Uvicorn | 生产环境多进程部署 |
| AI 模型 | DeepSeek API | 大语言模型（支持多轮续写） |
| 文档生成 | python-docx, ReportLab | Word/PDF 文档生成 |
| Markdown 解析 | mistletoe | 规范化 Markdown 解析 |

### 前端技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 框架 | Vue 3 | 渐进式前端框架 |
| 语言 | TypeScript | 类型安全的 JavaScript |
| 构建工具 | Vite | 极速的前端构建工具 |
| UI 框架 | Element Plus | Vue 3 组件库 |
| 状态管理 | Pinia | Vue 官方状态管理库 |
| 路由 | Vue Router | 官方路由管理 |
| HTTP 客户端 | Axios | Promise 化的 HTTP 库 |
| 包管理 | pnpm | 快速、节省空间的包管理器 |

---

## 📁 项目结构

```
miaozhu/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── main.py         # FastAPI 应用入口
│   │   ├── api/            # API 路由
│   │   │   └── v1/         # API v1
│   │   │       ├── applications.py  # 软著申请管理
│   │   │       ├── generation.py    # AI 生成管理
│   │   │       ├── exports.py       # 文档导出
│   │   │       └── sse.py           # 实时进度推送
│   │   ├── models/         # SQLAlchemy 模型
│   │   │   ├── application.py       # 软著申请
│   │   │   ├── generation.py        # 生成任务
│   │   │   └── user.py              # 用户
│   │   ├── schemas/        # Pydantic 模型
│   │   │   ├── application.py       # 状态枚举、转换规则
│   │   │   └── generation.py
│   │   ├── services/       # 业务逻辑
│   │   │   ├── generation/          # 生成服务
│   │   │   │   ├── scheduler.py     # 任务调度器
│   │   │   │   └── orchestrator.py  # 生成编排
│   │   │   ├── llm/                 # LLM 集成
│   │   │   │   ├── base.py
│   │   │   │   ├── deepseek.py      # DeepSeek 实现
│   │   │   │   └── factory.py
│   │   │   ├── prompts/             # 提示词管理
│   │   │   │   └── copyright.py     # 软著提示词
│   │   │   └── document_export.py   # 文档导出
│   │   └── core/           # 核心配置
│   │       ├── config.py            # 配置管理
│   │       ├── database.py          # 数据库连接
│   │       └── redis.py             # Redis 连接
│   ├── alembic/            # 数据库迁移
│   │   └── versions/       # 迁移版本
│   └── requirements.txt    # Python 依赖
│
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── main.ts         # 应用入口
│   │   ├── views/          # 页面组件
│   │   │   ├── copyright/
│   │   │   │   ├── CopyrightCreateView.vue    # 创建申请
│   │   │   │   ├── CopyrightListView.vue      # 申请列表
│   │   │   │   └── CopyrightGenerateView.vue  # 生成进度
│   │   │   └── ...
│   │   ├── api/            # API 调用封装
│   │   │   ├── client.ts            # Axios 配置
│   │   │   ├── application.ts       # 申请 API
│   │   │   └── generation.ts        # 生成 API
│   │   ├── stores/         # Pinia 状态
│   │   └── router/         # 路由配置
│   ├── vite.config.ts      # Vite 配置
│   └── package.json        # Node 依赖
│
└── docs/                   # 项目文档
    └── 启动指南.md         # 启动命令详解
```

---

## 🚀 快速开始

### 最小化安装（5 分钟）

```bash
# 1. 克隆项目
git clone <repository-url>
cd miaozhu

# 2. 后端启动
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# 修改 app/core/config.py 中的数据库配置
alembic upgrade head
uvicorn app.main:app --reload

# 3. 前端启动（新终端）
cd frontend
pnpm install
pnpm dev

# 4. 访问应用
# 前端：http://localhost:5173
# 后端：http://localhost:8000/docs
```

### 详细文档

完整的启动指南、配置说明、部署方案，请查看：
- **[启动指南](docs/启动指南.md)** - 包含所有命令的详细解释

---

## 🔑 核心概念

### 状态流转

```
draft (草稿)
  ↓ 点击"开始生成"
generating (生成中) ← 自动
  ↓ 生成完成
generated (已生成)
  ↓ 用户审核通过
ready (准备提交)
  ↓ 提交到版权局
submitted (已提交)
  ↓ 版权局审批
approved (已通过) / rejected (已驳回)
  ↓
archived (已归档)
```

### 生成流程

1. **用户填写软件信息** → 创建申请（status: draft）
2. **点击开始生成** → 创建生成任务（status: generating）
3. **调度器轮询** → 获取 pending 任务
4. **AI 生成章节** → 并发生成（限制 3 个并发）
5. **实时推送进度** → SSE 推送到前端
6. **生成完成** → 更新状态（status: generated）
7. **用户导出文档** → Word/PDF 下载

### 调度器机制

- **Redis 分布式锁**：确保多 worker 环境只有一个调度器运行
- **轮询间隔**：5 秒（可配置）
- **并发控制**：asyncio.Semaphore 限制同时调用 LLM 数量
- **超时清理**：30 分钟超时自动标记失败
- **状态同步**：每轮轮询检查 task 状态与 sections 是否一致

---

## 📊 系统要求

### 开发环境

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis 6+
- 4GB+ RAM
- 10GB+ 磁盘空间

### 生产环境推荐

- **服务器**：4C8G（4 核 8GB 内存）
- **MySQL**：独立数据库服务器或 RDS
- **Redis**：独立 Redis 服务器
- **Nginx**：反向代理 + 静态文件服务
- **Gunicorn Workers**：9 个（2×CPU核心+1）
- **LLM 并发数**：3 个（可根据 API 配额调整）

---

## 🔐 安全特性

- **JWT 认证**：Access Token + Refresh Token
- **请求签名**：所有 API 请求需签名验证
- **Nonce 防重放**：60 秒内不允许重复请求
- **CORS 限制**：仅允许配置的域名跨域
- **SQL 注入防护**：SQLAlchemy ORM 自动转义
- **XSS 防护**：前端自动转义用户输入
- **密码加密**：bcrypt 哈希存储
- **敏感信息加密**：配置文件中的密钥不提交版本库

---

## 📈 性能指标

### 生成性能

- **单章节生成时间**：15-30 秒（取决于 LLM API 响应）
- **完整材料生成**：5-10 分钟（10 个章节并发）
- **文档导出**：3-5 秒（Word）
- **并发处理能力**：3 个任务/同时（可配置）

### 系统性能

- **API 响应时间**：< 100ms（P95）
- **并发用户**：500+（4C8G 服务器）
- **数据库连接池**：20 个连接
- **Gunicorn Workers**：9 个进程

---

## 🛠️ 开发工具

### 代码质量

```bash
# Python 代码格式化
black app/
isort app/

# TypeScript 类型检查
cd frontend && pnpm run type-check

# 代码检查
flake8 app/
eslint src/
```

### 数据库管理

```bash
# 创建迁移
alembic revision --autogenerate -m "描述"

# 升级到最新版本
alembic upgrade head

# 查看当前版本
alembic current

# 回退一个版本
alembic downgrade -1
```

### 日志管理

```bash
# 查看实时日志
sudo journalctl -u miaozhu-backend -f

# 查看错误日志
sudo journalctl -u miaozhu-backend -p err

# 查看最近 100 行
sudo journalctl -u miaozhu-backend -n 100
```

---

## 📝 配置说明

### 环境变量

后端 `.env` 必需配置：

```bash
# 数据库（必需）
DATABASE_URL=mysql+asyncmy://user:pass@host:3306/miaozhu?charset=utf8mb4

# Redis（必需）
REDIS_URL=redis://localhost:6379/0

# JWT 密钥（必需，生产环境务必修改）
JWT_SECRET_KEY=your-random-secret-key

# DeepSeek API（必需）
DEEPSEEK_API_KEY=your-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

前端 `.env.development` 必需配置：

```bash
# API 地址（必需）
VITE_API_BASE_URL=http://localhost:8000/api/v1

# 签名密钥（必需，需与后端一致）
VITE_SIGN_SECRET_KEY=ruanzhu-client-secret-key
```

---

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系方式

- **项目地址**：[GitHub Repository]
- **问题反馈**：[Issues]
- **技术文档**：[docs/启动指南.md](docs/启动指南.md)

---

**最后更新**：2024-02-14
