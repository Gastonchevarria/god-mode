---
name: figma-to-code
description: "Reads a Figma design through the Figma MCP server and extracts exact tokens (colors, spacing, type, radii, shadows), variables, layers and a reference screenshot before any code. Use when the user shares a Figma link or says 'get the tokens from Figma' or 'match the mockup'."
---

# Figma to Code

Never guess a value that Figma can tell you. Colors, spacing, typography, radii, shadows and variable names come from the file, through the Figma MCP server, before the first line of CSS or JSX.

Every read is budgeted. On the free plans Figma allows very few MCP reads, so this skill gets a whole component out of one read, two at most, and never reads the same node twice.

## Read budget

Figma limits the MCP tools that read design data ([limits](https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/)):

| Plan and seat | Reads allowed |
| --- | --- |
| Starter, View or Collab seat | 20 per month |
| Professional, Organization or Enterprise, View or Collab seat | 6 per month |
| Professional, Dev or Full seat | 200 per day, 10 per minute |
| Organization, Dev or Full seat | 200 per day, 15 per minute |
| Enterprise, Dev or Full seat | 600 per day, 20 per minute |

Treat every account as the 20-per-month one unless the user says otherwise. Count each read you make and report the count at the end: `Figma: 1 lectura (get_design_context)`.

## 1. Check the connection

The Figma MCP server exposes tools such as `get_design_context`, `get_variable_defs` and `get_screenshot`. If none is available in the session, stop and show the user how to connect it; do not fall back to eyeballing a screenshot.

Remote server (works on every Figma plan, asks for a browser login the first time):

```bash
claude mcp add --transport http --scope user figma https://mcp.figma.com/mcp
```

In Cowork, connect the Figma connector from the connector settings. Either way, adding an MCP server is an external install: show the step and wait for the user's "yes".

Before the first `get_design_context`, load Figma's own design-to-code guidance, which the server requires: the `/figma-design-to-code` skill if the Figma plugin is installed, otherwise the MCP resource `skill://figma/figma-design-to-code/SKILL.md`. Loading it is not a design read.

## 2. Get a link to the exact node, before any read

Ask for a link to the frame or component, with `node-id=` in the URL. Do not spend a read to find the node: a link without `node-id` is answered by asking the user for a node link (in Figma: select the frame, then "Copy link to selection"), not by calling `get_metadata` to list the pages.

From `https://figma.com/design/<fileKey>/<name>?node-id=12-345`, the file key is `<fileKey>` and the node id is `12:345`. For a branch URL, use the branch key as the file key.

If the user wants several components that live in one frame, ask for the parent frame's link and read it once, instead of one read per child.

## 3. Look in the cache first

Every response is saved in the project under `.figma-cache/` and reused until the user says the design changed:

```
.figma-cache/
  <fileKey>_<nodeId>.context.md     # get_design_context output: reference code + notes
  <fileKey>_<nodeId>.png            # its screenshot, the reference for ui-states-verification
  <fileKey>_<nodeId>.variables.json # get_variable_defs, only if it was needed
  tokens.md                         # the token table of section 5, one per project
```

Before the first save, add `.figma-cache/` to `.git/info/exclude` so it never reaches the repository; that file is local and changes nothing in the repo. If the cache already has the node, read nothing from Figma and say so: `Figma: 0 lecturas (caché)`.

## 4. Read: one call, two at most

1. **`get_design_context`** with the file key and node id. It returns reference code, a screenshot of the node and the asset URLs in one read. Do not set `excludeScreenshot`; that screenshot is the reference for verification, so there is no separate `get_screenshot` call. Save the code and the screenshot to the cache.
2. **`get_variable_defs`**, only if the reference code from step 1 uses raw values (`#2563EB`, `12px`) instead of variable names, and the token table needs the Figma variable names. If the code already names the variables, skip it.

Never call these for a node already in the cache:

- `get_screenshot`: the screenshot came with step 1.
- `get_metadata`: only to list pages when there is no node link, and section 2 replaces that with a question.
- `download_assets`: step 1 already returns the asset URLs. Use it only for a format or scale the user asks for. Asset URLs expire, so download the files right after step 1.
- `get_motion_context`: only when the design has prototype animations the user wants reproduced. Otherwise motion comes from `motion-design`, at no read cost.

When a read fails with a rate limit, stop. Tell the user how many reads this session used, which ones, and that the plan's limit was reached; offer to continue from the cache or to wait. Do not retry in a loop: each retry may count.

## 5. Write the token table before coding

| Token | Figma variable | Value | Used by |
| --- | --- | --- | --- |
| Primary | `color/brand/500` | `#2563EB` | button background |
| Space 3 | `space/3` | `12px` (`0.75rem`) | button padding-y |
| Body | `type/body/md` | Inter 500 · 16px / 24px | label |
| Radius md | `radius/md` | `8px` | button |
| Shadow sm | `shadow/sm` | `0 1px 2px rgb(0 0 0 / .06)` | button rest |

Rules for the table:

- One row per value the component uses. If a value has no variable in Figma, write "no variable" and flag it: it may be a design inconsistency worth raising.
- Convert px to rem for font sizes and spacing when the project uses rem; keep both in the table.
- If the project already defines a token for the same value, map to it and note the mapping. Never create a second token for the same color.
- Append new tokens to `.figma-cache/tokens.md`, so the next component reuses them without a new read.
- Record the states Figma has as variants or layers (`hover`, `pressed`, `disabled`). If a state is missing from the design, say so before building: the build step still implements it from the closest token, and the user decides whether to add it to Figma. Do not read other variants one by one; ask for the component set's link if the states live there.

## 6. Hand off

Pass the token table, the reference code and the cached screenshot path to the build step (`design-to-web`). Report the reads used and anything Figma did not provide on the first line, never as an assumption buried in the code.
