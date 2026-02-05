#!/usr/bin/env node

import * as p from "@clack/prompts";
import fs from "fs";
import os from "os";
import path from "path";
import pc from "picocolors";
import {
  AI_TOOLS,
  KITS,
  getGlobalPath,
  getGlobalPathDisplay,
  type AITool,
  type InstallScope,
} from "./config.js";
import { installKit } from "./installers/index.js";

/**
 * Expand ~ to home directory (cross-platform)
 */
function expandPath(inputPath: string): string {
  if (inputPath.startsWith("~")) {
    return path.join(os.homedir(), inputPath.slice(1));
  }
  return inputPath;
}

/**
 * Check if a directory exists
 */
function directoryExists(dirPath: string): boolean {
  try {
    return fs.existsSync(dirPath) && fs.statSync(dirPath).isDirectory();
  } catch {
    return false;
  }
}

/**
 * Get the installation path based on scope and AI tool
 * Works correctly on Windows, macOS, and Linux
 */
function getInstallPath(
  aiTool: AITool,
  scope: InstallScope,
  workspacePath: string,
): string {
  if (scope === "global") {
    return getGlobalPath(aiTool);
  }
  return path.join(workspacePath, aiTool.path);
}

/**
 * Get display-friendly path (shows ~ on Unix, full path on Windows)
 */
function getDisplayPath(absolutePath: string): string {
  const home = os.homedir();
  const isWindows = process.platform === "win32";

  if (!isWindows && absolutePath.startsWith(home)) {
    return "~" + absolutePath.slice(home.length);
  }
  return absolutePath;
}

