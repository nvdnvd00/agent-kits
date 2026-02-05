import type { ParsedFrontmatter } from "./types.js";

/**
 * Parse YAML frontmatter from markdown content
 *
 * @param content - Markdown content with optional frontmatter
 * @returns Parsed frontmatter data and remaining content
 */
export function parseFrontmatter(content: string): ParsedFrontmatter {
  const frontmatterRegex = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/;
  const match = content.match(frontmatterRegex);

  if (!match) {
    return {
      data: {},
      content: content,
      raw: "",
    };
  }

  const rawFrontmatter = match[1];
  const bodyContent = match[2];

  // Parse YAML manually (simple key: value format)
  const data: Record<string, unknown> = {};
  const lines = rawFrontmatter.split("\n");

  for (const line of lines) {
    const colonIndex = line.indexOf(":");
    if (colonIndex === -1) continue;

    const key = line.slice(0, colonIndex).trim();
    let value: unknown = line.slice(colonIndex + 1).trim();

    // Handle boolean values
    if (value === "true") value = true;
    else if (value === "false") value = false;
    // Handle number values
    else if (!isNaN(Number(value)) && value !== "") value = Number(value);

    if (key) {
      data[key] = value;
    }
  }

  return {
    data,
    content: bodyContent,
    raw: rawFrontmatter,
  };
}

/**
 * Serialize frontmatter data back to YAML string
 *
 * @param data - Frontmatter data object
 * @returns YAML string with --- delimiters
 */
export function serializeFrontmatter(data: Record<string, unknown>): string {
  const lines: string[] = ["---"];

  for (const [key, value] of Object.entries(data)) {
    if (value === undefined || value === null) continue;
    lines.push(`${key}: ${value}`);
  }

  lines.push("---");
  return lines.join("\n");
}

/**
 * Combine frontmatter and content into markdown
 *
 * @param frontmatter - Serialized frontmatter (with --- delimiters)
 * @param content - Body content
 * @returns Combined markdown
 */
export function combineMarkdown(frontmatter: string, content: string): string {
  return `${frontmatter}\n${content}`;
}
