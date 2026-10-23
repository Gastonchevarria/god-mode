<div align="center">

<img src="assets/banner.png" alt="DEV GOD-MODE" width="100%" />

# ⚡ DEV GOD-MODE

### Describe the problem. `/god` picks the right skills and sees the job through.

111 expert skills, 6 review subagents and one execution protocol for **Claude Code, Antigravity, Cursor and Windsurf**.<br/>
It finishes reversible work end to end, and asks you before anything it can't undo.

[![Release](https://img.shields.io/github/v/release/Gastonchevarria/god-mode?style=for-the-badge&color=00b4d8)](https://github.com/Gastonchevarria/god-mode/releases)
[![CI](https://img.shields.io/github/actions/workflow/status/Gastonchevarria/god-mode/ci.yml?branch=main&style=for-the-badge&label=CI)](https://github.com/Gastonchevarria/god-mode/actions/workflows/ci.yml)
[![Skills](https://img.shields.io/badge/skills-111-7b2cbf?style=for-the-badge)](#-pick-a-pack)
[![License: MIT](https://img.shields.io/badge/license-MIT-f4d35e?style=for-the-badge)](LICENSE)

**[Install in 30 seconds](#-install-in-30-seconds)** · [See it work](#-see-it-work) · [The 5 commands](#-the-5-commands-worth-memorizing) · [How it works](#-how-it-works) · [FAQ](#-faq)

</div>

---

## 🤔 Why god-mode?

AI coding agents are powerful, but you have probably hit these walls:

| Without god-mode | With god-mode |
| :--- | :--- |
| You have to know which skill or prompt fits the job | Type `/god` and describe the problem. It routes to the right skills for you |
| The agent stops halfway: *"now you implement steps 4 and 5"* | It finishes every reversible step, then checks its own last paragraph for loose ends |
| It says "done" while a test quietly failed | Failures go on the **first line** of the reply, never buried in a summary |
| An eager agent pushes, deploys or deletes on its own | It **stops and asks** before push, deploy, delete, migrations, money, credentials, messages or installs |
| Every skill you add eats context | Pick a pack. All 111 descriptions take about 24,000 characters (6,000 tokens), well inside Claude Code's skill list on 1M-context models |
| Your rules only work in one editor | One protocol for Claude Code, Antigravity, Cursor and Windsurf |

---

## 🚀 Install in 30 seconds

Pick **one** way to install. Both give you the same skills.

| | **A. Installer** (recommended) | **B. Claude Code plugins** |
| :--- | :--- | :--- |
| **Best for** | Using god-mode everywhere, with the protocol always on | Trying it in Claude Code with nothing global changed |
| **Protocol** | Active in every session (managed block in `~/.claude/CLAUDE.md`, your own rules kept) | Active in every session (god-mode-core loads it when the session starts) |
| **Antigravity** | ✅ Installed automatically if `~/.gemini` exists | ❌ |
| **Cursor / Windsurf** | ✅ With `--cursor` or `god-mode cursor <project>` | ❌ |
| **Updates** | `god-mode update` | `/plugin marketplace update god-mode` |

**A. Installer** (macOS / Linux, needs `git` and `python3`):

```bash
curl -fsSL https://raw.githubusercontent.com/Gastonchevarria/god-mode/main/install.sh | bash -s -- --pack=core
```

**B. Claude Code plugins:**

```bash
/plugin marketplace add Gastonchevarria/god-mode
/plugin install god-mode-core@god-mode      # /god, /thermos, /anti-slop, /security, /archify
/plugin install god-mode-dev@god-mode       # optional: backend, frontend, AI, CI/CD, planning
/plugin install god-mode-growth@god-mode    # optional: pricing, SEO, CRO, ads, email, launch
/plugin install god-mode-design@god-mode    # optional: polished UI from a mockup, motion direction, Playwright verification
```

> [!WARNING]
> Don't use both at once. You would load every skill twice. `god-mode doctor` flags it.

> [!TIP]
> Do you use the Claude desktop app with the god-mode plugins uploaded for Cowork? Those plugins also load in the app's Claude Code sessions, so with the installer you would get every skill, hook and subagent twice. Run `god-mode claude-via plugins`: the CLI stops linking skills, copying subagents and writing hooks for Claude Code, and keeps the protocol in `CLAUDE.md`, Antigravity and Cursor as they are. Keep the plugins current by uploading each version's zip. `god-mode claude-via installer` reverts it.

**Check that it worked:** open Claude Code in any project and type `/god`. The first line of the reply should start with `⚡ GOD · Ruta:`.

---

## 👀 See it work

You describe the problem in plain English or Spanish:

```text
> /god our checkout endpoint returns 500 since the last deploy
```

The first line tells you which route it took and which skills it loaded, before it touches anything:

```text
⚡ GOD · Ruta: DEBUGGING · Skills: debugging-and-error-recovery · Reproduce the 500, find the root cause and fix it with a regression test.
```

Then it does the work. If a step fails, that failure opens the reply.

**What `/god` routes to:** one skill per request, the one that fits. Everyday requests load none.

| When you say something like… | Route | Skill it loads |
| :--- | :--- | :--- |
| "Rename this function" / "what does this regex do?" / "write the commit message" | Direct | none: it just does it |
| "Review this branch before I merge" | Thermo-nuclear review | `thermos` → two review subagents in parallel |
| "The build is broken" / "this test fails" | Debugging | `debugging-and-error-recovery` |
| "Audit security before launch" | Security | `security` |
| "Clean up the lazy AI code" | Anti-slop | `anti-slop` |
| "Draw our architecture" | Archify | `archify` |
| "Is this idea worth building?" | Discovery | `office-hours` |
| "Per seat or usage-based?" / "How much should we charge?" | Monetization | `saas-business-model` / `pricing` |
| "Build this feature end to end" | Full build | `incremental-implementation`, or `autoplan` when the feature is big or unclear |
| "Our MVP scope is too big" | Scope killer | `mvp-scope-killer` |
| "Build this screen from the mockup, pixel-perfect" | Design | `design-to-web` |
| "The modal feels stiff, add spring animations" | Design | `motion-design` |
| "Design the RAG pipeline" | AI architecture | `rag-implementation` |

---

## 👑 The 5 commands worth memorizing

| Command | What you get |
| :--- | :--- |
| **`/god`** | The router. Describe any problem: small requests get done directly, bigger ones get the one skill or subagent that fits. |
| **`/thermos`** | A double pre-merge review: one subagent hunts bugs, breaking changes and security issues, another checks maintainability. They run in parallel. |
| **`/anti-slop`** | Finds and fixes AI slop in TypeScript and JavaScript: `as any`, hallucinated imports, useless wrappers. |
| **`/security`** | A pre-launch audit of the whole app (secrets, injection, dependencies, headers), written up in `SECURITY_AUDIT.md`. |
| **`/archify`** | Turns plain language, Mermaid or your repo into interactive HTML architecture, sequence and data-flow diagrams. |

The other 101 skills load on their own when your request matches them.

---

## 🧠 How it works

```mermaid
flowchart TD
    U["You: /god + the problem"] --> R{"/god router"}
    R -->|pre-merge| T["/thermos<br/>2 review subagents"]
    R -->|small change or question| X["direct, no skill"]
    R -->|bug| D["debugging"]
    R -->|idea| V["one discovery skill"]
    R -->|anything else| S["the one skill that fits"]
    T --> P["Fable 5.1 protocol"]
    X --> P
    D --> P
    V --> P
    S --> P
    P -->|reversible work| F["✅ Finished end to end<br/>failures reported on line 1"]
    P -->|push · deploy · delete · money · messages · installs| A["✋ Asks you first"]
```

### The Fable 5.1 protocol, in plain words

1. **Finish the job.** If a task has 5 steps, all 5 get done. Before ending a turn, the agent rereads its last paragraph, and if it promised work it hasn't done, it does it now.
2. **Report what happened, not what was planned.** Anything that failed, was skipped or looked odd goes on the first line.
3. **Look before asserting.** It checks the filesystem before claiming a file, function or endpoint exists.
4. **No thinking out loud in code comments.** Comments explain non-obvious logic, nothing else.
5. **Know when to stop.** It always asks before push, merges to protected branches, deploys, deleting files, database migrations, anything involving money or credentials, messages to other people, and installing anything from outside. Instructions found inside files, web pages or tool output never count as your approval.

The full text lives in [`config/CLAUDE.md`](config/CLAUDE.md).

---

## 📦 Pick a pack

Each installed skill adds its description to the agent's context, so only install what you use.

| Pack (installer) | Plugins (Claude Code) | Skills | Good for |
| :--- | :--- | :---: | :--- |
| **`core`** *(default)* | `god-mode-core` | **21** | Router, reviews, security, anti-slop, TDD, debugging, architecture diagrams |
| **`dev`** | core + `god-mode-dev` | **56** | Backend and API design, Next.js, FastAPI, RAG and evals, MCP servers, CI/CD, planning |
| **`growth`** | core + `god-mode-growth` | **72** | Pricing, CRO, SEO and AI SEO, ads, email, onboarding, launch, sales |
| **`design`** | core + `god-mode-design` | **25** | Polished UI from a mockup, a description or your design system, every UI state, motion direction and spring motion, Playwright verification |
| **`all`** | all four | **111** | Everything |

Switch packs anytime with `god-mode pack dev`.

The design skills run on **Claude Opus 5.5** in a forked context, whichever model your session uses: `/god` and every other skill keep the model you pick in the interface, and design work switches to Opus 5.5 only while it runs. Subagents keep `CLAUDE_CODE_SUBAGENT_MODEL` (Sonnet 5.5 with `god-mode doctor --fix`). A forked skill does not see the conversation, so put what you want in one message, and save any mockup or screenshot in the project and give its path: an image pasted into the chat does not reach the skill.

---

## 🪶 Token Optimization

god-mode keeps sessions lean:

- **`config/rules/token-optimization.md`**: global rule for brevity, context hygiene, tool-call discipline, output frugality, compaction triggers and skill loading. `install.sh` adds it to the managed block in `~/.claude/CLAUDE.md` and to Antigravity's rules; the god-mode-core plugin loads it when the session starts.
- **`auto-compact` skill** (god-mode-core): rates the session 🟢🟡🔴 from observable signals (tool calls, back-and-forth, re-read files, topic changes) and, with your OK, compacts it with a structured summary that keeps decisions and dead ends.
- **CONTEXT-HEALTH route in `/god`**: "the session feels heavy" or "compact" loads `auto-compact`; "audit my CLAUDE.md and skills" runs Claude Code's own prompt audit (`/claude-api prompt-audit`) in a subagent.
- **Prompt audit after compacting**: after each compaction, a hook checks which instruction files changed since the last audit (CLAUDE.md, AGENTS.md, rules, commands, subagents, output styles and your own skills; it compares sizes and dates, not contents). Claude audits only those files, in a Sonnet subagent, with the session's model as the target, and shows you the findings. It edits nothing without your "yes". god-mode's own skills, linked into `~/.claude/skills`, are left out: an update does not trigger audits in every project. When the changed files add up to more than 60 KB, Claude only offers the audit (`GOD_MODE_PROMPT_AUDIT_MAX_KB` changes the cap, `0` removes it). Without a file list, Claude Code's prompt audit covers the whole working directory, which in a large repo is hundreds of thousands of tokens. Set `GOD_MODE_PROMPT_AUDIT` to `always` to audit every instruction file after every compaction, or to `off` to turn it off. The hook is installed by `god-mode doctor --fix` and loaded by the god-mode-core plugin. In Cowork, `claude-api` is turned off, so Claude says so in one line and carries on.
- **[Graphify](https://github.com/Graphify-Labs/graphify)** (optional, third-party, Apache-2.0): turns a repo into a local knowledge graph with tree-sitter, so Claude asks the graph instead of grepping dozens of files. `/god` sends "what depends on X", "what breaks if I change Y" or "trace the path from A to B" to the CODE-MAP route, which runs `graphify query`, `path`, `explain` or `affected` when the project has `graphify-out/graph.json`. god-mode does not install it: `uv tool install graphifyy` (the PyPI name has two y's for now), then, in each project, `graphify install --project`, `graphify extract . --code-only` (writes `graph.json`) and `graphify cluster-only . --no-label` (adds `GRAPH_REPORT.md` and `graph.html`). With those two flags everything stays on your machine: only code is parsed, and communities keep numbered names instead of LLM-written ones. A full `graphify extract .` also sends docs and images to whichever LLM API key is set in your environment. `graphify install --project` adds a section to the project's `CLAUDE.md` and a PreToolUse hook in `.claude/settings.json` that nudges Claude toward the graph before raw reads and searches. It also adds a `graphify` skill of about 43 KB whose description matches any question about the code, so Claude loads it often. CODE-MAP uses the CLI, not that skill. To keep Claude from loading it on its own, add `disable-model-invocation: true` to the frontmatter of `.claude/skills/graphify/SKILL.md`: `/graphify` still works. The hook only suggests the graph, at most five times per session, and in practice Claude kept reading files. With `graphify hook-guard read --strict` as the Read hook, the first read of indexed code in each session waits for a `graphify query`, then it only suggests. `god-mode usage` lists projects whose graph went unqueried. god-mode's SessionStart hook runs `graphify update .` in the background when a session starts and after each compaction, in projects that have a graph: code only, local, no tokens. `GOD_MODE_GRAPHIFY_REFRESH=off` turns it off.
- **Loop breaker**: a workflow that retries the same failing command "until it works" can run for hours and burn the whole budget. A PreToolUse hook on Bash blocks the fourth run in a row of the same command (a `sleep` before the retry does not hide it) and tells Claude to stop, report the error and wait for you. Any other command in between resets the count. `GOD_MODE_LOOP_MAX` changes the limit; `0` turns it off. Installed by `god-mode doctor --fix` and loaded by the god-mode-core plugin. The token rule says the same in words: at most 2 retries per step, then abort and report.
- **Blast radius**: a PreToolUse hook on Bash and the write tools blocks the actions that throw work away and says what they would touch, so the user decides: `rm` outside the temp dir (with the file count, and the way out: move to `_to_delete/`), `git reset --hard`, `git checkout -- …`, `git restore …` and `git clean -f` (listing the uncommitted files they would discard; a clean tree passes), `git stash drop|clear`, `git branch -D`, force pushes (naming the branch), and any Write/Edit outside the session's project, the temp dir or `~/.claude` (work for another project belongs in a session opened there). `GOD_MODE_BLAST=off` turns it off. Installed by `god-mode doctor --fix` and loaded by the god-mode-core plugin.
- **Short skill descriptions**: every description is 200 characters or fewer. Claude Code gives the list of skills 1% of the context window (about 40,000 characters on a 1M-context model, 8,000 on a 200k one) and lists the skills that do not fit by name only, which Claude cannot pick on its own. With all four packs plus Cowork's own skills, the old 300-character descriptions overflowed and 31 of the 35 `god-mode-dev` skills lost theirs. On a 200k-context model, install only the packs you use.
- **`god-mode doctor`**: checks the installation and the recommended settings below, and prints the exact fix for anything missing. It changes nothing unless you add `--fix`, which writes the settings below and god-mode's two SessionStart hooks into `~/.claude/settings.json` (backup first, every other key kept).
- **`god-mode usage`**: shows where Claude Code's tokens went in the last two days (`--days=N` for more): per session, the main model, cost as Claude Code computes it, cache reads, the largest context, compactions, subagents and skills. It also counts `claude -p` sessions such as AutoHarness, times the context was written again because the cache had expired, and Graphify graphs nobody queried. It only reads `~/.claude/projects` and each project's `graphify-out/`.

### Recommended settings

`god-mode doctor --fix` writes them for you:

```jsonc
// ~/.claude/settings.json
{
  "outputStyle": "Concise",                          // built-in style: results first, no narration
  "autoCompactWindow": 200000,                       // compact when the context fills 200k, about 187k after the 13k Claude Code keeps for the summary; with 1M it waits until ~987k (kept if you set it)
  "env": {
    "CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-5-5", // subagents run on Sonnet 5.5 instead of the main model
    "AUTOHARNESS_REFLECT_EVERY_N": "75",             // only if you use AutoHarness (default 50)
    "AUTOHARNESS_CONSOLIDATE_EVERY_N": "300"         // only if you use AutoHarness (default 250)
  },
  "hooks": {
    "SessionStart": [
      { "matcher": "compact",                         // after each compaction: prompt audit if instructions changed
        "hooks": [{ "type": "command", "command": "python3 \"/path/to/god-mode/plugins/god-mode-core/hooks/prompt_audit_check.py\"" }] },
      { "hooks": [{ "type": "command",                 // at start and after compaction: graphify update . where there is a graph
          "command": "python3 \"/path/to/god-mode/plugins/god-mode-core/hooks/graphify_refresh.py\"" }] }
    ]
  }
}
```

Exporting the same variables in `~/.zshrc` works too. For a single project, put these keys in the project's `.claude/settings.json`, next to rules such as `"permissions": {"deny": ["Bash(git push:*)", "Read(./**/.env)"]}`.
- **[AutoHarness](https://github.com/tigerless-labs/autoharness)** (optional, third-party, MIT): a Claude Code plugin that learns skills from your sessions. Each reflection runs a background session on Haiku; the higher values above make it run less often.

  ```
  /plugin marketplace add tigerless-labs/autoharness
  /plugin install autoharness@autoharness
  ```

---

## 🧩 Works with your tools

| Tool | What gets installed | Where |
| :--- | :--- | :--- |
| **Claude Code** | Skills, 6 subagents, protocol | `~/.claude/skills`, `~/.claude/agents`, `~/.claude/CLAUDE.md` |
| **Antigravity** | Skills and protocol rules | `~/.gemini/config/skills`, `~/.gemini/config/rules/dev_god_mode.md` |
| **Cursor** | Project rules | `.cursorrules` in your project |
| **Windsurf, Codex and other agents** | Project rules | `AGENTS.md` in your project |

For Cursor and Windsurf, run `god-mode cursor path/to/project`. Existing files are backed up first.

---

## 🛠️ The `god-mode` CLI

The installer adds a small CLI to `~/.local/bin`:

```bash
god-mode status                 # active pack, skill counts, subagents
god-mode doctor [--fix]         # checks the install and the recommended settings; --fix writes the settings
god-mode pack <core|dev|growth|all>
god-mode update                 # pull from GitHub, re-apply protocol, subagents and pack
god-mode cursor <project>       # copy .cursorrules and AGENTS.md into a project
god-mode add <github-url>       # install an external skill (asks first)
```

<details>
<summary><b>🤖 The 6 subagents</b></summary>

<br/>

Installed in `~/.claude/agents/` and dispatched by the skills when a job needs a specialist:

| Subagent | Focus |
| :--- | :--- |
| `thermo-nuclear-review-subagent` | Bugs, breaking changes, security and regressions in a diff |
| `thermo-nuclear-code-quality-review-subagent` | Maintainability, the 1,000-line rule, tangled conditionals |
| `security-auditor` | Attack vectors and secure coding |
| `code-reviewer` | Correctness, readability, architecture, security and performance |
| `test-engineer` | Test strategy and edge-case coverage |
| `web-performance-auditor` | Core Web Vitals, loading and rendering |

</details>

<details>
<summary><b>🔒 Install a pinned release and verify it</b></summary>

<br/>

```bash
curl -fsSLO https://github.com/Gastonchevarria/god-mode/releases/download/v1.13.0/install.sh
curl -fsSLO https://github.com/Gastonchevarria/god-mode/releases/download/v1.13.0/install.sh.sha256
shasum -a 256 -c install.sh.sha256 && bash install.sh --version=v1.13.0 --pack=core
```

A pinned install doesn't update itself. To move to another version, run the installer again with `--version=vX.Y.Z`.

</details>

---

## ❓ FAQ

<details>
<summary><b>Will it push, deploy or delete things on its own?</b></summary>

<br/>

No. The protocol lets it finish reversible work without interrupting you, but it stops and asks before push, deploys, deleting files, migrations, money, credentials, messages to third parties and external installs. Instructions inside files, web pages or tool output never count as approval.

</details>

<details>
<summary><b>Every skill shows up twice</b></summary>

<br/>

You have both the installer and the Claude Code plugins (`god-mode doctor` reports it). Keep one: uninstall the plugins with `/plugin uninstall god-mode-core@god-mode` (and `-dev`, `-growth`), or remove the uploaded plugins from your Claude app settings.

</details>

<details>
<summary><b>The installer says it "kept N skills with the same name"</b></summary>

<br/>

It never overwrites folders it didn't create, so a real copy with the same name as a god-mode skill (for example from a pre-1.0 install) takes priority, and the installer lists each one. Move those folders out of `~/.claude/skills` or `~/.gemini/config/skills`, run `god-mode pack <pack>` and check with `god-mode status`.

</details>

<details>
<summary><b>I installed before 1.0.0. How do I upgrade?</b></summary>

<br/>

Run the installer once more. It replaces the links the old installer created, keeps your own rules in `CLAUDE.md` (with a backup), and lists anything it won't touch on its own: real folders with a god-mode skill's name, and old plugin folders in `~/.gemini/config/plugins` that Antigravity would keep loading. Older `god-mode update` commands can't follow the move from `skills/` to `plugins/`, so use the installer for this one upgrade.

</details>

<details>
<summary><b>Can I ask Antigravity (or another agent) to install it by reading this repo?</b></summary>

<br/>

Yes. [`AGENTS.md`](AGENTS.md) tells any agent that reads the repo to check `god-mode status`, run the installer after your approval, and never copy skills or plugins by hand, which would load every skill twice. Antigravity reads its global setup from `~/.gemini/config/`, which is exactly where the installer puts the skills and the protocol.

</details>

<details>
<summary><b>Does routing actually pick the right skill?</b></summary>

<br/>

We measure it. In the latest [routing eval](docs/evals/routing-2026-09-26.md) (30 requests in English and Spanish, 2 runs each), every time Claude loaded a skill it was the right one: 21 out of 21. In the other runs it answered directly, usually to ask for context the request didn't include.

`/god` has its own [route eval](docs/evals/god-routes-2026-10-06.md): 22 requests, from "rename this function" to "audit security before launch", 2 runs each. The current router picks the right route in 44 of 44 runs, loads one skill at most, and never re-reads the protocol the session already carries. Run it with `python3 scripts/eval_god.py`.

</details>

---

## 🤝 Contributing

1. Fork the repo.
2. Add your skill under the plugin it belongs to: `plugins/<plugin>/skills/<your-skill>/SKILL.md`, with a `name` equal to the folder and a `description` of 200 characters or fewer.
3. If it comes from another project, add it to `config/third_party.json`.
4. Run the same checks as CI:
   ```bash
   python3 scripts/build_plugins.py
   python3 scripts/validate.py
   python3 -m unittest discover -s tests
   bash tests/smoke.sh
   npm ci --prefix plugins/god-mode-core/skills/archify && python3 scripts/test_archify.py
   ```
5. Open a pull request.

## 📄 License

god-mode's own code and skills are **MIT**. Created by [Gaston Chevarria](https://github.com/Gastonchevarria).

Many skills come from other open-source projects and keep their original licenses (MIT and Apache-2.0). See [THIRD_PARTY.md](THIRD_PARTY.md) for credits, and [SECURITY.md](SECURITY.md) to report a vulnerability.

<div align="center">

<br/>

**If god-mode saves you time, a ⭐ helps other developers find it.**

[![Star on GitHub](https://img.shields.io/github/stars/Gastonchevarria/god-mode?style=social)](https://github.com/Gastonchevarria/god-mode)

</div>
