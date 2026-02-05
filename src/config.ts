import os from "os";
import path from "path";

export interface AITool {
  id: string;
  name: string;
  icon: string;
  path: string; // Workspace path (relative to project root)
  globalPathPattern: string; // Global path pattern (uses ~ for display, resolved at runtime)
  rulesFile: string;
  kitRulesFile: string; // Source file in kit's rules/ folder
  rulesInsideKit?: boolean; // If true, rules file goes inside kit folder even for workspace install
}

export interface Kit {
  id: string;
  name: string;
  icon: string;
  description: string;
  agents: number;
  skills: number;
  workflows: number;
  available: boolean;
}

// Installation scope options
export type InstallScope = "global" | "workspace";

/**
 * Get the absolute global path for an AI tool
 * Works correctly on Windows, macOS, and Linux
 *
 * @example
 * getGlobalPath(claudeTool) // Windows: "C:\\Users\\username\\.claude"
 * getGlobalPath(claudeTool) // macOS: "/Users/username/.claude"
 * getGlobalPath(claudeTool) // Linux: "/home/username/.claude"
 */
export function getGlobalPath(tool: AITool): string {
  // Extract the folder name from pattern (e.g., "~/.claude" -> ".claude")
  const folderName = tool.globalPathPattern.replace("~/", "");
  return path.join(os.homedir(), folderName);
}

/**
 * Get a display-friendly global path
 * Shows ~ on Unix, full path on Windows
 */
export function getGlobalPathDisplay(tool: AITool): string {
  if (process.platform === "win32") {
    return getGlobalPath(tool);
  }
  return tool.globalPathPattern;
}

export const AI_TOOLS: AITool[] = [
  {
    id: "claude",
    name: "Claude Code",
    icon: "🟠",
    path: ".claude",
    globalPathPattern: "~/.claude", // Resolved to home dir at runtime
    rulesFile: "CLAUDE.md",
    kitRulesFile: "CLAUDE.md",
    rulesInsideKit: true, // Claude reads from .claude/CLAUDE.md (2025 standard)
  },
  {
    id: "gemini",
    name: "Gemini CLI",
    icon: "🔵",
    path: ".gemini",
    globalPathPattern: "~/.gemini",
    rulesFile: "GEMINI.md",
    kitRulesFile: "GEMINI.md",
    rulesInsideKit: true, // Gemini reads from .gemini/GEMINI.md
  },
  {
    id: "codex",
    name: "Codex CLI",
    icon: "🟢",
    path: ".codex",
    globalPathPattern: "~/.codex",
    rulesFile: "AGENTS.md",
    kitRulesFile: "AGENTS.md",
    rulesInsideKit: true, // Codex reads from .codex/AGENTS.md
  },
  {
    id: "antigravity",
    name: "Antigravity",
    icon: "🟣",
    path: ".agent",
    globalPathPattern: "~/.agent",
    rulesFile: "GEMINI.md",
    kitRulesFile: "GEMINI.md",
    rulesInsideKit: true, // Antigravity reads GEMINI.md from inside .agent/
  },
  {
    id: "cursor",
    name: "Cursor",
    icon: "⚪",
    path: ".cursor/rules", // Modern path: .cursor/rules/ (2025 standard)
    globalPathPattern: "~/.cursor/rules",
    rulesFile: "rules.md", // Modern: .cursor/rules/rules.md instead of .cursorrules
    kitRulesFile: "CURSOR.md", // Source file in kit
    rulesInsideKit: true,
  },
  {
    id: "custom",
    name: "Custom",
    icon: "⚙️",
    path: ".ai",
    globalPathPattern: "~/.ai",
    rulesFile: "RULES.md",
    kitRulesFile: "GEMINI.md", // Use GEMINI.md as base for custom
  },
];

export const KITS: Kit[] = [
  {
    id: "coder",
    name: "Coder",
    icon: "💻",
    description: "22 agents, 39 skills, 7 workflows for software development",
    agents: 22,
    skills: 39,
    workflows: 7,
    available: true,
  },
  {
    id: "writer",
    name: "Writer",
    icon: "✍️",
    description: "Content creation, copywriting, documentation",
    agents: 0,
    skills: 0,
    workflows: 0,
    available: false,
  },
  {
    id: "researcher",
    name: "Researcher",
    icon: "🔬",
    description: "Research, analysis, synthesis",
    agents: 0,
    skills: 0,
    workflows: 0,
    available: false,
  },
  {
    id: "designer",
    name: "Designer",
    icon: "🎨",
    description: "UI/UX design, branding, visual assets",
    agents: 0,
    skills: 0,
    workflows: 0,
    available: false,
  },
];
