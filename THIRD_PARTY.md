# Third-party components

god-mode bundles skills and agents written by other authors. Each one keeps its original license. The full license texts are in [`licenses/`](licenses/). Files may have been modified from the upstream versions listed below.

| Source | License | Upstream commit | Skills / agents |
| --- | --- | --- | --- |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT ([text](licenses/marketingskills-MIT.txt)) | `5b2c000` | 49 skills: `ab-testing`, `ad-creative`, `ads`, `ai-seo`, `analytics`, `aso`, `attribution`, `churn-prevention`, `co-marketing`, `cold-email`, `community-marketing`, `competitor-profiling`, `competitors`, `content-strategy`, `copy-editing`, `copywriting`, `cro`, `customer-research`, `directory-submissions`, `emails`, `free-tools`, `image`, `influencer-marketing`, `launch`, `lead-magnets`, `marketing-council`, `marketing-ideas`, `marketing-loops`, `marketing-plan`, `marketing-psychology`, `offers`, `onboarding`, `paywalls`, `popups`, `pricing`, `product-marketing`, `programmatic-seo`, `prospecting`, `public-relations`, `referrals`, `revops`, `sales-enablement`, `schema`, `seo-audit`, `signup`, `site-architecture`, `sms`, `social`, `video` |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | MIT ([text](licenses/agent-skills-MIT.txt)) | `bcab6a1` | 24 skills: `api-and-interface-design`, `browser-testing-with-devtools`, `ci-cd-and-automation`, `code-review-and-quality`, `code-simplification`, `context-engineering`, `debugging-and-error-recovery`, `deprecation-and-migration`, `documentation-and-adrs`, `doubt-driven-development`, `frontend-ui-engineering`, `git-workflow-and-versioning`, `idea-refine`, `incremental-implementation`, `interview-me`, `observability-and-instrumentation`, `performance-optimization`, `planning-and-task-breakdown`, `security-and-hardening`, `shipping-and-launch`, `source-driven-development`, `spec-driven-development`, `test-driven-development`, `using-agent-skills`. Agents: `code-reviewer`, `security-auditor`, `test-engineer`, `web-performance-auditor` |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 ([text](licenses/hyperframes-Apache-2.0.txt)) | `edb3747c4` | 25 skills: `captions-overlay`, `cut-the-curve`, `embedded-captions`, `faceless-explainer`, `figma`, `general-video`, `hyperframes`, `hyperframes-animation`, `hyperframes-audio`, `hyperframes-cli`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-registry`, `media-use`, `motion-doctrine`, `motion-graphics`, `music-to-video`, `oversized-cursor`, `pr-to-video`, `product-launch-video`, `remotion-to-hyperframes`, `seam-craft`, `slideshow`, `talking-head-recut` |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | MIT ([text](skills/archify/LICENSE)) | `9e35d2b` | `archify` (its own third-party notices are in [skills/archify/THIRD_PARTY_NOTICES.md](skills/archify/THIRD_PARTY_NOTICES.md)) |

Fonts bundled inside the hyperframes skills (for example `embedded-captions/modes/standard/fonts`) are distributed upstream under their own open font licenses, mostly the SIL Open Font License 1.1. `talking-head-recut/assets/vendor/gsap.min.js` is GSAP, distributed under the [GSAP Standard License](https://gsap.com/standard-license).

## Removed for licensing reasons

- `zero`, from officialzeroxyz/zero-plugins: the upstream repository has no license, so redistribution is not permitted.
- `changelog-video`, from heygen-com/hyperframes: it ships commercial fonts (TT Norms Pro, ABC Solar Display) that the repository license does not cover.

## Original to god-mode

34 skills: `agent-mcp-builder`, `ai-product-architect`, `ai-product-eval-ops`, `anti-slop`, `autoplan`, `backend-architect`, `data-analytics-growth`, `deep-code-audit`, `error-handling`, `fastapi-pro`, `founder-technical-decision`, `god`, `launch-growth-loop`, `mvp-scope-killer`, `nextjs-app-router`, `office-hours`, `plan-ceo-review`, `plan-design-review`, `plan-devex-review`, `plan-eng-review`, `prompt-engineering-patterns`, `rag-implementation`, `ralph-loop`, `retro`, `saas-business-model`, `saas-launch-revenue`, `security`, `self-learning-skills`, `skill-installer`, `startup-god-router`, `startup-idea-validation`, `thermo-nuclear-code-quality-review`, `thermo-nuclear-review`, `thermos`. Agents: `thermo-nuclear-review-subagent`, `thermo-nuclear-code-quality-review-subagent`.

Some of these reuse only the name of a skill from another project, for example the `plan-*-review`, `office-hours`, `autoplan` and `retro` skills from [garrytan/gstack](https://github.com/garrytan/gstack), or `fastapi-pro`, `backend-architect`, `rag-implementation` and `prompt-engineering-patterns` from [wshobson/agents](https://github.com/wshobson/agents). Their text is original.

## How this list was built

Every `SKILL.md` and agent was compared line by line against the upstream repositories above. A component is listed as third-party when at least 30% of its lines, or a substantial share of its six-word phrases, match an upstream file. `scripts/validate.py` fails the CI when a skill is missing from this file.
