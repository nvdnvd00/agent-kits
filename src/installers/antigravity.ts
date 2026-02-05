/**
 * Antigravity Installer - Base installer used by most AI tools
 * Also used as fallback for Claude, Gemini, Codex, and Custom
 *
 * Standard installation: copies kit with workflows/ folder
 */

import fs from "fs/promises";
import path from "path";
import type { AIToolInstaller, InstallOptions, InstallResult } from "./base.js";
import {
  copyCommonAssets,
  copyDirectory,
  copyRulesFile,
  countItems,
  getKitSource,
} from "./base.js";

export class AntigravityInstaller implements AIToolInstaller {
  async install(options: InstallOptions): Promise<InstallResult[]> {
    const { aiTool, kits, targetPath } = options;
    const results: InstallResult[] = [];

    for (const kitId of kits) {
      const { kitSourcePath, kit } = getKitSource(kitId);
      const kitTargetPath = path.join(targetPath, aiTool.path);

      // Ensure target directory exists
      await fs.mkdir(kitTargetPath, { recursive: true });

      // Copy kit contents (excluding rules folder)
      await copyDirectory(kitSourcePath, kitTargetPath, ["rules"], aiTool.path);

      // Copy rules file
      await copyRulesFile(
        kitSourcePath,
        kitTargetPath,
        targetPath,
        aiTool,
        options.scope,
      );

      // Copy common assets
      try {
        await copyCommonAssets(kitTargetPath, aiTool, "workflows");
      } catch {
        // Common assets might not exist
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
}
