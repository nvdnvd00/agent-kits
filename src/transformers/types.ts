import type { AITool } from "../config.js";

/**
 * Context for transformation operations
 */
export interface TransformContext {
  /** Target AI tool configuration */
  aiTool: AITool;
  /** Source file path */
  sourcePath: string;
  /** Target file path */
  targetPath: string;
  /** Map of skill names to their descriptions (loaded from SKILL.md files) */
  skillDescriptions?: Record<string, string>;
}

/**
 * Parsed YAML frontmatter result
 */
export interface ParsedFrontmatter {
  /** Original YAML content as object */
  data: Record<string, unknown>;
  /** Content after frontmatter */
  content: string;
  /** Raw frontmatter string (without ---) */
  raw: string;
}

/**
 * Agent-Kits standard agent frontmatter
 */
export interface AgentKitsFrontmatter {
  name: string;
  description: string;
  tools?: string;
  model?: string;
  skills?: string;
  tier?: number;
}

/**
 * Cursor subagent frontmatter format
 */
export interface CursorSubagentFrontmatter {
  name: string;
  description: string;
  model?: string;
  readonly?: boolean;
  is_background?: boolean;
}

/**
 * Interface for content transformers
 */
export interface ContentTransformer {
  /**
   * Transform content for target AI tool
   * @param content - Original file content
   * @param context - Transformation context
   * @returns Transformed content
   */
  transform(content: string, context: TransformContext): string;
}

/**
 * Interface for agent-specific transformers
 */
export interface AgentTransformer extends ContentTransformer {
  /**
   * Transform agent file from Agent-Kits format to tool-specific format
   */
  transform(content: string, context: TransformContext): string;
}
