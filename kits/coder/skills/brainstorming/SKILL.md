---
name: brainstorming
description: Socratic questioning protocol and user communication. Use for complex requests, new features, unclear requirements, or when deep understanding is needed before implementation. Includes progress reporting and error handling patterns.
allowed-tools: Read, Write, Edit
---

# Brainstorming - Socratic Discovery Protocol

> **Philosophy:** Understanding precedes implementation. Ask first, build second.

---

## 🎯 Core Principle: Never Assume

```
❌ WRONG: User says "add login" → Start coding auth flow
✅ CORRECT: User says "add login" → Ask about auth provider, user types, session needs
```

**The Socratic Approach:**

- Guide through questions, don't dictate solutions
- Surface hidden assumptions
- Challenge unclear requirements
- Explore edge cases before they become bugs

---

## 🚦 When to Apply Socratic Gate

### Decision Matrix

| Request Type    | Clarity Level | Action                          |
| --------------- | ------------- | ------------------------------- |
| **New Feature** | Any           | ASK 3+ strategic questions      |
| **Code Edit**   | Clear         | Confirm understanding, proceed  |
| **Code Edit**   | Vague         | Ask impact questions first      |
| **Bug Fix**     | Reproducible  | Investigate, minimal questions  |
| **Bug Fix**     | Unclear       | Ask for reproduction steps      |
| **Refactor**    | Any           | Ask about scope and constraints |

### Question Triggers

**Always ask questions when:**

- User says "build", "create", "implement", "add feature"
- Multiple valid interpretations exist
- Request involves architecture decisions
- Request affects multiple components
- Trade-offs are not explicit

**Skip questions when:**

- User says "just fix this specific thing"
- Request is purely mechanical (rename, format)
- Context is already established in conversation
- User explicitly says "don't ask, just do it"

---

## 🔑 Question Categories

### 1. Purpose & Goal Questions

**Uncover the "why":**

```markdown
- What problem does this solve for users?
- What's the expected outcome when this works?
- How will we know this feature is successful?
- Is this for a specific user segment or all users?
```

### 2. Scope & Boundary Questions

**Define the "what":**

```markdown
- What specifically should this include?
- What explicitly should this NOT include?
- Are there any time/budget constraints?
- Is this a complete solution or MVP first?
- What's the priority order if we can't do everything?
```

### 3. Context & Integration Questions

**Understand the "where":**

```markdown
- How does this fit with existing features?
- Are there similar patterns already in the codebase?
- What systems does this need to integrate with?
- Are there dependencies we should be aware of?
```

### 4. Edge Case & Failure Questions

**Anticipate the "what if":**

```markdown
- What happens if [X condition] occurs?
- How should we handle errors in this flow?
- What's the expected behavior for edge cases?
- Should we handle [unlikely but possible scenario]?
```

### 5. Trade-off Questions

**Clarify the "how much":**

```markdown
- Performance vs code simplicity—which matters more here?
- Should we build for scale now or optimize for speed to market?
- Complete solution now or iterative enhancement?
- Custom implementation or use existing library?
```

---

## 📋 Question Templates by Scenario

### New Feature Request

```markdown
Great, I want to make sure I build exactly what you need.

**Understanding the goal:**

1. What user problem does this solve?
2. How will users discover/access this feature?

**Scope check:** 3. What's the minimum version that would be useful? 4. Are there any "nice-to-haves" vs "must-haves"?

**Technical clarification:** 5. Any performance requirements (response time, data volume)? 6. Any security considerations (auth, data sensitivity)?
```

### Bug Fix Request

```markdown
Before I investigate:

1. Can you describe the expected vs actual behavior?
2. Is this reproducible? What steps trigger it?
3. When did this start happening? (recent change?)
4. Does it affect all users or specific conditions?
5. What's the severity/urgency?
```

### Refactoring Request

```markdown
To refactor effectively:

1. What's the main goal? (Readability? Performance? Testability?)
2. What's the scope boundary? (This file? This module? Entire feature?)
3. Are there hidden consumers of this code we need to consider?
4. Do we have test coverage to validate the refactor?
5. Any patterns we should align with from other parts of the codebase?
```

### Architecture Decision

```markdown
This is an important decision. Let's explore:

**Current State:**

1. What's driving this architecture change?
2. What problems exist with the current approach?

**Future State:** 3. What are the key requirements for the new design? 4. What trade-offs are acceptable?

**Constraints:** 5. Any technology restrictions or preferences? 6. Timeline or resource constraints?

**Risks:** 7. What could go wrong with this change? 8. What's our rollback strategy?
```

