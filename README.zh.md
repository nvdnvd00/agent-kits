<p align="center">
  <img src="./assets/logo.svg" width="200" alt="Agent Kits Logo" />
</p>

<h1 align="center">Agent Kits</h1>

<p align="center">
  <b>通用 AI 代理工具包</b><br/>
  <sub>适用于任何 AI 编程助手的技能、代理和工作流</sub>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@neyugn/agent-kits"><img src="https://img.shields.io/npm/v/@neyugn/agent-kits?style=flat-square&color=00ADD8" alt="npm version" /></a>
  <a href="https://www.npmjs.com/package/@neyugn/agent-kits"><img src="https://img.shields.io/npm/dm/@neyugn/agent-kits?style=flat-square&color=00ADD8" alt="npm downloads" /></a>
  <a href="https://github.com/nvdnvd00/agent-kits/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="license" /></a>
</p>

<p align="center">
  <a href="./README.md">English</a> •
  <a href="./README.vi.md">Tiếng Việt</a> •
  <b>中文</b>
</p>

<br/>

## ✨ 什么是 Agent Kits？

**Agent Kits** 是一个通用工具包，可以增强您的 AI 编程助手：

- 🤖 **专家代理** — 具有深度领域专业知识的预定义角色
- 🧩 **可复用技能** — 最佳实践和决策框架
- 📜 **工作流** — 常见任务的斜杠命令
- 🔍 **智能过滤** — 自动检测技术栈并优化加载的技能

适用于**任何 AI 工具** — Claude、Gemini、Codex、Cursor 等。

<br/>

## 🚀 快速开始

```bash
npx @neyugn/agent-kits@latest
```

就这样！交互式安装程序将引导您：

1. 选择您的 AI 工具（Claude、Gemini、Cursor 等）
2. 选择安装范围（Global 或 Workspace）
3. 选择要安装的工具包
4. 确认安装路径

### 🤖 代理激活协议

当您激活一个代理时，系统遵循 5 步协议：

```
1. 分类 intent → 选择代理
2. 宣布: 🤖 **@{agent} activated!**
3. 读取: .claude/agents/{agent}.md
4. 从 frontmatter 加载技能 → 读取 .claude/skills/{skill}/SKILL.md
5. 执行
```

**优先级:** DEBUG > CREATE > PLAN > QUESTION

<br/>

## 🖥️ CLI 命令

```bash
npx @neyugn/agent-kits              # 启动交互式安装向导
npx @neyugn/agent-kits --check-updates  # 检查新版本
npx @neyugn/agent-kits --version        # 显示当前版本
npx @neyugn/agent-kits --help           # 显示帮助
```

**有新版本时的输出示例：**

```
╭─────────────────────────╮
│  agent-kits v0.5.0     │
│  Latest:   v0.6.0      │
╰─────────────────────────╯

  ⚠ Update available! Run below to update:
  npx @neyugn/agent-kits@latest
```

<br/>

## 📌 重要说明

### IDE 下拉菜单中不显示斜杠命令

如果 `.agent/`（或 `.cursor/`、`.opencode/` 等）被添加到 `.gitignore` 中，某些 IDE 将跳过对其中文件的索引 — 包括为 `/plan`、`/debug`、`/create` 等斜杠命令提供支持的 `workflows/` 文件夹。

**解决方法：** 在 `.gitignore` 中添加否定规则来强制索引 workflows 文件夹：

```gitignore
# 忽略 kit 文件夹（可选）
.agent/

# 但始终索引 workflows，以便 IDE 中的斜杠命令正常工作
!.agent/workflows/
!.agent/workflows/**
```

> **推荐：** 将 kit 文件夹从 `.gitignore` 中完全移除并提交它。

<br/>

## ✨ 功能特性

### 🌍 Global vs Workspace 安装

| 模式         | 位置          | 使用场景     |
| ------------ | ------------- | ------------ |
| 📁 Workspace | `./{{tool}}/` | 项目特定配置 |
| 🌍 Global    | `~/{{tool}}/` | 所有项目共享 |

**各工具的 Global 路径：**

| 工具        | Global 路径  | Workspace 路径 |
| ----------- | ------------ | -------------- |
| Claude Code | `~/.claude/` | `.claude/`     |
| Gemini CLI  | `~/.gemini/` | `.gemini/`     |
| Codex CLI   | `~/.codex/`  | `.codex/`      |
| Antigravity | `~/.agent/`  | `.agent/`      |
| Cursor      | `~/.cursor/` | `.cursor/`     |