async function main() {
  console.clear();

  // ASCII Art Banner
  console.log(
    pc.cyan(`
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     █████╗  ██████╗ ███████╗███╗   ██╗████████╗               ║
║    ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝               ║
║    ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║                  ║
║    ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║                  ║
║    ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║                  ║
║    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝                  ║
║                    ${pc.bold("K I T S")}                                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
`),
  );

  p.intro(pc.bgCyan(pc.black(" Universal AI Agent Toolkit ")));

  // Step 1: Select AI Tool
  const aiToolResult = await p.select({
    message: "Which AI tool are you using?",
    options: AI_TOOLS.map((tool) => ({
      value: tool.id,
      label: `${tool.icon} ${tool.name}`,
      hint: `workspace: ${tool.path} | global: ${getGlobalPathDisplay(tool)}`,
    })),
  });

  if (p.isCancel(aiToolResult)) {
    p.cancel("Installation cancelled.");
    process.exit(0);
  }

  const aiTool = AI_TOOLS.find((t) => t.id === aiToolResult) as AITool;

  // Step 2: Select Installation Scope (Global vs Workspace)
  const scopeResult = await p.select({
    message: "Where do you want to install?",
    options: [
      {
        value: "workspace" as InstallScope,
        label: "📁 Workspace (Current Project)",
        hint: `Install to ${path.join(process.cwd(), aiTool.path)}`,
      },
      {
        value: "global" as InstallScope,
        label: "🌍 Global (All Projects)",
        hint: `Install to ${getGlobalPathDisplay(aiTool)}`,
      },
    ],
  });

  if (p.isCancel(scopeResult)) {
    p.cancel("Installation cancelled.");
    process.exit(0);
  }

  const scope = scopeResult as InstallScope;

  // Step 3: Get workspace path if workspace scope
  let workspacePath = process.cwd();
  if (scope === "workspace") {
    const pathResult = await p.text({
      message: "Workspace path:",
      placeholder: process.cwd(),
      defaultValue: process.cwd(),
      validate: (value) => {
        if (!value) return "Path is required";
        const expanded = expandPath(value);
        if (!directoryExists(expanded)) {
          return `Directory does not exist: ${expanded}`;
        }
      },
    });

    if (p.isCancel(pathResult)) {
      p.cancel("Installation cancelled.");
      process.exit(0);
    }

    workspacePath = expandPath(pathResult as string);
  }

  // Calculate final installation path
  const finalInstallPath = getInstallPath(aiTool, scope, workspacePath);
  const rulesFilePath =
    scope === "global"
      ? path.join(os.homedir(), aiTool.rulesFile)
      : path.join(workspacePath, aiTool.rulesFile);

  // Step 4: Check if already installed
  if (directoryExists(finalInstallPath)) {
    p.log.warn(
      `${pc.yellow("⚠")} Existing installation detected at: ${pc.cyan(getDisplayPath(finalInstallPath))}`,
    );

    const replaceResult = await p.select({
      message: "What would you like to do?",
      options: [
        {
          value: "replace",
          label: "🔄 Replace",
          hint: "Remove existing and install fresh",
        },
        {
          value: "merge",
          label: "🔀 Merge",
          hint: "Keep config files, update skills only",
        },
        {
          value: "skip",
          label: "⏭️ Skip",
          hint: "Keep existing, don't install",
        },
        {
          value: "cancel",
          label: "❌ Cancel",
          hint: "Exit installer",
        },
      ],
    });

    if (p.isCancel(replaceResult) || replaceResult === "cancel") {
      p.cancel("Installation cancelled.");
      process.exit(0);
    }

    if (replaceResult === "skip") {
      p.log.info("Skipping installation. Existing files preserved.");
      process.exit(0);
    }

    // Handle replace or merge
    if (replaceResult === "replace") {
      p.log.step(`Removing existing installation...`);
      fs.rmSync(finalInstallPath, { recursive: true, force: true });
    }
    // For merge, we'll let the installer handle it (it will overwrite files)
  }

  // Step 5: Select kits
  const selectedKits = await p.multiselect({
    message: "Select kits to install:",
    options: KITS.filter((kit) => kit.available).map((kit) => ({
      value: kit.id,
      label: `${kit.icon} ${kit.name}`,
      hint: kit.description,
    })),
    required: true,
  });

  if (p.isCancel(selectedKits)) {
    p.cancel("Installation cancelled.");
    process.exit(0);
  }

  // Step 6: Show summary and confirm
  const displayInstallPath = getDisplayPath(finalInstallPath);
  const displayRulesPath = getDisplayPath(rulesFilePath);

  const summaryLines = [
    `${pc.bold("AI Tool:")} ${aiTool.icon} ${aiTool.name}`,
    `${pc.bold("Scope:")} ${scope === "global" ? "🌍 Global" : "📁 Workspace"}`,
    `${pc.bold("Install Path:")} ${pc.cyan(displayInstallPath)}`,
    `${pc.bold("Rules File:")} ${pc.cyan(displayRulesPath)}`,
    `${pc.bold("Kits:")} ${(selectedKits as string[]).join(", ")}`,
  ];

  p.note(summaryLines.join("\n"), "Installation Summary");

  const confirmed = await p.confirm({
    message: `Proceed with installation?`,
  });

  if (p.isCancel(confirmed) || !confirmed) {
    p.cancel("Installation cancelled.");
    process.exit(0);
  }

  // Step 7: Installation
  const s = p.spinner();
  s.start(`Installing to ${pc.cyan(displayInstallPath)}...`);

  try {
    const results = await installKit({
      aiTool,
      kits: selectedKits as string[],
      targetPath: scope === "global" ? os.homedir() : workspacePath,
      scope,
    });

    s.stop("Installation complete!");

    // Summary
    p.note(
      [
        `${pc.bold("📍 Location:")} ${displayInstallPath}`,
        `${pc.bold("📜 Rules:")} ${displayRulesPath}`,
        "",
        ...results.map(
          (r) =>
            `${pc.green("✓")} ${r.kit}: ${r.agents} agents, ${r.skills} skills, ${r.workflows} workflows`,
        ),
      ].join("\n"),
      "Installed Successfully",
    );

    // Next steps based on scope
    const archPath =
      scope === "global"
        ? `${getGlobalPathDisplay(aiTool)}/ARCHITECTURE.md`
        : `${aiTool.path}/ARCHITECTURE.md`;

    p.outro(
      pc.green("Success! ") +
        pc.dim("Next steps:\n") +
        `  ${pc.cyan("•")} Use ${pc.bold("/filter")} to optimize skills for your project\n` +
        `  ${pc.cyan("•")} Use ${pc.bold("/plan")} to create project plans\n` +
        `  ${pc.cyan("•")} Use ${pc.bold("@backend-specialist")} for APIs\n` +
        `  ${pc.cyan("•")} Read ${pc.bold(archPath)}`,
    );
  } catch (error) {
    s.stop("Installation failed!");
    p.log.error(error instanceof Error ? error.message : "Unknown error");
    process.exit(1);
  }
}

main().catch(console.error);
