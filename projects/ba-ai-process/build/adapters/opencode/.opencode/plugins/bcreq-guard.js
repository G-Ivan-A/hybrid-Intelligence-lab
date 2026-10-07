// BCREQ guard: tools/opencode_hook.py decides every OpenCode tool call before it runs.
// A thrown error cancels the call; the runner and CI remain the authoritative gate.
import { spawnSync } from "node:child_process"
import path from "node:path"
import { fileURLToPath } from "node:url"

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..")
const HOOK = path.join(ROOT, "tools", "opencode_hook.py")
const PYTHONS = process.platform === "win32" ? [["python"], ["py", "-3"]] : [["python3"], ["python"]]

function decide(event) {
  for (const [command, ...prefix] of PYTHONS) {
    const result = spawnSync(command, [...prefix, HOOK], {
      cwd: ROOT,
      input: JSON.stringify(event),
      encoding: "utf8",
      timeout: 60000,
      windowsHide: true,
      env: { ...process.env, PYTHONUTF8: "1", PYTHONIOENCODING: "utf-8" },
    })
    if (result.error && result.error.code === "ENOENT") continue
    if (result.status !== 0 || !result.stdout) return { allow: false, reason: "Guard hook failed; check Python installation" }
    try {
      return JSON.parse(result.stdout.trim().split(/\r?\n/).pop())
    } catch {
      return { allow: false, reason: "Guard hook returned invalid output" }
    }
  }
  return { allow: false, reason: "Python 3.11+ is not found; every tool is blocked" }
}

export const BcreqGuard = async ({ directory }) => ({
  "tool.execute.before": async (input, output) => {
    const verdict = decide({ event: "tool.execute.before", tool: input.tool, args: output.args, directory })
    if (verdict.allow !== true) throw new Error(`BCREQ guard: ${verdict.reason || "tool call blocked"}`)
  },
})
