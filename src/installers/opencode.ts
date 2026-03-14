/**
 * OpenCode Installer - Special handling for OpenCode CLI tool
 *
 * Key differences from default installer:
 * - Workflows are called "commands" in OpenCode
 * - Commands are stored in .opencode/commands/ instead of .opencode/workflows/
 * - Rules file (AGENTS.md) goes to project root (rulesInsideKit = false)
 * - No agent transformation needed (OpenCode doesn't have subagent concept)
 */

import fs from "fs/promises";
import path from "path";
import type { TransformContext } from "../transformers/index.js";
import {
  createOpenCodeWorkflowTransformer,
} from "../transformers/index.js";
import type { AIToolInstaller, InstallOptions, InstallResult } from "./base.js";
import {
  copyCommonAssets,
  copyDirectory,
  copyRulesFile,
  countItems,
  getKitSource,
} from "./base.js";

export class OpenCodeInstaller implements AIToolInstaller {
  // OpenCode uses "commands" instead of "workflows"
  private readonly COMMANDS_FOLDER = "commands";

  // Transformer for OpenCode command format
  private readonly workflowTransformer = createOpenCodeWorkflowTransformer();

  async install(options: InstallOptions): Promise<InstallResult[]> {
    const { aiTool, kits, targetPath } = options;
    const results: InstallResult[] = [];

    for (const kitId of kits) {
      const { kitSourcePath, kit } = getKitSource(kitId);
      const kitTargetPath = path.join(targetPath, aiTool.path);

      // Ensure target directory exists
      await fs.mkdir(kitTargetPath, { recursive: true });

      // Copy kit contents (excluding rules and workflows - we handle them separately)
      await copyDirectory(
        kitSourcePath,
        kitTargetPath,
        ["rules", "workflows"],
        aiTool.path,
      );

      // Transform and copy workflows as "commands" for OpenCode
      await this.copyWorkflowsWithTransform(
        kitSourcePath,
        kitTargetPath,
        aiTool.path,
      );

      // Copy rules file (AGENTS.md to project root)
      await copyRulesFile(
        kitSourcePath,
        kitTargetPath,
        targetPath,
        aiTool,
        options.scope,
        this.COMMANDS_FOLDER, // Replace workflows/ with commands/
      );

      // Copy common assets (using commands folder)
      try {
        await copyCommonAssets(kitTargetPath, aiTool, this.COMMANDS_FOLDER);
      } catch {
        // Common assets might not exist
      }

      // Count installed items
      const agents = await countItems(path.join(kitTargetPath, "agents"));
      const skills = await countItems(path.join(kitTargetPath, "skills"));
      const commands = await countItems(
        path.join(kitTargetPath, this.COMMANDS_FOLDER),
      );

      results.push({
        kit: kit.name,
        agents,
        skills,
        workflows: commands, // Still called "workflows" in result for consistency
      });
    }

    return results;
  }

  /**
   * Copy workflows with transformation to OpenCode command format
   *
   * This method:
   * 1. Reads each workflow file from the kit
   * 2. Transforms the frontmatter to OpenCode command format
   * 3. Replaces path references (.agent/ → .opencode/)
   * 4. Replaces terminology (workflow → command)
   * 5. Writes the transformed command to the commands directory
   */
  private async copyWorkflowsWithTransform(
    kitSourcePath: string,
    kitTargetPath: string,
    toolPath: string,
  ): Promise<void> {
    const workflowsSource = path.join(kitSourcePath, "workflows");
    const commandsTarget = path.join(kitTargetPath, this.COMMANDS_FOLDER);

    try {
      await fs.access(workflowsSource);
    } catch {
      // No workflows directory
      return;
    }

    // Create target commands directory
    await fs.mkdir(commandsTarget, { recursive: true });

    // Read all workflow files
    const entries = await fs.readdir(workflowsSource, { withFileTypes: true });

    for (const entry of entries) {
      if (!entry.isFile() || !entry.name.endsWith(".md")) {
        continue;
      }

      const sourcePath = path.join(workflowsSource, entry.name);
      const targetPath = path.join(commandsTarget, entry.name);

      // Read original workflow content
      const content = await fs.readFile(sourcePath, "utf-8");

      // Transform to OpenCode command format
      const context: TransformContext = {
        aiTool: { path: toolPath } as TransformContext["aiTool"],
        sourcePath,
        targetPath,
      };

      const transformedContent = this.workflowTransformer.transform(
        content,
        context,
      );

      // Write transformed command
      await fs.writeFile(targetPath, transformedContent);
    }
  }
}