> **注意：** 在 Windows 上，`~` 会被替换为 `C:\Users\<用户名>\`

### 🔄 检测已存在的安装

如果安装程序检测到已存在的安装，您将看到以下选项：

- **🔄 替换**：删除现有安装，重新安装
- **🔀 合并**：保留配置文件，只更新技能
- **⏭️ 跳过**：保留现有，不安装
- **❌ 取消**：退出安装程序

### 🔌 通用兼容性

| 工具        | Workspace 路径    | Global 路径  | 状态        |
| ----------- | ----------------- | ------------ | ----------- |
| Antigravity | `.agent/skills/`  | `~/.agent/`  | ✅ 完全支持 |
| Cursor      | `.cursor/skills/` | `~/.cursor/` | ✅ 完全支持 |
| Claude Code | `.claude/skills/` | `~/.claude/` | ✅ 完全支持 |
| Gemini CLI  | `.gemini/skills/` | `~/.gemini/` | 🔜 即将推出 |
| Codex CLI   | `.codex/skills/`  | `~/.codex/`  | 🔜 即将推出 |

> **注意：** 标记为 🔜 即将推出的工具已纳入未来版本计划。基础架构已就绪，但这些工具需要额外的测试和配置。

### 💻 跨平台支持

支持 **Windows**、**macOS** 和 **Linux**，路径自动适配：

| 平台    | Global 路径示例              |
| ------- | ---------------------------- |
| Windows | `C:\Users\username\.claude\` |
| macOS   | `/Users/username/.claude/`   |
| Linux   | `/home/username/.claude/`    |

<br/>

## 🔍 智能过滤功能 (工作区分析)

**Filter** 功能是 Agent Kits 的 "大脑"，旨在确保您的 AI 助手始终保持敏锐和专注。系统会自动分析您的工作区，仅启用必要的技能，而不是让 AI 处理数十个无关的指令（技能）。

### 为什么需要过滤？

随着项目的复杂化，向 AI 提供过多的指令（系统提示词）会导致：
- **上下文膨胀 (Context Bloat)**：导致 AI 容易混淆且响应变慢。
- **注意力分散**：AI 可能会推荐一种框架的模式到另一种框架中（例如在正在使用 CSS Modules 的项目中推荐 Tailwind v4 模式）。
- **Token 浪费**：发送冗余指令会增加 API 使用成本。

### `/filter` 的工作机制

系统采用多层扫描机制来提供最佳建议：

1.  **技术栈检测**：扫描项目标识文件（`package.json`、`go.mod`、`requirements.txt`、`composer.json`、`Cargo.toml` 等）。
2.  **结构分析**：检查特征目录（如 Next.js App Router 的 `src/app`、移动端的 `android/` 等）。
3.  **代理与技能映射**：将检测到的技术栈与 Agent Kits 库进行对比，选出最相关的专家级代理 (Agents) 和核心能力 (Skills)。
4.  **配置文件优化**：创建或更新 `.agent/profile.json` 文件，精准配置 AI 可以访问的内容。

### 分析报告示例

```markdown
## 🔍 工作区分析：电商项目 (Next.js + NestJS)

**检测到的技术栈：**
- 前端：`Next.js 14`, `Tailwind CSS`, `Zustand`
- Backend: `NestJS`, `PostgreSQL`, `Prisma`
- 运维：`Docker`, `GitHub Actions`

**✅ 已启用的代理 (Specialists)：**
- `frontend-specialist`：针对 Next.js 和 Tailwind 进行了优化。
- `backend-specialist`：精通 NestJS 架构。
- `database-specialist`：支持 Prisma 查询优化。
- `devops-engineer`：管理 Docker 和 CI/CD 流程。

**🧩 已加载的技能：**
- `react-patterns`, `tailwind-patterns`, `nodejs-best-practices`, `postgres-patterns`, `docker-patterns`

