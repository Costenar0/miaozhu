<template>
  <div class="docs-page">
    <el-card shadow="never" class="docs-card">
      <div class="markdown-body" v-html="htmlContent"></div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { marked } from 'marked'

const htmlContent = ref('')

const markdown = `
## 功能特性

- **AI 智能生成**：基于软件信息自动生成操作说明书、源程序代码、数据库设计等材料
- **多格式导出**：支持 Word、PDF 格式导出，支持打包下载
- **实时进度**：SSE 实时推送生成进度，章节级别的状态跟踪
- **在线编辑**：生成结果支持在线 Markdown 编辑和实时预览
- **章节重新生成**：对不满意的章节可单独重新生成
- **图表生成**：可选生成流程图、ER 图等 Mermaid 图表
- **额外指令**：支持自定义生成指令，控制生成内容的方向和风格
- **通用 LLM**：兼容任何 OpenAI API 格式的大语言模型
- **开箱即用**：SQLite 嵌入式数据库，无需安装 MySQL/Redis，启动即用

---

## 使用指南

### 基本流程

1. **新建申请**：在「软著申请」页面点击新建，填写软件名称、简称、主要功能等基本信息
2. **完善信息**（可选）：补充开发语言、运行环境、权利信息、申请人信息等
3. **AI 生成**：点击生成按钮，AI 会自动生成以下材料：
   - 操作说明书（包含多个章节：软件概述、安装部署、功能模块详细说明等）
   - 源程序代码（前 30 页 + 后 30 页格式）
   - 数据库设计文档（可选）
4. **在线编辑**：对生成结果不满意的章节，可以直接在线编辑 Markdown 内容
5. **章节重新生成**：也可以对单个章节提交重新生成，支持附加额外指令引导 AI
6. **导出下载**：生成完成后，支持导出为 Word 或 PDF 格式

### 生成选项

新建申请时可以选择：

- **生成源程序代码**：默认开启，生成符合软著申请要求的源代码材料
- **生成数据库设计**：默认开启，生成数据库表结构和 ER 图
- **生成图表**：可选开启，在操作说明书中嵌入 Mermaid 流程图和架构图

### 额外指令

在生成时可以填写「额外指令」来引导 AI 的生成方向，例如：

- "使用 Java Spring Boot 框架风格"
- "源代码使用 Python，包含完整的错误处理"
- "操作说明书中着重描述数据分析和报表功能"

### 导出格式

| 格式 | 说明 |
|------|------|
| 文档鉴别材料 (Word/PDF) | 操作说明书，含目录、页眉页脚 |
| 源程序鉴别材料 (Word/PDF) | 源代码前后各 30 页 |
| 全部材料 (ZIP) | 打包下载以上所有格式 |

### 状态流转

申请的完整状态流：

\`\`\`
草稿 → 生成中 → 已生成 → 准备提交 → 已提交 → 已通过
                  ↘ 返回编辑       ↘ 返回审核    ↘ 已驳回 → 重新修改
                                                          → 归档
\`\`\`

---

## 配置说明

所有配置通过 \`backend/.env\` 文件管理：

### LLM 配置（必填）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| \`LLM_BASE_URL\` | OpenAI 兼容 API 地址 | \`https://api.openai.com/v1\` |
| \`LLM_API_KEY\` | API 密钥 | （无） |
| \`LLM_MODEL\` | 模型名称 | \`gpt-4o\` |

### 可选配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| \`CORS_ORIGINS\` | 允许的前端域名（JSON 数组） | \`["http://localhost:5173"]\` |
| \`DATABASE_URL\` | 数据库连接地址 | \`sqlite+aiosqlite:///data/miaozhu.db\` |
| \`EXPORT_DATA_DIR\` | 导出文件存储目录 | \`data/exports\` |
| \`SCHEDULER_POLL_INTERVAL\` | 调度器轮询间隔（秒） | \`5\` |
| \`SCHEDULER_MAX_CONCURRENT_LLM\` | 最大并发 LLM 调用数 | \`5\` |
| \`SCHEDULER_MAX_CONCURRENT_EXPORT\` | 最大并发导出任务数 | \`4\` |

### LLM 模型选择

项目使用通用的 OpenAI Chat Completions 兼容接口，支持任何提供该格式 API 的服务商和模型。

**模型要求**：生成软著材料涉及长篇中文文档和代码，建议选择中文能力强、支持长输出的模型。小参数量模型（7B 以下）可能生成质量不足。

#### OpenAI

| 模型 | 说明 |
|------|------|
| \`gpt-4o\` | 推荐，综合能力强，性价比高 |
| \`gpt-4o-mini\` | 更便宜，速度更快，质量略低 |
| \`o3-mini\` | 推理模型，适合复杂逻辑但速度较慢 |

\`\`\`bash
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-your-api-key
LLM_MODEL=gpt-4o
\`\`\`

#### DeepSeek

| 模型 | 说明 |
|------|------|
| \`deepseek-chat\` | 推荐，中文和代码能力优秀，价格低 |
| \`deepseek-reasoner\` | 推理模型，适合复杂场景 |

\`\`\`bash
LLM_BASE_URL=https://api.deepseek.com
LLM_API_KEY=sk-your-api-key
LLM_MODEL=deepseek-chat
\`\`\`

#### 通义千问（阿里云）

| 模型 | 说明 |
|------|------|
| \`qwen-plus\` | 推荐，均衡之选 |
| \`qwen-turbo\` | 更快更便宜，适合对质量要求不高的场景 |
| \`qwen-max\` | 最强能力，价格较高 |

\`\`\`bash
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_API_KEY=sk-your-api-key
LLM_MODEL=qwen-plus
\`\`\`

#### 智谱 GLM（智谱 AI）

| 模型 | 说明 |
|------|------|
| \`glm-4-plus\` | 推荐，中文能力强 |
| \`glm-4-flash\` | 免费额度大，速度快 |

\`\`\`bash
LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
LLM_API_KEY=your-api-key
LLM_MODEL=glm-4-plus
\`\`\`

#### 月之暗面 Kimi

| 模型 | 说明 |
|------|------|
| \`moonshot-v1-8k\` | 标准版 |
| \`moonshot-v1-32k\` | 长上下文 |

\`\`\`bash
LLM_BASE_URL=https://api.moonshot.cn/v1
LLM_API_KEY=sk-your-api-key
LLM_MODEL=moonshot-v1-8k
\`\`\`

#### 百度文心一言

| 模型 | 说明 |
|------|------|
| \`ernie-4.0-8k\` | 旗舰模型 |
| \`ernie-3.5-8k\` | 性价比之选 |

\`\`\`bash
LLM_BASE_URL=https://qianfan.baidubce.com/v2
LLM_API_KEY=your-api-key
LLM_MODEL=ernie-4.0-8k
\`\`\`

#### 本地部署（Ollama）

适合对数据隐私有要求、不想调用云端 API 的场景。建议 14B 及以上参数量的模型。

| 模型 | 说明 |
|------|------|
| \`qwen2.5:14b\` | 推荐，中文能力好 |
| \`qwen2.5:32b\` | 更强，需要较大显存 |
| \`deepseek-v2:16b\` | 代码能力突出 |

\`\`\`bash
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=qwen2.5:14b
\`\`\`

> Ollama 安装后运行 \`ollama pull qwen2.5:14b\` 即可下载模型。

#### 其他兼容服务

任何提供 OpenAI Chat Completions 格式（\`POST /v1/chat/completions\`）的服务均可接入，包括 vLLM、LocalAI、LiteLLM、OpenRouter、硅基流动（SiliconFlow）等。只需正确填写 \`LLM_BASE_URL\`、\`LLM_API_KEY\`、\`LLM_MODEL\` 三项即可。

---

## 常见问题

**Q: 生成速度慢？**

生成速度取决于 LLM API 的响应速度。一个完整的软著材料包含十多个章节，每个章节需要一次 LLM 调用。可以通过调整 \`SCHEDULER_MAX_CONCURRENT_LLM\` 增加并发数来加速（默认 5）。

**Q: 导出 PDF 失败？**

PDF 导出依赖 Playwright 浏览器引擎。请确保已运行 \`playwright install chromium\`。在服务器上可能需要额外安装系统依赖：\`playwright install --with-deps chromium\`。

**Q: 如何更换 LLM 模型？**

修改 \`.env\` 中的 \`LLM_BASE_URL\`、\`LLM_API_KEY\`、\`LLM_MODEL\` 三项即可，无需重启服务（下次生成任务会使用新配置）。支持任何兼容 OpenAI Chat Completions API 的服务。

**Q: 数据库文件越来越大？**

可以定期清理旧的导出文件：\`rm -rf backend/data/exports/*\`。如果数据库本身过大，可以用 \`sqlite3 backend/data/miaozhu.db "VACUUM;"\` 压缩。
`

