import type { ContentTransformer, TransformContext } from "./types.js";
import {
  combineMarkdown,
  parseFrontmatter,
  serializeFrontmatter,
} from "./utils.js";

/**
 * Cursor Command frontmatter interface
 *
 * Based on Cursor's command specification:
 * - description: Command purpose (shown in command palette)
 * - globs: Optional file patterns for context
 * - alwaysApply: Whether to auto-apply
 * - referencedFiles: Files to include as context
 */
export interface CursorCommandFrontmatter {
  description: string;
  globs?: string;
  alwaysApply?: boolean;
  referencedFiles?: string[];
}

/**
 * Agent-Kits Workflow frontmatter interface
 */
export interface WorkflowFrontmatter {
  description: string;
  agent?: string;
  trigger?: string;
}

/**
 * Transformer for converting Agent-Kits workflows to Cursor commands
 *
 * Key transformations:
 * 1. Keep `description` field
 * 2. Replace `.agent/` paths with `.cursor/` in content
 * 3. Replace `workflows/` references with `commands/`
 * 4. Update agent paths to use `.cursor/agents/`
 * 5. Update skill paths to use `.cursor/skills/`
 */
export class CursorWorkflowTransformer implements ContentTransformer {
  /**
   * Transform workflow content from Agent-Kits format to Cursor command format
   */
  transform(content: string, context: TransformContext): string {
    const parsed = parseFrontmatter(content);
    const originalData = parsed.data as unknown as WorkflowFrontmatter;

    // Create Cursor command frontmatter
    // Keep only fields that Cursor commands support
    const cursorFrontmatter: CursorCommandFrontmatter = {
      description: originalData.description,
    };

    // Serialize new frontmatter
    const newFrontmatter = serializeFrontmatter(
      cursorFrontmatter as unknown as Record<string, unknown>,
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
   * Transform path references from .agent/ to .cursor/
   */
  private transformPaths(content: string, context: TransformContext): string {
    let transformed = content;

    // Replace .agent/ with tool path (.cursor/)
    const toolPath = context.aiTool?.path || ".cursor";
    transformed = transformed.replace(/\.agent\//g, `${toolPath}/`);

    return transformed;
  }

  /**
   * Transform terminology from Agent-Kits to Cursor
   */
  private transformTerminology(content: string): string {
    let transformed = content;

    // Replace workflow references with command references
    transformed = transformed.replace(/workflows?\//gi, "commands/");
    transformed = transformed.replace(/\/workflow/gi, "/command");
    transformed = transformed.replace(/workflow/gi, "command");
    transformed = transformed.replace(/Workflow/g, "Command");
    transformed = transformed.replace(/WORKFLOW/g, "COMMAND");

    return transformed;
  }
}

/**
 * Create a Cursor workflow transformer instance
 */
export function createCursorWorkflowTransformer(): ContentTransformer {
  return new CursorWorkflowTransformer();
}
