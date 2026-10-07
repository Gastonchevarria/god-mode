# /god route eval — 2026-10-06

`scripts/eval_god.py` sends 22 requests to `/god` (`tests/evals/god_routes.json`), in Spanish and English, and stops after 4 turns. Six are everyday requests that need no skill: rename a function, explain a regex, change a CSS color, write a commit message, add a `.env.example`, a React question. The other 16 cover one route each.

It records the route named on the `⚡ GOD` line, the skills `/god` loads, whether it reads `references/protocol.md`, and the cost of those 4 turns. A run passes when the route's name, before any parenthesis, names the expected route and no other one.

Model: `claude-opus-5-5`, 2 runs per request. Fable 5.1 answered "out of usage credits" in the test environment, so it could not be the model under test.

## Results

| | v1.5.0 router | v1.6.0 router |
| --- | --- | --- |
| Right route | 43 / 44 | 44 / 44 |
| Everyday requests named as a direct route | 11 / 12, under 6 different improvised names | 12 / 12, always `DIRECTA` (`DIRECT` once, in English) |
| Runs that loaded two skills at once | 5 | 0 |
| Runs that re-read `protocol.md` | 26 / 44 | 0 / 44 |
| Cost of the first 4 turns, per run | US$ 0.241 | US$ 0.236 |

- **The one v1.5.0 miss:** "change the primary button color" went to DESIGN. v1.6.0 says a one-off style change is DIRECTA.
- **Two skills at once (v1.5.0):** MONETIZATION loaded `saas-business-model` and `pricing`, AI-ARCH loaded `ai-product-architect` and `rag-implementation`, and GROWTH once loaded `saas-launch-revenue`, the billing skill, for "how do I get my first 100 users?". v1.6.0 loads one skill per request, and billing code moved to MONETIZATION.
- **Cost:** about the same, but the turns are spent differently. In v1.5.0, 26 runs spent a turn re-reading the protocol, and DEBUGGING, THERMO and FULL-BUILD had not loaded their skill within the 4 turns. In v1.6.0 those turns already run the skill.

## Caveats

- 2 runs per request; a routing change can move a case by one run.
- The first 4 turns only. The eval checks the route and the first skill, not the finished work.
- Before the final runs, the parser only read `Ruta:`; two English runs wrote `Route:` and were scored as errors. It now reads both.