---

## 💬 Communication Patterns

### Progress Reporting

**For long tasks, report periodically:**

```markdown
🔄 **Progress Update:**

**Completed:**

- ✅ Created user authentication module
- ✅ Added database schema

**In Progress:**

- 🔄 Implementing password reset flow

**Remaining:**

- ⏳ Email notification integration
- ⏳ Testing and documentation

**Estimated completion:** ~2 more steps
```

### Clarification Requests

**When genuinely unclear:**

```markdown
🤔 **Quick clarification needed:**

I want to proceed correctly, but I'm unsure about [specific thing].

**Option A:** [Description] — Better for [use case]
**Option B:** [Description] — Better for [use case]

Which approach fits your needs?
```

### Error Handling Communication

**When something goes wrong:**

```markdown
⚠️ **Issue Encountered:**

**What happened:** [Brief description]

**Why it happened:** [Root cause if known]

**Options to proceed:**

1. [Option with trade-off]
2. [Different approach]
3. [Need more info on X]

What would you like to do?
```

### Confirmation Before Risky Actions

**Before destructive or irreversible actions:**

```markdown
🛡️ **Confirmation Required:**

I'm about to: [Describe action]

**This will:**

- [Effect 1]
- [Effect 2]

**This is irreversible / can be undone by [method]**

Proceed? (yes/no)
```

---

## 🔄 Iterative Discovery Pattern

### When user provides spec-heavy answers

```
User provides detailed spec →
  ↓
Still ask 2-3 "Edge Case" questions:
  - "What if [unlikely scenario]?"
  - "Should we handle [error condition]?"
  - "Is there a fallback for [dependency failure]?"
  ↓
Surface hidden assumptions before implementation
```

### Converging on Solution

```
1. Ask broad questions (Purpose, Scope)
2. Ask specific questions (Technical details)
3. Summarize understanding
4. Propose approach
5. Get confirmation
6. Begin implementation
```

---

## 🚨 Anti-Patterns

| ❌ Don't                        | ✅ Do                                                |
| ------------------------------- | ---------------------------------------------------- |
| Ask 10+ questions at once       | Group into 3-5 most important                        |
| Ask obvious questions           | Ask where there's genuine ambiguity                  |
| Re-ask answered questions       | Read conversation context                            |
| Block on every detail           | Make reasonable default assumptions for minor things |
| Question simple requests        | Apply judgment on when questions add value           |
| Ask then ignore answers         | Incorporate answers into your approach               |
| Pretend to understand           | Admit confusion and ask for clarity                  |
| Assume user knows best approach | Offer expert guidance with questions                 |

---

## 📋 Socratic Gate Checklist

Before major implementation:

```markdown
## Pre-Implementation Review

### Understanding (Must be clear)

- [ ] I understand the user's goal
- [ ] I understand the scope boundaries
- [ ] I have asked about edge cases

### Assumptions (Must be validated)

- [ ] Technical assumptions stated and confirmed
- [ ] Default behaviors agreed upon
- [ ] Error handling approach confirmed

### Risks (Must be acknowledged)

- [ ] Breaking changes identified
- [ ] Dependencies mapped
- [ ] Rollback strategy exists

### Ready to proceed?

- [ ] User has confirmed approach
- [ ] No critical questions remaining
```

---

## 📊 Question Quality Metrics

**Good questions are:**

- **Specific** — Not vague or overly broad
- **Actionable** — Answer directly informs implementation
- **Prioritized** — Most important first
- **Non-redundant** — Not already known from context

**Question effectiveness:**

| Question Type | When Valuable                       |
| ------------- | ----------------------------------- |
| Clarifying    | When terms are ambiguous            |
| Probing       | When surface answer is insufficient |
| Hypothetical  | When exploring edge cases           |
| Comparative   | When choosing between options       |
| Reflective    | When validating understanding       |

---

## 🔗 Related Skills

| Need                         | Skill                  |
| ---------------------------- | ---------------------- |
| Writing implementation plans | `plan-writing`         |
| Debugging with questions     | `systematic-debugging` |
| Clean code standards         | `clean-code`           |

---

> **Remember:** The cost of asking one more question is minutes. The cost of building the wrong thing is days or weeks.
