<p align="center">
  <img src="./assets/logo.svg" width="200" alt="Agent Kits Logo" />
</p>

<h1 align="center">Agent Kits</h1>

<p align="center">
  <b>Bộ công cụ AI Agent phổ quát</b><br/>
  <sub>Skills, Agents, và Workflows cho mọi trợ lý AI lập trình</sub>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@neyugn/agent-kits"><img src="https://img.shields.io/npm/v/@neyugn/agent-kits?style=flat-square&color=00ADD8" alt="npm version" /></a>
  <a href="https://www.npmjs.com/package/@neyugn/agent-kits"><img src="https://img.shields.io/npm/dm/@neyugn/agent-kits?style=flat-square&color=00ADD8" alt="npm downloads" /></a>
  <a href="https://github.com/nvdnvd00/agent-kits/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="license" /></a>
</p>

<p align="center">
  <a href="./README.md">English</a> •
  <b>Tiếng Việt</b> •
  <a href="./README.zh.md">中文</a>
</p>

<br/>

## ✨ Agent Kits là gì?

**Agent Kits** là bộ công cụ phổ quát giúp nâng cấp trợ lý AI lập trình của bạn với:

- 🤖 **Agent Chuyên gia** — Các Agent được định nghĩa sẵn với chuyên môn sâu trong từng lĩnh vực
- 🧩 **Skills Tái sử dụng** — Best practices và các framework hỗ trợ ra quyết định
- 📜 **Workflows** — Các slash command cho công việc thường gặp
- 🔍 **Lọc Thông minh** — Tự động phát hiện techstack và tối ưu skills được load

Hoạt động với **mọi công cụ AI** — Claude, Gemini, Codex, Cursor, và nhiều hơn nữa.

<br/>

## 🚀 Bắt đầu nhanh

```bash
npx @neyugn/agent-kits
```

Đó là tất cả! Installer tương tác sẽ hướng dẫn bạn:

1. Chọn công cụ AI của bạn (Claude, Gemini, Cursor, etc.)
2. Chọn phạm vi cài đặt (Global hoặc Workspace)
3. Chọn kits cần cài đặt
4. Xác nhận đường dẫn cài đặt

<br/>

## ✨ Tính năng

### 🎯 Một lệnh, mọi công cụ

```bash
npx @neyugn/agent-kits
```

```
  ╭──────────────────────────────────────────────────────────────────────────╮
  │                                                                          │
  │        _     ____  _____  _   _  _____   _  __ ___  _____  ____          │
  │       / \   / ___|| ____|| \ | ||_   _| | |/ /|_ _||_   _|/ ___|         │
  │      / _ \ | |  _ |  _|  |  \| |  | |   | ' /  | |   | |  \___ \         │
  │     / ___ \| |_| || |___ | |\  |  | |   | . \  | |   | |   ___) |        │
  │    /_/   \_\\____||_____||_| \_|  |_|   |_|\_\|___|  |_|  |____/         │
  │                                                                          │
  │           ⚡  The Universal AI Agent Toolkit  ⚡                         │
  │                                                                          │
  ╰──────────────────────────────────────────────────────────────────────────╯

  SETUP WIZARD

◆  🤖 Bạn đang sử dụng công cụ AI nào?
│  ○ Claude Code (.claude/)
│  ● Gemini CLI (.gemini/)
│  ○ Cursor (.cursor/)
│  ○ Tùy chỉnh...

◆  📂 Bạn muốn cài đặt ở đâu?
│  ● Workspace (Dự án hiện tại)
│  ○ Global (Tất cả dự án)
```

### 🌍 Global vs Workspace

| Chế độ      | Vị trí        | Use Case                      |
| ----------- | ------------- | ----------------------------- |
| � Workspace | `./{{tool}}/` | Cấu hình riêng cho từng dự án |
| 🌍 Global   | `~/{{tool}}/` | Dùng chung cho tất cả dự án   |

**Đường dẫn Global theo công cụ:**

