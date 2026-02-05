/**
 * Installer Entry Point
 * Routes to the appropriate installer based on AI tool selection
 */

import { AntigravityInstaller } from "./antigravity.js";
import type { AIToolInstaller, InstallOptions, InstallResult } from "./base.js";
import { CursorInstaller } from "./cursor.js";

// Re-export types for external use
export type { InstallOptions, InstallResult } from "./base.js";

/**
 * Registry of AI tool installers
 * Each AI tool can have its own specialized installer
 *
 * Antigravity is the base installer - other tools extend or reuse it
 */
const installerRegistry: Record<string, AIToolInstaller> = {
  // Antigravity is the base/default installer
  antigravity: new AntigravityInstaller(),

  // These tools use the same installation logic as Antigravity
  claude: new AntigravityInstaller(),
  gemini: new AntigravityInstaller(),
  codex: new AntigravityInstaller(),
  custom: new AntigravityInstaller(),

  // Cursor has special handling (workflows -> commands)
  cursor: new CursorInstaller(),
};

/**
 * Get the appropriate installer for an AI tool
 * Falls back to Antigravity installer for unknown tools
 */
function getInstaller(toolId: string): AIToolInstaller {
  const installer = installerRegistry[toolId];
  if (!installer) {
    // Fallback to Antigravity installer for unknown tools
    return new AntigravityInstaller();
  }
  return installer;
}

/**
 * Install kit(s) for the selected AI tool
 * Automatically routes to the correct installer based on tool selection
 */
export async function installKit(
  options: InstallOptions,
): Promise<InstallResult[]> {
  const installer = getInstaller(options.aiTool.id);
  return installer.install(options);
}
