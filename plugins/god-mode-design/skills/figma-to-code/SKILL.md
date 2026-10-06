---
name: figma-to-code
description: "Reads a Figma design through the Figma MCP server and extracts exact tokens (colors, spacing, type, radii, shadows), variables, layers and a reference screenshot before any code. Use when the user shares a Figma link or says 'get the tokens from Figma' or 'match the mockup'."
---

# Figma to Code

Never guess a value that Figma can tell you. Colors, spacing, typography, radii, shadows and variable names come from the file, through the Figma MCP server, before the first line of CSS or JSX.

## 1. Check the connection

The Figma MCP server exposes tools such as `get_design_context`, `get_variable_defs`, `get_metadata` and `get_screenshot`. If none of them is available in the session, stop and show the user how to connect it; do not fall back to eyeballing a screenshot.

Remote server (works on every Figma plan, needs a browser login the first time):

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

Figma also ships a desktop server inside the Figma app (Dev or Full seat on paid plans). Either way, adding an MCP server is an external install: show the command and wait for the user's "yes".

## 2. Get the right node

Ask for a link to the frame or component, not the whole file. A Figma URL carries the node id after `node-id=`; the MCP tools take that id. If the user selected a layer in the Figma desktop app, the desktop server reads the current selection without a link.

## 3. Extract, in this order

1. `get_metadata`: the sparse layer tree. Use it to find the exact node and to see the component's structure (auto-layout frames, instances, text layers).
2. `get_variable_defs`: variables and styles used in the selection, with their names. These names map to design tokens in code.
3. `get_design_context`: the detailed layout and style data for the node, which is what the code must match.
4. `get_screenshot`: the reference image the verification step will compare against.
5. `download_assets` when the design has icons or images that must be exported.

Read only the node you are implementing. Pulling a whole page floods the context and slows every step after it.

## 4. Write the token table before coding

| Token | Figma variable | Value | Used by |
| --- | --- | --- | --- |
| Primary | `color/brand/500` | `#2563EB` | button background |
| Space 3 | `space/3` | `12px` (`0.75rem`) | button padding-y |
| Body | `type/body/md` | Inter 500 · 16px / 24px | label |
| Radius md | `radius/md` | `8px` | button |
| Shadow sm | `shadow/sm` | `0 1px 2px rgb(0 0 0 / .06)` | button rest |

Rules for the table:

- One row per value the component uses. If a value has no variable in Figma, say "no variable" and flag it: it may be a design inconsistency worth raising.
- Convert px to rem for font sizes and spacing when the project uses rem; keep both in the table.
- If the project already defines a token for the same value, map to the existing one and note the mapping. Never create a second token for the same color.
- Record states Figma has as separate variants or layers (`hover`, `pressed`, `disabled`). If a state is missing from the design, say so before building: the build step still implements it, with a value derived from the closest token, and the user decides whether to add it to Figma.

## 5. Hand off

Pass the token table, the layer tree and the screenshot path to the build step (`design-to-web`). Report anything Figma did not provide as the first line, never as an assumption buried in the code.
