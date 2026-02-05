import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";
import type { AITool, InstallScope } from "../config.js";
import { KITS } from "../config.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KITS_DIR = path.resolve(__dirname, "../../kits");
const COMMON_DIR = path.resolve(__dirname, "../../common");

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
    await copyDirectory(kitSourcePath, kitTargetPath, ["rules"]);

    // Create rules file at root level (read from kit's rules/ folder)
    // Use the specific rules file for this AI tool
    const rulesSource = path.join(kitSourcePath, "rules", aiTool.kitRulesFile);
    const rulesTarget = path.join(targetPath, aiTool.rulesFile);

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

      // Copy common skills into kit's skills folder
      const targetSkillsPath = path.join(kitTargetPath, "skills");
      await fs.mkdir(targetSkillsPath, { recursive: true });
      await copyDirectory(commonSkillsPath, targetSkillsPath);

      // Copy common workflows into kit's workflows folder
      const targetWorkflowsPath = path.join(kitTargetPath, "workflows");
      await fs.mkdir(targetWorkflowsPath, { recursive: true });
      await copyDirectory(commonWorkflowsPath, targetWorkflowsPath);

      // Copy COMMON.md to kit root for reference
      const targetCommonDoc = path.join(kitTargetPath, "COMMON.md");
      await fs.copyFile(commonDocPath, targetCommonDoc);
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

async function copyDirectory(
  src: string,
  dest: string,
  exclude: string[] = [],
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
      await copyDirectory(srcPath, destPath, exclude);
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
