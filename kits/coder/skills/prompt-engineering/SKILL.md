---
name: prompt-engineering
description: Prompt engineering principles for AI systems. Use when writing system prompts, agent personas, optimizing AI interactions, or debugging agent behavior. Covers few-shot learning, chain-of-thought, template design, and best practices.
allowed-tools: Read, Write, Edit
version: 1.0
priority: CRITICAL
---

# Prompt Engineering - AI Communication Excellence

> **Philosophy:** Prompts are code. They should be **specific, structured, and testable**. Vague prompts produce vague results.

---

## Core Principles

| Principle      | Rule                                               |
| -------------- | -------------------------------------------------- |
| **Specific**   | Ambiguity causes inconsistent outputs              |
| **Structured** | Clear sections: Context → Task → Format → Examples |
| **Testable**   | Evaluate on diverse inputs, measure consistency    |
| **Iterative**  | Start simple, add complexity only when needed      |
| **Versioned**  | Treat prompts as code with proper version control  |

---

## Prompt Structure

### Universal Template

```
[ROLE/PERSONA]     → Who the AI should be
[CONTEXT]          → Background information
[TASK]             → What to do
[CONSTRAINTS]      → Rules and boundaries
[FORMAT]           → Expected output structure
[EXAMPLES]         → Input-output demonstrations
```

### System Prompt Example

```markdown
# Role

You are a senior backend engineer specializing in API design.

# Rules

- Always consider scalability and performance
- Suggest RESTful patterns by default
- Flag security concerns immediately
- Use early return pattern in code

# Output Format

1. Analysis
2. Recommendation
3. Code example
4. Trade-offs
```

---

## Key Techniques

### 1. Few-Shot Learning

| When to Use                | Examples Needed    |
| -------------------------- | ------------------ |
| Consistent formatting      | 2-3 examples       |
| Complex reasoning patterns | 3-5 examples       |
| Edge case handling         | Include edge cases |
| Simple tasks               | 0-1 examples       |

```markdown
Extract key information:

Input: "Login error 403, can't access dashboard"
Output: {"issue": "auth", "code": 403, "priority": "high"}

Input: "Feature request: add dark mode"
Output: {"issue": "feature", "code": null, "priority": "low"}

Now process: "Can't upload files, timeout after 10s"
```

### 2. Chain-of-Thought (CoT)

Force step-by-step reasoning for complex problems:

```markdown
Analyze this bug report.

Think step by step:

1. What is the expected behavior?
2. What is the actual behavior?
3. What changed recently?
4. What components are involved?
5. What is the most likely root cause?

Bug: "Users can't save drafts after cache update"
```

| CoT Type       | Trigger                    | Accuracy Boost |
| -------------- | -------------------------- | -------------- |
| **Zero-shot**  | "Let's think step by step" | +10-20%        |
| **Few-shot**   | Show reasoning examples    | +30-50%        |
| **Self-check** | "Verify your reasoning"    | +10-15%        |

### 3. Progressive Disclosure

Start simple, add complexity only when needed:

| Level | Prompt                                        | Use When         |
| ----- | --------------------------------------------- | ---------------- |
| 1     | "Summarize this article"                      | Testing baseline |
| 2     | "Summarize in 3 bullet points"                | Need structure   |
| 3     | "Identify main findings, then summarize each" | Need reasoning   |
| 4     | Include 2-3 example summaries                 | Need consistency |

---

## Agent Prompt Patterns

### Persona Definition

```markdown
# Identity

You are [ROLE] with expertise in [DOMAIN].

# Philosophy

> "[CORE BELIEF]"

# Behavioral Traits

- [Trait 1]
- [Trait 2]
- [Trait 3]

# Anti-Patterns (What NOT to do)

- ❌ [Bad behavior 1]
- ❌ [Bad behavior 2]
```

### Decision Framework

```markdown
When [SITUATION]:

1. First, check [CONDITION_1]
2. If true → [ACTION_1]
3. If false → Check [CONDITION_2]
4. Default → [FALLBACK_ACTION]
```

### Error Recovery

```markdown
If uncertain:

- Request clarification with specific questions
- Provide confidence score (1-10)
- Offer alternative interpretations
- Indicate missing information clearly
```

---

## Optimization Techniques

| Technique             | Purpose                 | Example                       |
| --------------------- | ----------------------- | ----------------------------- |
| **Constraints**       | Limit output scope      | "Max 100 words"               |
| **Format specs**      | Ensure parseable output | "Respond in JSON"             |
| **Role priming**      | Set expertise level     | "As a senior engineer..."     |
| **Negative examples** | What NOT to do          | "Do NOT include explanations" |
| **Confidence scores** | Measure certainty       | "Rate your confidence 1-10"   |

### Token Efficiency

| Inefficient                        | Efficient                        |
| ---------------------------------- | -------------------------------- |
| Long verbose instructions          | Concise, direct commands         |
| Repeating context in every message | System prompt for stable context |
| 10 examples when 3 suffice         | Minimal effective examples       |

---

## Decision Trees

### When to Use Few-Shot?

```
Is output format critical?
├── Yes → Add 2-3 format examples
└── No → Is task complex?
    ├── Yes → Add reasoning examples
    └── No → Zero-shot often sufficient
```

### How Many Examples?

```
Task complexity?
├── Simple formatting → 2 examples
├── Complex reasoning → 3-5 examples
└── Novel task → Start with 5, reduce if consistent
```

---

## Anti-Patterns (DON'T)

| ❌ Anti-Pattern                | ✅ Correct Approach               |
| ------------------------------ | --------------------------------- |
| Vague instructions             | Specific, measurable requirements |
| Complex prompt from start      | Start simple, iterate             |
| Examples that don't match task | Representative, diverse examples  |
| No output format specified     | Clear format expectations         |
| Ignoring edge cases            | Test on boundary inputs           |
| Same prompt for all tasks      | Task-specific optimized prompts   |
| No version control             | Git-track prompts like code       |

---

## Testing Prompts

| Test Type       | Purpose                  | Method                          |
| --------------- | ------------------------ | ------------------------------- |
| **Consistency** | Same input → same output | Run 5x, check variance          |
| **Edge cases**  | Handle unusual inputs    | Test empty, long, special chars |
| **Adversarial** | Resist manipulation      | Test injection attempts         |
| **Performance** | Speed and token usage    | Measure latency, token count    |

### Prompt Evaluation Checklist

```
□ Clear role/persona defined?
□ Task instructions specific?
□ Output format specified?
□ Constraints explicit?
□ Examples representative?
□ Edge cases handled?
□ Error recovery defined?
```

---

## 🔴 Self-Check Before Completing

| Check                  | Question                           |
| ---------------------- | ---------------------------------- |
| ✅ **Specific?**       | No ambiguous instructions?         |
| ✅ **Structured?**     | Role → Task → Format → Examples?   |
| ✅ **Tested?**         | Evaluated on diverse inputs?       |
| ✅ **Versioned?**      | Prompt tracked in version control? |
| ✅ **Optimized?**      | Minimal tokens, maximum clarity?   |
| ✅ **Error handling?** | Handles uncertain/edge cases?      |

---

## Related Skills

| Need                    | Skill                    |
| ----------------------- | ------------------------ |
| Agent design            | `agent-creator` (future) |
| Skill creation          | `skill-creator` (future) |
| AI application patterns | `ai-patterns` (future)   |
| User communication      | `brainstorming`          |

---

> **Remember:** A well-crafted prompt is invisible - the AI just does what you need without confusion. If you're constantly rephrasing or clarifying, the prompt needs work.