| Công cụ     | Đường dẫn Global | Đường dẫn Workspace |
| ----------- | ---------------- | ------------------- |
| Claude Code | `~/.claude/`     | `.claude/`          |
| Gemini CLI  | `~/.gemini/`     | `.gemini/`          |
| Codex CLI   | `~/.codex/`      | `.codex/`           |
| Antigravity | `~/.agent/`      | `.agent/`           |
| Cursor      | `~/.cursor/`     | `.cursor/`          |

> **Lưu ý:** Trên Windows, `~` được thay bằng `C:\Users\<username>\`

### 🔄 Phát hiện cài đặt có sẵn

Nếu installer phát hiện cài đặt đã tồn tại, bạn sẽ được hỏi:

- **🔄 Thay thế**: Xóa cũ và cài mới
- **🔀 Merge**: Giữ config, chỉ cập nhật skills
- **⏭️ Bỏ qua**: Giữ nguyên, không cài đặt
- **❌ Hủy**: Thoát installer

### 🔌 Tương thích phổ quát

| Công cụ     | Đường dẫn Workspace | Đường dẫn Global | Trạng thái     |
| ----------- | ------------------- | ---------------- | -------------- |
| Cursor      | `.cursor/skills/`   | `~/.cursor/`     | ✅ Đã xác nhận |
| Antigravity | `.agent/skills/`    | `~/.agent/`      | ✅ Đã xác nhận |
| Claude Code | `.claude/skills/`   | `~/.claude/`     | 🧪 Thực nghiệm |
| Gemini CLI  | `.gemini/skills/`   | `~/.gemini/`     | 🧪 Thực nghiệm |
| Codex CLI   | `.codex/skills/`    | `~/.codex/`      | 🧪 Thực nghiệm |
| Tùy chỉnh   | Có thể cấu hình     | `~/.ai/`         | 🧪 Thực nghiệm |

> **Lưu ý:** Các công cụ đánh dấu 🧪 Thực nghiệm chưa được kiểm tra đầy đủ và có thể cần người dùng tùy chỉnh thêm. Đóng góp và phản hồi luôn được hoan nghênh!

### 💻 Hỗ trợ đa nền tảng

Hoạt động trên **Windows**, **macOS**, và **Linux** với đường dẫn được tự động điều chỉnh:

| Nền tảng | Đường dẫn Global ví dụ       |
| -------- | ---------------------------- |
| Windows  | `C:\Users\username\.claude\` |
| macOS    | `/Users/username/.claude/`   |
| Linux    | `/home/username/.claude/`    |

<br/>

## 🔍 Filter Skill (Tính năng lọc Skills)

**Filter Skill** giải quyết vấn đề "quá tải skills" bằng cách tự động phát hiện techstack của dự án và chỉ bật các skills liên quan.

### Cách sử dụng

```bash
/filter
```

### Quy trình hoạt động

| Phase            | Mô tả                                                                     |
| ---------------- | ------------------------------------------------------------------------- |
| **1. Phát hiện** | Quét các file config (`package.json`, `pubspec.yaml`, `Dockerfile`, etc.) |
| **2. Đề xuất**   | Map techstack đã phát hiện với các skills cần thiết                       |
| **3. Xác nhận**  | Hiển thị thay đổi và hỏi về kế hoạch techstack tương lai                  |
| **4. Lưu trữ**   | Lưu profile vào `.agent/workspace-profile.json`                           |

### Ví dụ

```markdown
## 🔍 Phân tích Workspace hoàn tất

**Techstack đã phát hiện:**
| Danh mục | Công nghệ |
| --------- | ----------------------- |
| Ngôn ngữ | TypeScript |
| Framework | Next.js 14 (App Router) |
| Styling | Tailwind CSS v4 |
| Database | PostgreSQL (Prisma) |

**Skills cần BẬT:**
| Skill | Lý do |
| ----------------- | ------------------------ |
| react-patterns | Phát hiện Next.js |
| tailwind-patterns | Tìm thấy tailwind.config |
| postgres-patterns | Prisma + PostgreSQL |

