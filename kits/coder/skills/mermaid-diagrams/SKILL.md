---
name: mermaid-diagrams
description: Mermaid diagram patterns for documentation. Create flowcharts, sequence diagrams, ERDs, and architecture diagrams. Use when visualizing systems, processes, or data relationships.
allowed-tools: Read, Write, Edit
version: 1.0
priority: LOW
---

# Mermaid Diagrams - Visual Documentation

> **Philosophy:** A good diagram is worth a thousand words. Keep it simple, readable, and purposeful.

---

## 🎯 Core Principles

| Principle       | Rule                                         |
| --------------- | -------------------------------------------- |
| **Clarity**     | One diagram, one concept                     |
| **Simplicity**  | Avoid overcrowding - less is more            |
| **Consistency** | Same styling and conventions across diagrams |
| **Purpose**     | Every element should serve understanding     |
| **Maintenance** | Easy to update as system evolves             |

---

## 📊 Diagram Types

| Type              | Best For                                |
| ----------------- | --------------------------------------- |
| `flowchart`       | Processes, decision trees, workflows    |
| `sequenceDiagram` | API calls, interactions, timing         |
| `classDiagram`    | Object relationships, inheritance       |
| `erDiagram`       | Database schemas, entity relationships  |
| `stateDiagram-v2` | State machines, lifecycle               |
| `gantt`           | Project timelines, milestones           |
| `pie`             | Proportions, distributions              |
| `gitGraph`        | Branch strategies, merges               |
| `journey`         | User experience flows                   |
| `C4Context`       | System architecture (with C4 extension) |

---

## 📈 Flowchart Patterns

### Basic Flowchart

```mermaid
flowchart TD
    A[Start] --> B{Is valid?}
    B -->|Yes| C[Process]
    B -->|No| D[Error]
    C --> E[End]
    D --> E
```

### Node Shapes

| Shape         | Syntax     | Use For             |
| ------------- | ---------- | ------------------- |
| Rectangle     | `[text]`   | Process, action     |
| Rounded       | `(text)`   | Start/end, terminal |
| Stadium       | `([text])` | Start/end (alt)     |
| Diamond       | `{text}`   | Decision            |
| Hexagon       | `{{text}}` | Preparation         |
| Parallelogram | `[/text/]` | Input/output        |
| Circle        | `((text))` | Connector           |
| Database      | `[(text)]` | Database            |

### Subgraphs for Organization

```mermaid
flowchart TB
    subgraph Frontend
        A[React App] --> B[API Client]
    end

    subgraph Backend
        C[API Server] --> D[(Database)]
    end

    B --> C
```

---

## 🔄 Sequence Diagram Patterns

### Basic API Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant D as Database

    C->>+A: POST /users
    A->>+D: INSERT user
    D-->>-A: user record
    A-->>-C: 201 Created
```

### Arrow Types

| Arrow   | Meaning                |
| ------- | ---------------------- |
| `->>`   | Solid with arrowhead   |
| `-->`   | Dotted with arrowhead  |
| `->>+`  | Activate lifeline      |
| `-->>-` | Deactivate lifeline    |
| `-x`    | Solid with X (failure) |
| `--x`   | Dotted with X          |

### Notes and Loops

```mermaid
sequenceDiagram
    participant U as User
    participant S as Server

    Note over U,S: Authentication Flow

    U->>S: Login request
    activate S

    loop Validate
        S->>S: Check credentials
    end

    alt Success
        S-->>U: JWT Token
    else Failure
        S-->>U: 401 Error
    end

    deactivate S
```

---

## 🗃️ ER Diagram Patterns

### Database Schema

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        uuid id PK
        string email UK
        string name
        timestamp created_at
    }

    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        uuid id PK
        uuid user_id FK
        decimal total
        string status
    }

    ORDER_ITEM }o--|| PRODUCT : references
    ORDER_ITEM {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
    }

    PRODUCT {
        uuid id PK
        string name
        decimal price
    }
```

### Relationship Symbols

| Symbol | Meaning      |
| ------ | ------------ | ----------- | ----------- |
| `      |              | `           | Exactly one |
| `o{`   | Zero or more |
| `      | {`           | One or more |
| `o     | `            | Zero or one |

---

## 🔀 State Diagram Patterns

### Lifecycle States

```mermaid
stateDiagram-v2
    [*] --> Draft

    Draft --> Pending: Submit
    Pending --> Approved: Approve
    Pending --> Rejected: Reject

    Approved --> Published: Publish
    Published --> Archived: Archive

    Rejected --> Draft: Revise
    Archived --> [*]

    note right of Pending
        Awaiting review
    end note
```

---

## 🎨 Styling

### Theme Options

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    A --> B
```

| Theme     | Best For                |
| --------- | ----------------------- |
| `default` | Light backgrounds       |
| `dark`    | Dark mode documentation |
| `forest`  | Calm, professional      |
| `neutral` | Minimal, clean          |

### Custom Styling

```mermaid
flowchart TD
    A[Critical]:::critical --> B[Normal]
    B --> C[Success]:::success

    classDef critical fill:#ff6b6b,stroke:#c92a2a,color:#fff
    classDef success fill:#51cf66,stroke:#2b8a3e,color:#fff
```

---

## 📋 Best Practices

### Do's

| Practice                | Why                              |
| ----------------------- | -------------------------------- |
| One concept per diagram | Clarity and focus                |
| Use descriptive labels  | Self-documenting                 |
| Consistent direction    | TD/LR - pick one and stick to it |
| Group with subgraphs    | Visual organization              |
| Use proper shapes       | Semantic meaning                 |

### Don'ts

| Anti-Pattern          | Problem                          |
| --------------------- | -------------------------------- |
| Too many nodes        | Overwhelming, hard to read       |
| Long text in nodes    | Cluttered diagram                |
| Crossing lines        | Confusing flow                   |
| Inconsistent styling  | Unprofessional look              |
| No legend when needed | Readers can't understand symbols |

---

## 🔧 Common Use Cases

### Architecture Decision

```mermaid
flowchart TD
    subgraph Options
        A[REST API] --> X{Choose}
        B[GraphQL] --> X
        C[gRPC] --> X
    end

    X -->|Web/Mobile| B
    X -->|Microservices| C
    X -->|Simple CRUD| A
```

### Deployment Flow

```mermaid
flowchart LR
    subgraph Development
        A[Code] --> B[PR]
    end

    subgraph CI/CD
        B --> C[Build]
        C --> D[Test]
        D --> E{Pass?}
    end

    subgraph Deploy
        E -->|Yes| F[Staging]
        F --> G[Production]
    end

    E -->|No| A
```

### User Journey

```mermaid
journey
    title User Signup Flow
    section Discovery
      Visit landing page: 5: User
      Read features: 4: User
    section Signup
      Click signup: 5: User
      Fill form: 3: User
      Verify email: 2: User
    section Onboarding
      Complete profile: 4: User
      Start using: 5: User
```

---

## ✅ Diagram Checklist

Before sharing a diagram:

- [ ] Single clear purpose
- [ ] All nodes have meaningful labels
- [ ] No unnecessary complexity
- [ ] Consistent styling
- [ ] Renders correctly in target platform
- [ ] Accessible (add description if needed)
- [ ] Source stored in version control

---

## 🔗 Related Skills

| Need                   | Skill                     |
| ---------------------- | ------------------------- |
| Architecture decisions | `architecture`            |
| Database design        | `database-design`         |
| API documentation      | `documentation-templates` |
| Project planning       | `plan-writing`            |

---

> **Remember:** The purpose of a diagram is to communicate. If it takes longer to understand the diagram than the concept it represents, simplify it.
