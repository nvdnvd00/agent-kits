/**
 * Cursor Installer - Special handling for Cursor AI editor
 *
 * Key differences from default installer:
 * - Workflows are called "commands" in Cursor
 * - Commands are stored in .cursor/commands/ instead of .cursor/workflows/
 * - Rules file goes to .cursor/rules/rules.md
 * - Agents are transformed to Cursor subagent format with skills embedded
 */

import fs from "fs/promises";
import path from "path";
import type { TransformContext } from "../transformers/index.js";
import {
  createCursorAgentTransformer,
  createCursorWorkflowTransformer,
  parseFrontmatter,
} from "../transformers/index.js";
import type { AIToolInstaller, InstallOptions, InstallResult } from "./base.js";
import {
  COMMON_DIR,
  copyCommonAssets,
  copyDirectory,
  copyRulesFile,
  countItems,
  getKitSource,
  replaceToolPaths,
} from "./base.js";

export class CursorInstaller implements AIToolInstaller {
  // Cursor uses "commands" instead of "workflows"
  private readonly COMMANDS_FOLDER = "commands";

  // Transformers for Cursor-specific formats
  private readonly agentTransformer = createCursorAgentTransformer();
  private readonly workflowTransformer = createCursorWorkflowTransformer();

  async install(options: InstallOptions): Promise<InstallResult[]> {
    const { aiTool, kits, targetPath } = options;
    const results: InstallResult[] = [];

    for (const kitId of kits) {
      const { kitSourcePath, kit } = getKitSource(kitId);
      const kitTargetPath = path.join(targetPath, aiTool.path);

      // Ensure target directory exists
      await fs.mkdir(kitTargetPath, { recursive: true });

      // Load skill descriptions from kit and common skills
      const skillDescriptions = await this.loadSkillDescriptions(kitSourcePath);

      // Copy kit contents (excluding rules, workflows, and agents - we handle them separately)
      await copyDirectory(
        kitSourcePath,
        kitTargetPath,
        ["rules", "workflows", "agents"],
        aiTool.path,
      );

      // Transform and copy agents to Cursor subagent format
      await this.copyAgentsWithTransform(
        kitSourcePath,
        kitTargetPath,
        aiTool.path,
        skillDescriptions,
      );

      // Transform and copy workflows as "commands" for Cursor
      await this.copyWorkflowsWithTransform(
        kitSourcePath,
        kitTargetPath,
        aiTool.path,
      );

      // Copy rules file with workflows/ -> commands/ replacement
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
   * Load skill descriptions from SKILL.md files
   *
   * Reads the `description` field from each skill's frontmatter.
   * Loads from both kit-specific skills and common skills.
   *
   * @returns Map of skill name to description
   */
  private async loadSkillDescriptions(
    kitSourcePath: string,
  ): Promise<Record<string, string>> {
    const descriptions: Record<string, string> = {};

    // Load from kit skills
    const kitSkillsPath = path.join(kitSourcePath, "skills");
    await this.extractSkillDescriptions(kitSkillsPath, descriptions);

    // Load from common skills
    const commonSkillsPath = path.join(COMMON_DIR, "skills");
    await this.extractSkillDescriptions(commonSkillsPath, descriptions);

    return descriptions;
  }

  /**
   * Extract descriptions from all SKILL.md files in a directory
   */
  private async extractSkillDescriptions(
    skillsDir: string,
    descriptions: Record<string, string>,
  ): Promise<void> {
    try {
      const entries = await fs.readdir(skillsDir, { withFileTypes: true });

      for (const entry of entries) {
        if (!entry.isDirectory()) continue;

        const skillMdPath = path.join(skillsDir, entry.name, "SKILL.md");

        try {
          const content = await fs.readFile(skillMdPath, "utf-8");
          const parsed = parseFrontmatter(content);

          if (parsed.data.description) {
            // Extract first sentence or limit to 80 chars for brevity
            let desc = String(parsed.data.description);
            const sentenceEnd = desc.indexOf(". ");
            if (sentenceEnd > 0 && sentenceEnd < 80) {
              desc = desc.slice(0, sentenceEnd);
            } else if (desc.length > 80) {
              desc = desc.slice(0, 77) + "...";
            }
            descriptions[entry.name] = desc;
          }
        } catch {
          // SKILL.md might not exist for this skill
        }
      }
    } catch {
      // Skills directory might not exist
    }
  }

  /**
   * Copy agents with transformation to Cursor subagent format
   *
   * This method:
   * 1. Reads each agent file from the kit
   * 2. Transforms the frontmatter to Cursor subagent format
   * 3. Embeds skills references into the agent body
   * 4. Writes the transformed agent to the target directory
   */
  private async copyAgentsWithTransform(
    kitSourcePath: string,
    kitTargetPath: string,
    toolPath: string,
    skillDescriptions: Record<string, string>,
  ): Promise<void> {
    const agentsSource = path.join(kitSourcePath, "agents");
    const agentsTarget = path.join(kitTargetPath, "agents");

    try {
      // Check if agents directory exists
      await fs.access(agentsSource);
    } catch {
      // No agents directory
      return;
    }

    // Create target agents directory
    await fs.mkdir(agentsTarget, { recursive: true });

    // Read all agent files
    const entries = await fs.readdir(agentsSource, { withFileTypes: true });

    for (const entry of entries) {
      if (!entry.isFile() || !entry.name.endsWith(".md")) {
        continue;
      }

      const sourcePath = path.join(agentsSource, entry.name);
      const targetPath = path.join(agentsTarget, entry.name);

      // Read original agent content
      let content = await fs.readFile(sourcePath, "utf-8");

      // Replace tool paths first (.agent/ -> .cursor/)
      content = replaceToolPaths(content, toolPath);

      // Transform to Cursor subagent format
      const context: TransformContext = {
        aiTool: { path: toolPath } as TransformContext["aiTool"],
        sourcePath,
        targetPath,
        skillDescriptions,
      };

      const transformedContent = this.agentTransformer.transform(
        content,
        context,
      );

      // Write transformed agent
      await fs.writeFile(targetPath, transformedContent);
    }
  }

  /**
   * Copy workflows with transformation to Cursor command format
   *
   * This method:
   * 1. Reads each workflow file from the kit
   * 2. Transforms the frontmatter to Cursor command format
   * 3. Replaces path references (.agent/ -> .cursor/)
   * 4. Replaces terminology (workflow -> command)
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
      // Check if workflows directory exists
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

      // Transform to Cursor command format
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