**Skills cần TẮT:**
| Skill | Lý do |
| ---------------- | ---------------------------- |
| flutter-patterns | Không có pubspec.yaml |
| mobile-design | Không phát hiện setup mobile |

**Câu hỏi:**

1. Bạn có đồng ý với các thay đổi trên? (có/không/tùy chỉnh)
2. Có techstack nào bạn dự định thêm trong tương lai không?
```

### Các lệnh

```bash
/filter                           # Phân tích và lọc skills
/filter --force-enable ai-rag     # Bật cưỡng chế skill cụ thể
/filter --force-disable mobile    # Tắt cưỡng chế skill cụ thể
/filter --reset                   # Reset về mặc định (bật tất cả)
```

### Core Skills (Không bao giờ tắt)

Các skills này luôn được bật bất kể techstack:

| Skill                   | Mô tả                     |
| ----------------------- | ------------------------- |
| `clean-code`            | Tiêu chuẩn code thực dụng |
| `brainstorming`         | Phương pháp hỏi Socratic  |
| `plan-writing`          | Phân chia task và WBS     |
| `systematic-debugging`  | Debug 4 phase             |
| `testing-patterns`      | Testing pyramid patterns  |
| `security-fundamentals` | OWASP 2025 security       |

<br/>

## 📦 Các Kits

### 💻 Coder Kit

Bộ công cụ hoàn chỉnh cho phát triển phần mềm với **22 agent chuyên gia**, **40 skills**, và **7 workflows**.

<details>
<summary><b>🤖 Agents (22)</b></summary>

#### Tier 1: Master Agents

| Agent             | Mô tả                         |
| ----------------- | ----------------------------- |
| `orchestrator`    | Điều phối đa agent            |
| `project-planner` | Lập kế hoạch dự án thông minh |
| `debugger`        | Debug có hệ thống             |

#### Tier 2: Chuyên gia Phát triển

| Agent                 | Mô tả                      |
| --------------------- | -------------------------- |
| `frontend-specialist` | React, Next.js, Vue, UI/UX |
| `backend-specialist`  | APIs, Node.js, Python      |
| `mobile-developer`    | React Native, Flutter      |
| `database-specialist` | Thiết kế schema, queries   |
| `devops-engineer`     | CI/CD, deployment          |

#### Tier 3: Chất lượng & Bảo mật

| Agent                 | Mô tả                       |
| --------------------- | --------------------------- |
| `security-auditor`    | OWASP 2025, lỗ hổng bảo mật |
| `code-reviewer`       | Review PR, chất lượng code  |
| `test-engineer`       | TDD, testing pyramid        |
| `performance-analyst` | Core Web Vitals, profiling  |

#### Tier 4: Chuyên gia Domain

| Agent                    | Mô tả                           |
| ------------------------ | ------------------------------- |
| `realtime-specialist`    | WebSocket, Socket.IO            |
| `multi-tenant-architect` | Tenant isolation, SaaS          |
| `queue-specialist`       | Message queues, background jobs |
| `integration-specialist` | External APIs, webhooks         |
| `ai-engineer`            | LLM, RAG, AI/ML systems         |
| `cloud-architect`        | AWS, Azure, GCP, Terraform      |
| `data-engineer`          | ETL, pipelines, analytics       |

#### Tier 5: Agents Hỗ trợ

| Agent                  | Mô tả                       |
| ---------------------- | --------------------------- |
| `documentation-writer` | Tài liệu kỹ thuật, API docs |
| `i18n-specialist`      | Đa ngôn ngữ                 |
| `ux-researcher`        | Nghiên cứu UX, usability    |

</details>

<details>
<summary><b>🧩 Skills (40)</b></summary>

**Core Skills:**
| Skill | Mô tả |
| ----------------------- | ------------------------------ |
| `clean-code` | Tiêu chuẩn code thực dụng |
| `api-patterns` | Quyết định REST/GraphQL/tRPC |
| `database-design` | Thiết kế schema, indexing |
| `testing-patterns` | Unit, integration, E2E |
| `security-fundamentals` | OWASP 2025, secure coding |
| `performance-profiling` | Core Web Vitals, optimization |

**Process Skills:**
| Skill | Mô tả |
| ----------------------- | ------------------------------ |
| `brainstorming` | Phương pháp hỏi Socratic |
| `plan-writing` | Phân chia task, WBS |
| `systematic-debugging` | Debug 4 phase |

**Domain Skills (31):** `react-patterns`, `typescript-patterns`, `docker-patterns`, `kubernetes-patterns`, `terraform-patterns`, `auth-patterns`, `graphql-patterns`, `redis-patterns`, `realtime-patterns`, `queue-patterns`, `multi-tenancy`, `ai-rag-patterns`, `prompt-engineering`, `monitoring-observability`, `frontend-design`, `mobile-design`, `tailwind-patterns`, `e2e-testing`, `github-actions`, `gitlab-ci-patterns`, `flutter-patterns`, `react-native-patterns`, `seo-patterns`, `accessibility-patterns`, `mermaid-diagrams`, `i18n-localization`, `postgres-patterns`, `nodejs-best-practices`, `documentation-templates`, `ui-ux-pro-max`, `aws-patterns`

</details>

<details>
<summary><b>📜 Workflows (7)</b></summary>

| Lệnh             | Mô tả                           |
| ---------------- | ------------------------------- |
| `/plan`          | Tạo kế hoạch dự án (không code) |
| `/create`        | Build ứng dụng mới              |
| `/debug`         | Debug có hệ thống               |
| `/test`          | Tạo và chạy tests               |
| `/deploy`        | Deployment production           |
| `/orchestrate`   | Điều phối đa agent              |
| `/ui-ux-pro-max` | Thiết kế UI/UX thông minh       |

> **Lưu ý:** Lệnh `/filter` nằm trong **Common Skills Layer** (xem bên dưới) và có sẵn trong tất cả kits.

</details>

### 🔜 Sắp ra mắt

| Kit               | Mô tả                           | Trạng thái         |
| ----------------- | ------------------------------- | ------------------ |
| ✍️ **Writer**     | Sáng tạo nội dung, copywriting  | 🚧 Đang phát triển |
| 🔬 **Researcher** | Nghiên cứu, phân tích, tổng hợp | 📋 Kế hoạch        |
| 🎨 **Designer**   | Thiết kế UI/UX, branding        | 📋 Kế hoạch        |

<br/>

## 🛠️ Cách sử dụng

### Sử dụng Agents

Gọi agents với `@tên-agent`:

```markdown
@backend-specialist thiết kế API quản lý user
@security-auditor review code authentication này
@test-engineer viết tests cho payment service
```

### Sử dụng Workflows

Gọi workflows với slash commands:

```bash
/plan trang e-commerce mới       # Tạo kế hoạch dự án
/create todo app                 # Build ứng dụng
/debug login không hoạt động     # Sửa bugs
/test user service               # Tạo tests
/filter                          # Tối ưu skills cho workspace
```

<br/>

## 📚 Tài liệu

Sau khi cài đặt, tìm tài liệu trong dự án của bạn:

- **Hướng dẫn Kiến trúc**: `<path>/ARCHITECTURE.md`
- **Chi tiết Agents**: `<path>/agents/*.md`
- **Hướng dẫn Skills**: `<path>/skills/*/SKILL.md`
- **Tài liệu Workflows**: `<path>/workflows/*.md`
- **Common Skills**: `common/COMMON.md`

<br/>

## 🤝 Đóng góp

Chúng tôi hoan nghênh đóng góp! Xem [Hướng dẫn đóng góp](CONTRIBUTING.md) để biết chi tiết về:

- Tạo kits mới
- Thêm agents và skills
- Gửi pull requests

<br/>

## 📄 Giấy phép

MIT © [Neos](https://github.com/nvdnvd00)

---

<p align="center">
  <sub>Được xây dựng với ❤️ cho cộng đồng phát triển với AI</sub>
</p>