onMounted(() => {
  htmlContent.value = marked.parse(markdown) as string
})
</script>

<style scoped lang="scss">
.docs-page {
  max-width: 900px;
}

.docs-card {
  border-radius: 8px;
}

:deep(.markdown-body) {
  color: #303133;
  font-size: 14px;
  line-height: 1.8;

  h2 {
    margin: 32px 0 16px;
    padding-bottom: 8px;
    font-size: 20px;
    border-bottom: 1px solid #ebeef5;

    &:first-child {
      margin-top: 0;
    }
  }

  h3 {
    margin: 24px 0 12px;
    font-size: 16px;
  }

  h4 {
    margin: 20px 0 8px;
    font-size: 15px;
  }

  p {
    margin: 8px 0;
  }

  ul, ol {
    padding-left: 24px;
    margin: 8px 0;
  }

  li {
    margin: 4px 0;
  }

  code {
    background: #f5f7fa;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 13px;
    color: #c7254e;
  }

  pre {
    background: #f5f7fa;
    border-radius: 6px;
    padding: 14px 18px;
    overflow-x: auto;
    margin: 12px 0;

    code {
      background: none;
      padding: 0;
      color: #303133;
    }
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;

    th, td {
      border: 1px solid #ebeef5;
      padding: 8px 12px;
      text-align: left;
      font-size: 13px;
    }

    th {
      background: #f5f7fa;
      font-weight: 600;
    }
  }

  blockquote {
    margin: 12px 0;
    padding: 8px 16px;
    border-left: 4px solid #409eff;
    background: #f4f8ff;
    color: #606266;

    p {
      margin: 0;
    }
  }

  hr {
    border: none;
    border-top: 1px solid #ebeef5;
    margin: 24px 0;
  }

  strong {
    color: #303133;
  }
}
</style>