**🚫 已隐藏的技能 (减少噪音)：**
- `flutter-patterns`, `mobile-design`, `aws-patterns` (本项目未使用)
```

### 控制命令

```bash
/filter                           # 重新扫描工作区并自动更新
/filter --force-enable ai-rag     # 强制启用 RAG 技能（无论技术栈如何）
/filter --force-disable mobile    # 强制禁用移动端相关技能
/filter --reset                   # 重置为初始状态（启用全部）
```

### 核心技能 (始终就绪)

某些基础技能和核心代理将永远不会被禁用，以确保系统级的逻辑思考能力：

| 技能 | 核心价值 |
| :--- | :--- |
| `clean-code` | 确保代码整洁且易于维护。 |
| `brainstorming` | 激活苏格拉底式思维以解决复杂问题。 |
| `plan-writing` | 在执行任何代码之前进行详细规划。 |
| `systematic-debugging` | 基于证据的 4 步骤系统化调试流程。 |
| `security-fundamentals` | 符合 OWASP 2025 标准的安全检查。 |

<br/>

## 📦 工具包

### 💻 Coder Kit（编程工具包）

完整的软件开发工具包，包含 **22 个专家代理**、**40 个技能** 和 **7 个工作流**。

<details>
<summary><b>🤖 代理 (22)</b></summary>

#### 第1层：主控代理

| 代理              | 描述         |
| ----------------- | ------------ |
| `orchestrator`    | 多代理协调   |
| `project-planner` | 智能项目规划 |
| `debugger`        | 系统化调试   |

#### 第2层：开发专家

| 代理                  | 描述                       |
| --------------------- | -------------------------- |
| `frontend-specialist` | React、Next.js、Vue、UI/UX |
| `backend-specialist`  | APIs、Node.js、Python      |
| `mobile-developer`    | React Native、Flutter      |
| `database-specialist` | 模式设计、查询             |
| `devops-engineer`     | CI/CD、部署                |

#### 第3层：质量与安全

| 代理                  | 描述                      |
| --------------------- | ------------------------- |
| `security-auditor`    | OWASP 2025、漏洞扫描      |
| `code-reviewer`       | PR 审查、代码质量         |
| `test-engineer`       | TDD、测试金字塔           |
| `performance-analyst` | Core Web Vitals、性能分析 |

#### 第4层：领域专家

| 代理                     | 描述                       |
| ------------------------ | -------------------------- |
| `realtime-specialist`    | WebSocket、Socket.IO       |
| `multi-tenant-architect` | 租户隔离、SaaS             |
| `queue-specialist`       | 消息队列、后台任务         |
| `integration-specialist` | 外部 API、webhooks         |
| `ai-engineer`            | LLM、RAG、AI/ML 系统       |
| `cloud-architect`        | AWS、Azure、GCP、Terraform |
| `data-engineer`          | ETL、数据管道、分析        |

#### 第5层：支持代理

| 代理                   | 描述               |
| ---------------------- | ------------------ |
| `documentation-writer` | 技术文档、API 文档 |
| `i18n-specialist`      | 国际化             |
| `ux-researcher`        | UX 研究、可用性    |

</details>

<details>
<summary><b>🧩 技能 (40)</b></summary>

**核心技能：**
| 技能 | 描述 |
| ----------------------- | ------------------------- |
| `clean-code` | 实用编码标准 |
| `api-patterns` | REST/GraphQL/tRPC 决策 |
| `database-design` | 模式设计、索引 |
| `testing-patterns` | 单元、集成、E2E 测试 |
| `security-fundamentals` | OWASP 2025、安全编码 |
| `performance-profiling` | Core Web Vitals、优化 |

**流程技能：**
| 技能 | 描述 |
| ----------------------- | ------------------------- |
| `brainstorming` | 苏格拉底式提问协议 |
| `plan-writing` | 任务分解、WBS |
| `systematic-debugging` | 4阶段调试 |

**领域技能 (31):** `react-patterns`、`typescript-patterns`、`docker-patterns`、`kubernetes-patterns`、`terraform-patterns`、`auth-patterns`、`graphql-patterns`、`redis-patterns`、`realtime-patterns`、`queue-patterns`、`multi-tenancy`、`ai-rag-patterns`、`prompt-engineering`、`monitoring-observability`、`frontend-design`、`mobile-design`、`tailwind-patterns`、`e2e-testing`、`github-actions`、`gitlab-ci-patterns`、`flutter-patterns`、`react-native-patterns`、`seo-patterns`、`accessibility-patterns`、`mermaid-diagrams`、`i18n-localization`、`postgres-patterns`、`nodejs-best-practices`、`documentation-templates`、`ui-ux-pro-max`、`aws-patterns`

</details>

<details>
<summary><b>📜 工作流 (7)</b></summary>

| 命令             | 描述                   |
| ---------------- | ---------------------- |
| `/plan`          | 创建项目计划（无代码） |
| `/create`        | 构建新应用             |
| `/debug`         | 系统化调试             |
| `/test`          | 生成和运行测试         |
| `/deploy`        | 生产部署               |
| `/orchestrate`   | 多代理协调             |
| `/ui-ux-pro-max` | UI/UX 设计智能         |

</details>

### 🔜 即将推出

| 工具包            | 描述               | 状态      |
| ----------------- | ------------------ | --------- |
| ✍️ **Writer**     | 内容创作、文案写作 | 🚧 开发中 |
| 🔬 **Researcher** | 研究、分析、综合   | 📋 计划中 |
| 🎨 **Designer**   | UI/UX 设计、品牌   | 📋 计划中 |

<br/>

## 🛠️ 使用方法

### 使用代理

使用 `@代理名` 引用代理：

```markdown
@backend-specialist 设计用户管理 API
@security-auditor 审查这段认证代码
@test-engineer 为支付服务编写测试
```

### 使用工作流

使用斜杠命令调用工作流：

```bash
/plan 新电商网站         # 创建项目计划
/create todo app        # 构建应用
/debug 登录不工作       # 修复 bug
/test user service      # 生成测试
/filter                 # 为工作区优化技能
```

<br/>

## 📚 文档

安装后，在您的项目中找到文档：

- **架构指南**: `<path>/ARCHITECTURE.md`
- **代理详情**: `<path>/agents/*.md`
- **技能指南**: `<path>/skills/*/SKILL.md`
- **工作流文档**: `<path>/workflows/*.md`
- **通用技能**: `common/COMMON.md`

<br/>

## 🤝 贡献

欢迎贡献！请查看我们的[贡献指南](CONTRIBUTING.md)，了解详细说明：

- 创建新工具包
- 添加代理和技能
- 提交 pull requests

<br/>

## 📄 许可证

MIT © [Neos](https://github.com/nvdnvd00)

---

<p align="center">
  <sub>为 AI 辅助开发社区倾心打造 ❤️</sub>
</p>
