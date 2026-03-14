import type { ContentTransformer, TransformContext } from "./types.js";
import {
  combineMarkdown,
  parseFrontmatter,
  serializeFrontmatter,
} from "./utils.js";

/**
 * OpenCode Command frontmatter interface
 *
 * OpenCode custom commands are simple markdown files with optional frontmatter.
 * Commands in `.opencode/commands/` are prefixed with `project:`.
 */
export interface OpenCodeCommandFrontmatter {
  description: string;
}

/**
 * Transformer for converting Agent-Kits workflows to OpenCode commands
 *
 * Key transformations:
 * 1. Keep `description` field in frontmatter
 * 2. Replace `.agent/` paths with `.opencode/`
 * 3. Replace `workflows/` references with `commands/`
 */
export class OpenCodeWorkflowTransformer implements ContentTransformer {
  /**
   * Transform workflow content from Agent-Kits format to OpenCode command format
   */
  transform(content: string, context: TransformContext): string {
    const parsed = parseFrontmatter(content);
    const originalData = parsed.data as Record<string, unknown>;

    // Create OpenCode command frontmatter (keep only description)
    const commandFrontmatter: OpenCodeCommandFrontmatter = {
      description: String(originalData.description || ""),
    };

    // Serialize new frontmatter
    const newFrontmatter = serializeFrontmatter(
      commandFrontmatter as unknown as Record<string, unknown>,
    );

    // Transform body content
    let bodyContent = parsed.content;

    // Replace path references
    bodyContent = this.transformPaths(bodyContent, context);

    // Transform terminology
    bodyContent = this.transformTerminology(bodyContent);

    return combineMarkdown(newFrontmatter, bodyContent);
  }

  /**
   * Replace .agent/ paths with .opencode/
   */
  private transformPaths(content: string, context: TransformContext): string {
    const toolPath = context.aiTool?.path || ".opencode";
    return content.replace(/\.agent\//g, `${toolPath}/`);
  }

  /**
   * Transform terminology: workflow → command
   */
  private transformTerminology(content: string): string {
    let transformed = content;

    transformed = transformed.replace(/workflows?\//gi, "commands/");
    transformed = transformed.replace(/\/workflow/gi, "/command");
    transformed = transformed.replace(/workflow/gi, "command");
    transformed = transformed.replace(/Workflow/g, "Command");
    transformed = transformed.replace(/WORKFLOW/g, "COMMAND");

    return transformed;
  }
}

/**
 * Create an OpenCode workflow transformer instance
 */
export function createOpenCodeWorkflowTransformer(): ContentTransformer {
  return new OpenCodeWorkflowTransformer();
}
