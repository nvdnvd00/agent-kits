import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";
import type { AITool, InstallScope } from "../config.js";
import { KITS } from "../config.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// After tsup bundles to dist/cli.js, paths need to be relative from dist/
const KITS_DIR = path.resolve(__dirname, "../kits");
const COMMON_DIR = path.resolve(__dirname, "../common");

interface InstallOptions {
  aiTool: AITool;
  kits: string[];
  targetPath: string;
  scope: InstallScope;
}

interface InstallResult {
  kit: string;
  agents: number;
  skills: number;
  workflows: number;
}

export async function installKit(
  options: InstallOptions,
): Promise<InstallResult[]> {
  const { aiTool, kits, targetPath } = options;
  const results: InstallResult[] = [];

  for (const kitId of kits) {
    const kit = KITS.find((k) => k.id === kitId);
    if (!kit || !kit.available) {
      throw new Error(`Kit "${kitId}" is not available`);
    }

    const kitSourcePath = path.join(KITS_DIR, kitId);
    const kitTargetPath = path.join(targetPath, aiTool.path);

    // Ensure target directory exists
    await fs.mkdir(kitTargetPath, { recursive: true });

    // Copy kit contents (excluding rules folder - we handle that separately)
    // Pass aiTool.path to replace .agent/ references with correct tool path
    await copyDirectory(kitSourcePath, kitTargetPath, ["rules"], aiTool.path);

    // Create rules file (2025 standard: all tools use rulesInsideKit=true)
    // - Global: inside kit directory (e.g., ~/.gemini/GEMINI.md, ~/.cursor/rules/rules.md)
    // - Workspace: inside kit directory (e.g., ./.claude/CLAUDE.md, ./.cursor/rules/rules.md)
    // This keeps project root clean and follows each tool's modern conventions
    const rulesSource = path.join(kitSourcePath, "rules", aiTool.kitRulesFile);
    const rulesTarget =
      options.scope === "global" || aiTool.rulesInsideKit
        ? path.join(kitTargetPath, aiTool.rulesFile) // Inside kit: ~/.gemini/GEMINI.md or ./.agent/GEMINI.md
        : path.join(targetPath, aiTool.rulesFile); // Project root: ./GEMINI.md

    try {
      let rulesContent = await fs.readFile(rulesSource, "utf-8");
      // Replace path references based on AI tool
      // Handle common path patterns: .agent/, .claude/, .gemini/, .cursor/, .codex/
      rulesContent = rulesContent.replace(
        /\.(agent|claude|gemini|cursor|codex)\//g,
        `${aiTool.path}/`,
      );
      await fs.writeFile(rulesTarget, rulesContent);
    } catch {
      // Rules file might not exist for this AI tool, that's OK
      // Try falling back to GEMINI.md as base
      try {
        const fallbackSource = path.join(kitSourcePath, "rules", "GEMINI.md");
        let rulesContent = await fs.readFile(fallbackSource, "utf-8");
        rulesContent = rulesContent.replace(
          /\.(agent|claude|gemini|cursor|codex)\//g,
          `${aiTool.path}/`,
        );
        await fs.writeFile(rulesTarget, rulesContent);
      } catch {
        // No rules file available
      }
    }

    // Copy common skills (shared across all kits)
    // Common skills are merged into the kit's skills/ and workflows/ directories
    try {
      const commonSkillsPath = path.join(COMMON_DIR, "skills");
      const commonWorkflowsPath = path.join(COMMON_DIR, "workflows");
      const commonDocPath = path.join(COMMON_DIR, "COMMON.md");

      // Copy common skills into kit's skills folder (with path replacement)
      const targetSkillsPath = path.join(kitTargetPath, "skills");
      await fs.mkdir(targetSkillsPath, { recursive: true });
      await copyDirectory(commonSkillsPath, targetSkillsPath, [], aiTool.path);

      // Copy common workflows into kit's workflows folder (with path replacement)
      const targetWorkflowsPath = path.join(kitTargetPath, "workflows");
      await fs.mkdir(targetWorkflowsPath, { recursive: true });
      await copyDirectory(
        commonWorkflowsPath,
        targetWorkflowsPath,
        [],
        aiTool.path,
      );

      // Copy COMMON.md to kit root for reference (with path replacement)
      const targetCommonDoc = path.join(kitTargetPath, "COMMON.md");
      const commonContent = await fs.readFile(commonDocPath, "utf-8");
      const updatedCommonContent = commonContent.replace(
        /\.(agent|claude|gemini|cursor|codex)\//g,
        `${aiTool.path}/`,
      );
      await fs.writeFile(targetCommonDoc, updatedCommonContent);
    } catch {
      // Common skills dir might not exist, that's OK
    }

    // Count installed items
    const agents = await countItems(path.join(kitTargetPath, "agents"));
    const skills = await countItems(path.join(kitTargetPath, "skills"));
    const workflows = await countItems(path.join(kitTargetPath, "workflows"));

    results.push({
      kit: kit.name,
      agents,
      skills,
      workflows,
    });
  }

  return results;
}

/**
 * Replace AI tool path references in file content
 * Converts .agent/, .claude/, .gemini/, .cursor/, .codex/ to target tool path
 */
function replaceToolPaths(content: string, targetPath: string): string {
  return content.replace(
    /\.(agent|claude|gemini|cursor|codex)\//g,
    `${targetPath}/`,
  );
}

/**
 * Check if file should have path replacement applied
 * Only applies to text files that may contain path references
 */
function shouldReplacePaths(filename: string): boolean {
  const ext = path.extname(filename).toLowerCase();
  return [".md", ".py", ".sh", ".txt", ".json"].includes(ext);
}

async function copyDirectory(
  src: string,
  dest: string,
  exclude: string[] = [],
  toolPath?: string, // If provided, replace .agent/ paths with this
): Promise<void> {
  await fs.mkdir(dest, { recursive: true });

  const entries = await fs.readdir(src, { withFileTypes: true });

  for (const entry of entries) {
    // Skip excluded directories/files
    if (exclude.includes(entry.name)) {
      continue;
    }

    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      await copyDirectory(srcPath, destPath, exclude, toolPath);
    } else if (toolPath && shouldReplacePaths(entry.name)) {
      // Read, replace paths, and write
      const content = await fs.readFile(srcPath, "utf-8");
      const updatedContent = replaceToolPaths(content, toolPath);
      await fs.writeFile(destPath, updatedContent);
    } else {
      await fs.copyFile(srcPath, destPath);
    }
  }
}

async function countItems(dirPath: string): Promise<number> {
  try {
    const entries = await fs.readdir(dirPath);
    return entries.length;
  } catch {
    return 0;
  }
}
