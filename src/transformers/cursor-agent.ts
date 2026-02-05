import type {
  AgentKitsFrontmatter,
  AgentTransformer,
  CursorSubagentFrontmatter,
  TransformContext,
} from "./types.js";
import {
  combineMarkdown,
  parseFrontmatter,
  serializeFrontmatter,
} from "./utils.js";

/**
 * Transformer for converting Agent-Kits agents to Cursor subagent format
 *
 * Key transformations:
 * 1. Remove `tools`, `skills`, `tier` from frontmatter
 * 2. Add `readonly: false` and `is_background: false`
 * 3. Embed skills as a "Required Skills" section in the body
 *
 * Skill descriptions are loaded dynamically from SKILL.md files via context.skillDescriptions
 */
export class CursorAgentTransformer implements AgentTransformer {
  /**
   * Transform agent content from Agent-Kits format to Cursor subagent format
   */
  transform(content: string, context: TransformContext): string {
    const parsed = parseFrontmatter(content);
    const originalData = parsed.data as unknown as AgentKitsFrontmatter;

    // Extract skills before removing
    const skillsString = originalData.skills;
    const skills = skillsString
      ? skillsString.split(",").map((s) => s.trim())
      : [];

    // Create new Cursor subagent frontmatter
    const cursorFrontmatter: CursorSubagentFrontmatter = {
      name: originalData.name,
      description: originalData.description,
      model: originalData.model || "inherit",
      readonly: false,
      is_background: false,
    };

    // Serialize new frontmatter
    const newFrontmatter = serializeFrontmatter(
      cursorFrontmatter as unknown as Record<string, unknown>,
    );

    // Create skills section if skills exist
    let skillsSection = "";
    if (skills.length > 0) {
      skillsSection = this.createSkillsSection(
        skills,
        context.skillDescriptions || {},
      );
    }

    // Find the first heading in the body to insert skills section after it
    const bodyContent = parsed.content;
    const insertedBody = this.insertSkillsSection(bodyContent, skillsSection);

    return combineMarkdown(newFrontmatter, insertedBody);
  }

  /**
   * Create markdown section for required skills
   * Uses descriptions from context (loaded from SKILL.md files)
   */
  private createSkillsSection(
    skills: string[],
    skillDescriptions: Record<string, string>,
  ): string {
    const lines = [
      "",
      "## 📚 Required Skills",
      "",
      "This agent uses the following skills from `.cursor/skills/`:",
      "",
    ];

    for (const skill of skills) {
      const description =
        skillDescriptions[skill] || "Domain-specific knowledge module";
      lines.push(`- **${skill}** - ${description}`);
    }

    lines.push("", "---", "");

    return lines.join("\n");
  }

  /**
   * Insert skills section after the first heading
   */
  private insertSkillsSection(body: string, skillsSection: string): string {
    if (!skillsSection) return body;

    // Find the first heading and the line after it
    const lines = body.split("\n");
    let insertIndex = 0;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      // Find first H1 heading (# Title)
      if (line.startsWith("# ")) {
        // Insert after the heading line
        insertIndex = i + 1;
        // Skip any empty lines after heading
        while (insertIndex < lines.length && lines[insertIndex].trim() === "") {
          insertIndex++;
        }
        // Also skip description line if it exists (non-heading text)
        if (
          insertIndex < lines.length &&
          !lines[insertIndex].trim().startsWith("#")
        ) {
          insertIndex++;
        }
        break;
      }
    }

    // Insert skills section
    lines.splice(insertIndex, 0, skillsSection);
    return lines.join("\n");
  }
}

/**
 * Create a Cursor agent transformer instance
 */
export function createCursorAgentTransformer(): AgentTransformer {
  return new CursorAgentTransformer();
}
