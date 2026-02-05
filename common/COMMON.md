# Common Skills Layer

> Universal skills shared across ALL kits in @neyugn/agent-kits

---

## 🎯 Purpose

Common Skills là một layer đặc biệt chứa các skill được chia sẻ giữa **tất cả các kits**. Những skill này:

1. **Được cài đặt cùng với mọi kit** - Khi user cài một kit bất kỳ (coder, writer, etc.), common skills cũng được cài theo
2. **Được đề cập trong ARCHITECTURE.md** của mỗi kit
3. **Có workflow riêng** - Chỉ được gọi khi user sử dụng slash command tương ứng

---

## 📁 Directory Structure

```plaintext
common/
├── COMMON.md               # This file - documentation
├── skills/                 # Common skills
│   └── filter-skill/       # Workspace filtering skill
│       ├── SKILL.md
│       └── scripts/
│           └── workspace_analyzer.py
└── workflows/              # Common workflows
    └── filter.md           # /filter command
```

---

## 🧩 Common Skills

| Skill          | Description                                                                | Workflow  |
| -------------- | -------------------------------------------------------------------------- | --------- |
| `filter-skill` | Tự động phân tích workspace và bật/tắt skills/agents phù hợp với techstack | `/filter` |

---

## 🔄 How It Works

### Installation

Khi user chạy `npx @neyugn/agent-kits`:

1. User chọn kit (e.g., `coder`)
2. Installer copy kit vào workspace
3. Installer copy `common/` skills vào cùng vị trí
4. Common skills được merge vào architecture của kit

### Usage

```bash
# User gọi workflow để filter skills
/filter

# AI sẽ:
# 1. Phân tích workspace (package.json, pubspec.yaml, etc.)
# 2. Xác định techstack
# 3. Đề xuất enable/disable skills
# 4. Hỏi user xác nhận + techstack tương lai
# 5. Lưu kết quả vào .agent/workspace-profile.json
```

---

## 📊 Integration with Kits

Mỗi kit's `ARCHITECTURE.md` PHẢI đề cập:

```markdown
## 🔗 Common Skills

This kit inherits from the **Common Skills Layer**. See `common/COMMON.md` for:

- `/filter` - Workspace-aware skill filtering
- [Future common skills...]

Common skills are automatically installed and available in all kits.
```

---

## 🚀 Future Common Skills (Planned)

| Skill             | Description                                     | Status  |
| ----------------- | ----------------------------------------------- | ------- |
| `context-manager` | Quản lý context length, tự động tóm tắt history | Planned |
| `memory-skill`    | Lưu trữ và recall thông tin quan trọng          | Planned |
| `preference-sync` | Đồng bộ preferences của user giữa các sessions  | Planned |

---

## 📝 Adding Common Skills

1. Create skill folder in `common/skills/`
2. Create workflow in `common/workflows/`
3. Update this file's Skills table
4. Update all kits' ARCHITECTURE.md to reference

---
