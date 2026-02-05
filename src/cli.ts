#!/usr/bin/env node

import * as p from "@clack/prompts";
import boxen from "boxen";
import figlet from "figlet";
import fs from "fs";
import gradient from "gradient-string";
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

/**
 * Display the beautiful banner
 */
function displayBanner() {
  console.clear();

  // Create ASCII Art
  const text = figlet.textSync("AGENT KITS", {
    font: "Standard",
    horizontalLayout: "fitted",
  });

  // Apply gradient
  const title = gradient.passion(text);

  // Box it
  console.log(
    boxen(title, {
      padding: 1,
      margin: 1,
      borderStyle: "round",
      borderColor: "cyan",
      float: "center",
    }),
  );

  console.log(
    gradient.morning.multiline(
      "       ⚡  The Universal AI Agent Toolkit  ⚡       ",
    ),
  );
  console.log("");
}

async function main() {
  displayBanner();

  p.intro(pc.bgCyan(pc.black(" SETUP WIZARD ")));

  // Step 1: Select AI Tool
  const aiToolResult = await p.select({
    message: "🤖 Which AI assistant are you using?",
    options: AI_TOOLS.map((tool) => ({
      value: tool.id,
      label: `${tool.name}`,
      hint: `${getGlobalPathDisplay(tool)}`,
    })),
  });

  if (p.isCancel(aiToolResult)) {
    p.cancel("Operation cancelled.");
    process.exit(0);
  }

  const aiTool = AI_TOOLS.find((t) => t.id === aiToolResult) as AITool;

  // Step 2: Select Installation Scope (Global vs Workspace)
  const scopeResult = await p.select({
    message: "📂 Where should we install?",
    options: [
      {
        value: "workspace" as InstallScope,
        label: "Workspace (Project)",
        hint: `Best for sharing with team (${path.join(process.cwd(), aiTool.path)})`,
      },
      {
        value: "global" as InstallScope,
        label: "Global (System)",
        hint: `Best for personal use across projects (${getGlobalPathDisplay(aiTool)})`,
      },
    ],
  });

  if (p.isCancel(scopeResult)) {
    p.cancel("Operation cancelled.");
    process.exit(0);
  }

  const scope = scopeResult as InstallScope;

  // Step 3: Get workspace path if workspace scope
  let workspacePath = process.cwd();
  if (scope === "workspace") {
    const pathResult = await p.text({
      message: "📍 Confirm workspace path:",
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
      p.cancel("Operation cancelled.");
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
      `${pc.yellow("⚠")} Existing toolkit found at: ${pc.cyan(getDisplayPath(finalInstallPath))}`,
    );

    const replaceResult = await p.select({
      message: "How should we proceed?",
      options: [
        {
          value: "replace",
          label: "🚀 Replace",
          hint: "Fresh install (Recommended)",
        },
        {
          value: "merge",
          label: "🔄 Merge",
          hint: "Update skills, keep configs",
        },
        {
          value: "skip",
          label: "⏭️ Skip",
          hint: "Don't install files",
        },
        {
          value: "cancel",
          label: "❌ Cancel",
          hint: "Exit setup",
        },
      ],
    });

    if (p.isCancel(replaceResult) || replaceResult === "cancel") {
      p.cancel("Operation cancelled.");
      process.exit(0);
    }

    if (replaceResult === "skip") {
      p.log.info("Skipping installation. Have a nice day! 👋");
      process.exit(0);
    }

    // Handle replace
    if (replaceResult === "replace") {
      const s_rm = p.spinner();
      s_rm.start("Cleaning up old files...");
      fs.rmSync(finalInstallPath, { recursive: true, force: true });
      s_rm.stop("Cleanup complete.");
    }
  }

  // Step 5: Select kits
  const selectedKits = await p.multiselect({
    message: "📦 Select kits to include:",
    options: KITS.filter((kit) => kit.available).map((kit) => ({
      value: kit.id,
      label: `${kit.icon} ${kit.name}`,
      hint: kit.description,
    })),
    required: true,
  });

  if (p.isCancel(selectedKits)) {
    p.cancel("Operation cancelled.");
    process.exit(0);
  }

  // Step 6: Confirmation
  const displayInstallPath = getDisplayPath(finalInstallPath);

  console.log("");
  console.log(
    boxen(
      [
        `${pc.cyan(pc.bold("TARGET SUMMARY"))}`,
        "",
        `${pc.dim("Tool:")}    ${aiTool.name}`,
        `${pc.dim("Scope:")}   ${scope === "global" ? "Global" : "Workspace"}`,
        `${pc.dim("Path:")}    ${displayInstallPath}`,
        `${pc.dim("Kits:")}    ${(selectedKits as string[]).join(", ")}`,
      ].join("\n"),
      { padding: 1, borderStyle: "single", borderColor: "dim" },
    ),
  );
  console.log("");

  const confirmed = await p.confirm({
    message: `Ready to install?`,
  });

  if (p.isCancel(confirmed) || !confirmed) {
    p.cancel("Operation cancelled.");
    process.exit(0);
  }

  // Step 7: Installation
  const s = p.spinner();
  s.start(`Installing ✨ magic...`);

  try {
    const results = await installKit({
      aiTool,
      kits: selectedKits as string[],
      targetPath: scope === "global" ? os.homedir() : workspacePath,
      scope,
    });

    const isGlobal = scope === "global";
    const rulesFile = isGlobal
      ? path.join(os.homedir(), aiTool.rulesFile)
      : path.join(workspacePath, aiTool.rulesFile);

    s.stop("Installation complete! 🎉");

    // Success Summary
    console.log("");
    console.log(
      boxen(
        [
          gradient.morning("Successfully Installed Agent Kits!"),
          "",
          `${pc.green("✔")} Core System Ready`,
          `${pc.green("✔")} ${results.reduce((acc, r) => acc + r.skills, 0)} Skills Active`,
          `${pc.green("✔")} Agents Deployed`,
          "",
          pc.bold("👉 NEXT STEPS:"),
          `1. Open ${pc.cyan(getDisplayPath(rulesFile))}`,
          `2. Read the instructions`,
          `3. Type ${pc.magenta("/plan")} or ${pc.magenta("/create")} to start`,
        ].join("\n"),
        {
          padding: 1,
          margin: 1,
          borderStyle: "round",
          borderColor: "green",
        },
      ),
    );

    p.outro(`Thank you for using Agent Kits. Happy coding! 🚀`);
  } catch (error) {
    s.stop("Installation failed.");
    p.log.error(error instanceof Error ? error.message : "Unknown error");
    process.exit(1);
  }
}

main().catch(console.error);
