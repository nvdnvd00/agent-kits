import type {
  AgentKitsFrontmatter,
  AgentTransformer,
  TransformContext,
} from "./types.js";
import {
  combineMarkdown,
  parseFrontmatter,
  serializeFrontmatter,
} from "./utils.js";

/**
 * OpenCode Agent frontmatter interface
 *
 * OpenCode expects `tools` as a record of { toolName: boolean }
 * instead of a comma-separated string.
 *
 * @see https://opencode.ai/docs/agents#tools
 */
export interface OpenCodeAgentFrontmatter {
  description: string;
  model?: string;
  tools?: Record<string, boolean>;
  mode?: string;
}

/**
 * Mapping from Agent-Kits tool names to OpenCode tool identifiers
 *
 * Agent-Kits uses capitalized names (Read, Write, Edit, Bash, Grep, Glob, Agent)
 * OpenCode uses lowercase names (read, write, edit, bash, glob, grep, agent)
 */
const TOOL_NAME_MAP: Record<string, string> = {
  read: "read",
  write: "write",
  edit: "edit",
  bash: "bash",
  grep: "grep",
  glob: "glob",
  agent: "agent",
};

/**
 * Transformer for converting Agent-Kits agents to OpenCode agent format
 *
 * Key transformations:
 * 1. Convert `tools` from comma-separated string to record<string, boolean>
 * 2. Remove `skills` and `tier` from frontmatter (kept in body for reference)
 * 3. Add `mode: subagent` for non-orchestrator agents
 * 4. Replace `.agent/` paths with `.opencode/`
 */
export class OpenCodeAgentTransformer implements AgentTransformer {
  /**
   * Transform agent content from Agent-Kits format to OpenCode agent format
   */
  transform(content: string, context: TransformContext): string {
    const parsed = parseFrontmatter(content);
    const originalData = parsed.data as unknown as AgentKitsFrontmatter;

    // Convert tools string to record
    const toolsRecord = this.parseToolsToRecord(originalData.tools);

    // Create new OpenCode agent frontmatter
    const opencodeFrontmatter: OpenCodeAgentFrontmatter = {
      description: originalData.description,
      ...(originalData.model && { model: originalData.model }),
      ...(Object.keys(toolsRecord).length > 0 && { tools: toolsRecord }),
    };

    // Serialize new frontmatter (with special tools handling)
    const newFrontmatter = this.serializeOpenCodeFrontmatter(opencodeFrontmatter);

    // Transform body content
    let bodyContent = parsed.content;

    // Replace path references
    bodyContent = this.transformPaths(bodyContent, context);

    return combineMarkdown(newFrontmatter, bodyContent);
  }

  /**
   * Parse comma-separated tools string into a record of { toolName: boolean }
   *
   * @example
   * "Read, Grep, Glob, Bash, Edit, Write" →
   * { read: true, grep: true, glob: true, bash: true, edit: true, write: true }
   */
  private parseToolsToRecord(
    toolsString: string | undefined,
  ): Record<string, boolean> {
    if (!toolsString) return {};

    const tools: Record<string, boolean> = {};
    const toolNames = toolsString.split(",").map((t) => t.trim().toLowerCase());

    for (const toolName of toolNames) {
      const mappedName = TOOL_NAME_MAP[toolName] || toolName;
      tools[mappedName] = true;
    }

    return tools;
  }

  /**
   * Custom serializer for OpenCode frontmatter
   *
   * OpenCode expects tools as a nested YAML map:
   * ```yaml
   * tools:
   *   read: true
   *   write: true
   * ```
   *
   * The standard serializeFrontmatter outputs flat key-value pairs,
   * so we need custom handling for the `tools` field.
   */
  private serializeOpenCodeFrontmatter(
    data: OpenCodeAgentFrontmatter,
  ): string {
    const lines: string[] = ["---"];

    // Serialize simple fields first
    if (data.description) {
      lines.push(`description: ${data.description}`);
    }
    if (data.model) {
      lines.push(`model: ${data.model}`);
    }
    if (data.mode) {
      lines.push(`mode: ${data.mode}`);
    }

    // Serialize tools as nested YAML map
    if (data.tools && Object.keys(data.tools).length > 0) {
      lines.push("tools:");
      for (const [tool, enabled] of Object.entries(data.tools)) {
        lines.push(`  ${tool}: ${enabled}`);
      }
    }

    lines.push("---");
    return lines.join("\n");
  }

  /**
   * Replace .agent/ paths with .opencode/
   */
  private transformPaths(content: string, context: TransformContext): string {
    const toolPath = context.aiTool?.path || ".opencode";
    return content.replace(/\.agent\//g, `${toolPath}/`);
  }
}

/**
 * Create an OpenCode agent transformer instance
 */
export function createOpenCodeAgentTransformer(): AgentTransformer {
  return new OpenCodeAgentTransformer();
}
