import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";
import type { AITool, InstallScope } from "../config.js";
import { KITS } from "../config.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// After tsup bundles to dist/cli.js, paths need to be relative from dist/
export const KITS_DIR = path.resolve(__dirname, "../kits");
export const COMMON_DIR = path.resolve(__dirname, "../common");

export interface InstallOptions {
  aiTool: AITool;
  kits: string[];
  targetPath: string;
  scope: InstallScope;
}

export interface InstallResult {
  kit: string;
  agents: number;
  skills: number;
  workflows: number;
}

/**
 * Base installer interface - each AI tool implements this
 */
export interface AIToolInstaller {
  install(options: InstallOptions): Promise<InstallResult[]>;
}

/**
 * Get kit source path and validate kit exists
 */
export function getKitSource(kitId: string): {
  kitSourcePath: string;
  kit: (typeof KITS)[0];
} {
  const kit = KITS.find((k) => k.id === kitId);
  if (!kit || !kit.available) {
    throw new Error(`Kit "${kitId}" is not available`);
  }
  const kitSourcePath = path.join(KITS_DIR, kitId);
  return { kitSourcePath, kit };
}

/**
 * Replace AI tool path references in file content
 * Converts .agent/, .claude/, .gemini/, .cursor/, .codex/ to target tool path
 */
export function replaceToolPaths(content: string, targetPath: string): string {
  return content.replace(
    /\.(agent|claude|gemini|cursor|codex)\//g,
    `${targetPath}/`,
  );
}

/**
 * Check if file should have path replacement applied
 * Only applies to text files that may contain path references
 */
export function shouldReplacePaths(filename: string): boolean {
  const ext = path.extname(filename).toLowerCase();
  return [".md", ".py", ".sh", ".txt", ".json"].includes(ext);
}

/**
 * Copy directory recursively with optional path replacement
 */
export async function copyDirectory(
  src: string,
  dest: string,
  exclude: string[] = [],
  toolPath?: string,
): Promise<void> {
  await fs.mkdir(dest, { recursive: true });

  const entries = await fs.readdir(src, { withFileTypes: true });

  for (const entry of entries) {
    if (exclude.includes(entry.name)) {
      continue;
    }

    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      await copyDirectory(srcPath, destPath, exclude, toolPath);
    } else if (toolPath && shouldReplacePaths(entry.name)) {
      const content = await fs.readFile(srcPath, "utf-8");
      const updatedContent = replaceToolPaths(content, toolPath);
      await fs.writeFile(destPath, updatedContent);
    } else {
      await fs.copyFile(srcPath, destPath);
    }
  }
}

/**
 * Count items in a directory
 */
export async function countItems(dirPath: string): Promise<number> {
  try {
    const entries = await fs.readdir(dirPath);
    return entries.length;
  } catch {
    return 0;
  }
}

/**
 * Copy rules file with path replacement
 */
export async function copyRulesFile(
  kitSourcePath: string,
  kitTargetPath: string,
  targetPath: string,
  aiTool: AITool,
  scope: InstallScope,
  workflowsReplacement?: string,
): Promise<void> {
  const rulesSource = path.join(kitSourcePath, "rules", aiTool.kitRulesFile);
  const rulesTarget =
    scope === "global" || aiTool.rulesInsideKit
      ? path.join(kitTargetPath, aiTool.rulesFile)
      : path.join(targetPath, aiTool.rulesFile);

  // Ensure parent directory exists for rules file
  await fs.mkdir(path.dirname(rulesTarget), { recursive: true });

  try {
    let rulesContent = await fs.readFile(rulesSource, "utf-8");
    rulesContent = replaceToolPaths(rulesContent, aiTool.path);

    // Replace workflows/ with custom folder name if specified
    if (workflowsReplacement) {
      rulesContent = rulesContent.replace(
        /workflows\//g,
        `${workflowsReplacement}/`,
      );
    }

    await fs.writeFile(rulesTarget, rulesContent);
  } catch {
    // Try falling back to GEMINI.md as base
    try {
      const fallbackSource = path.join(kitSourcePath, "rules", "GEMINI.md");
      let rulesContent = await fs.readFile(fallbackSource, "utf-8");
      rulesContent = replaceToolPaths(rulesContent, aiTool.path);

      if (workflowsReplacement) {
        rulesContent = rulesContent.replace(
          /workflows\//g,
          `${workflowsReplacement}/`,
        );
      }

      await fs.writeFile(rulesTarget, rulesContent);
    } catch {
      // No rules file available
    }
  }
}

/**
 * Copy common skills and workflows
 */
export async function copyCommonAssets(
  kitTargetPath: string,
  aiTool: AITool,
  workflowsFolderName: string = "workflows",
): Promise<void> {
  const commonSkillsPath = path.join(COMMON_DIR, "skills");
  const commonWorkflowsPath = path.join(COMMON_DIR, "workflows");
  const commonDocPath = path.join(COMMON_DIR, "COMMON.md");

  // Copy common skills
  const targetSkillsPath = path.join(kitTargetPath, "skills");
  await fs.mkdir(targetSkillsPath, { recursive: true });
  await copyDirectory(commonSkillsPath, targetSkillsPath, [], aiTool.path);

  // Copy common workflows (with custom folder name)
  const targetWorkflowsPath = path.join(kitTargetPath, workflowsFolderName);
  await fs.mkdir(targetWorkflowsPath, { recursive: true });
  await copyDirectory(
    commonWorkflowsPath,
    targetWorkflowsPath,
    [],
    aiTool.path,
  );

  // Copy COMMON.md
  const targetCommonDoc = path.join(kitTargetPath, "COMMON.md");
  const commonContent = await fs.readFile(commonDocPath, "utf-8");
  const updatedCommonContent = replaceToolPaths(commonContent, aiTool.path);
  await fs.writeFile(targetCommonDoc, updatedCommonContent);
}
