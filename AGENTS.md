# Meta-Engine: Universal Cognitive Model Toolkit

> **27 cognitive models · 53 scene combinations · Agent-agnostic · ~180KB knowledge base**

## What Is This?

Meta-Engine is a family of **27 deep cognitive models** distilled into structured, reusable markdown files. Each model provides a proven mental framework for reasoning about complex problems — from system architecture to strategic decisions, from debugging to personal growth.

Originally built as the "Xuan Master" (璇玑) skill family for Hermes Agent, Meta-Engine has been generalized to work across **any AI coding agent**: Claude Code, Codex, Cursor, OpenClaw, Hermes, and more.

## Layered Skills Architecture

The current canonical layer names are:

- **Xuan Master**: the core meta-cognition layer and 27-model knowledge kernel
- **Archon**: the enabler layer for calibration, orchestration, actions, and generation workflows such as document and PDF outputs
- **Prism**: the specialist layer for routing and mapping work into deeper domain-specific execution

In the current repository layout:

- `xuan-master/SKILL.md` is the loadable entrypoint for **Xuan Master**, backed by `xuan-master/00-entry/` plus the `xuan-master/001-*` through `xuan-master/027-*` model directories
- `archon/SKILL.md` is the loadable entrypoint for **Archon**, backed by `interview/` and `enabled/`
- `prism/SKILL.md` is the loadable entrypoint for **Prism**, with future specialist assets accumulating under `prism/domains/`
- `optimization/` remains a cross-cutting self-improvement loop across all layers

## How Agents Use It

### For any agent, the pattern is the same:

1. **Scan the catalog** (`xuan-master/00-entry/SKILL.md`) to find relevant models for the problem
   Or load `xuan-master/SKILL.md` as the core layer entrypoint first.
2. **Load the model files** by reading their SKILL.md
3. **Apply the frameworks** — principles, cross-domain mappings, case studies, practice exercises
4. **Combine models** using scene recommendations for multi-dimensional analysis

### Agent-specific integration:

| Agent | Integration Method |
|-------|-------------------|
| **Claude Code** | Add to CLAUDE.md: `When analyzing complex problems, load skills from Skills/meta-engine/` |
| **Codex (OpenAI)** | Include in .codex.md or project rules |
| **Cursor** | Add to .cursorrules as a knowledge base reference |
| **OpenClaw** | Load via its skill/plugin system |
| **Hermes** | Use native skill_view() or direct file reads |
| **Any LLM** | Simply read the SKILL.md files as context |

### Quick Start (10 minutes):

```
1. Read xuan-master/001-layered-architecture/SKILL.md — How to decompose any system
2. Read xuan-master/007-iterative-thinking/SKILL.md — How to improve anything
3. Read xuan-master/019-meta-cognition/SKILL.md — How to think about your thinking
```

## Model Catalog

### Speculative (Philosophy & Cognition) — 10 models
> Deep reasoning, worldviews, cognitive biases — the "why" layer

| # | Model | Read |
|---|-------|------|
| 004 | Pareto Distribution (80/20) | [SKILL.md](xuan-master/004-pareto-distribution/SKILL.md) |
| 005 | Reverse Thinking | [SKILL.md](xuan-master/005-reverse-thinking/SKILL.md) |
| 006 | First Principles | [SKILL.md](xuan-master/006-first-principles/SKILL.md) |
| 008 | Entropy Management | [SKILL.md](xuan-master/008-entropy-management/SKILL.md) |
| 009 | Path of Least Resistance | [SKILL.md](xuan-master/009-path-of-least-resistance/SKILL.md) |
| 010 | Occam's Razor | [SKILL.md](xuan-master/010-occams-razor/SKILL.md) |
| 012 | Game Theory | [SKILL.md](xuan-master/012-game-theory/SKILL.md) |
| 016 | Dual Process Theory | [SKILL.md](xuan-master/016-dual-process-theory/SKILL.md) |
| 019 | Meta-Cognition | [SKILL.md](xuan-master/019-meta-cognition/SKILL.md) |
| 027 | AI-Native Mindset | [SKILL.md](xuan-master/027-ai-native-mindset/SKILL.md) |

### Method (Execution & Process) — 10 models
> Structured operations, workflows, frameworks — the "how" layer

| # | Model | Read |
|---|-------|------|
| 007 | Iterative Thinking | [SKILL.md](xuan-master/007-iterative-thinking/SKILL.md) |
| 014 | 5W2H Analysis | [SKILL.md](xuan-master/014-5w2h/SKILL.md) |
| 015 | Lean Thinking | [SKILL.md](xuan-master/015-lean-thinking/SKILL.md) |
| 017 | BFS vs DFS Search | [SKILL.md](xuan-master/017-bfs-dfs/SKILL.md) |
| 018 | SWOT Analysis | [SKILL.md](xuan-master/018-swot/SKILL.md) |
| 020 | Six Thinking Hats | [SKILL.md](xuan-master/020-six-thinking-hats/SKILL.md) |
| 021 | SECI Knowledge Mgmt | [SKILL.md](xuan-master/021-seci-knowledge-management/SKILL.md) |
| 022 | McKinsey Method | [SKILL.md](xuan-master/022-mckinsey-method/SKILL.md) |
| 023 | OGSM Goal Management | [SKILL.md](xuan-master/023-ogsm-goal-management/SKILL.md) |
| 024 | RICE Diagnosis | [SKILL.md](xuan-master/024-rice-diagnosis/SKILL.md) |

### System (Engineering & Design) — 7 models
> Dynamic interaction, structural resilience, emergent behavior — the "organize" layer

| # | Model | Read |
|---|-------|------|
| 001 | Layered Architecture | [SKILL.md](xuan-master/001-layered-architecture/SKILL.md) |
| 002 | Flow Model | [SKILL.md](xuan-master/002-flow-model/SKILL.md) |
| 003 | State Machine | [SKILL.md](xuan-master/003-state-machine/SKILL.md) |
| 011 | Feedback Loop | [SKILL.md](xuan-master/011-feedback-loop/SKILL.md) |
| 013 | Network Effects | [SKILL.md](xuan-master/013-network-effects/SKILL.md) |
| 025 | High Availability Design | [SKILL.md](xuan-master/025-high-availability/SKILL.md) |
| 026 | Bio-Brain Architecture | [SKILL.md](xuan-master/026-bio-brain/SKILL.md) |

## Scene Recommendations (Top 15)

| Scenario | Model Pipeline |
|----------|---------------|
| System Architecture Design | 001 + 002 + 003 + 008 + 025 |
| Bug Diagnosis | 003 + 005 + 009 |
| Incident Response | 024 + 003 + 017 + 005 |
| Business/Product Decisions | 006 + 004 + 005 + 012 |
| Strategic Positioning | 018 + 014 + 005 |
| Investment Strategy Design | 006 + 003 + 004 + 002 + 011 + 025 + 012 + 016 + 019 + 007 |
| Deep Learning/Self-Study | 019 + 011 + 007 + 016 |
| Personal Knowledge Mgmt | 021 + 019 + 007 + 011 |
| AI Agent/System Design | 026 + 001 + 003 + 025 |
| Critical Thinking | 019 + 005 + 014 + 006 |
| Team Decision Making | 020 + 018 + 005 + 016 |
| OKR System Optimization | 023 + 004 + 011 + 007 |
| Risk/Continuity Planning | 025 + 024 + 004 + 023 |
| Code Quality Improvement | 011 + 007 + 005 + 010 |
| Career/Growth Planning | 026 + 019 + 011 + 021 |

*See `xuan-master/00-entry/SKILL.md` for all 53 scene combinations.*

## System Layers

```
Application Layer    → Specific problems → specific outputs
Prism Layer          → Domain routing → specialized mapping → deeper expert work
Archon Layer         → Calibration → orchestration → actions → generation → synthesis
Xuan Master Core     → 27 deep cognitive models (10 Speculative / 10 Method / 7 System)
Optimization Loop    → Audit → recovery → self-improvement across all layers
```

- **Xuan Master Core**: [`xuan-master/SKILL.md`](xuan-master/SKILL.md) backed by [`xuan-master/00-entry/SKILL.md`](xuan-master/00-entry/SKILL.md) plus the `xuan-master/001-*` through `xuan-master/027-*` model directories
- **Archon Layer**: [`archon/SKILL.md`](archon/SKILL.md) backed by [`interview/SKILL.md`](interview/SKILL.md) and [`enabled/SKILL.md`](enabled/SKILL.md)
- **Prism Layer**: [`prism/SKILL.md`](prism/SKILL.md) — specialist routing and specialization guidance
- **Optimization Loop**: [`optimization/SKILL.md`](optimization/SKILL.md) — self-improvement and corpus maintenance

## File Structure

```
meta-engine/
├── AGENTS.md                     ← This file (universal entry point)
├── xuan-master/                  ← Xuan Master layer entrypoint
│   ├── SKILL.md
│   ├── 00-entry/
│   │   └── SKILL.md             ← Xuan Master core catalog + 53 scene combos
│   ├── 001-layered-architecture/
│   │   └── SKILL.md             ← Model content
│   ├── 002-flow-model/
│   ├── ...
│   └── 027-ai-native-mindset/SKILL.md
├── archon/                       ← Archon layer entrypoint
│   └── SKILL.md
├── prism/                        ← Prism layer entrypoint + future specialist packs
│   ├── SKILL.md
│   └── domains/
├── enabled/                      ← Archon execution engine implementation
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── interview/                    ← Archon calibration protocol implementation
│   └── SKILL.md
└── optimization/                 ← Self-improvement
    ├── SKILL.md
    └── scripts/
```

## Design Philosophy

- **One model, one file** — Each SKILL.md is self-contained and independently loadable
- **Agent-agnostic** — No dependency on any specific agent's tool system
- **Pipeline architecture** — Models compose via Unix-style pipes: output of A feeds into B
- **Standardized structure** — Every model: Definition → Cross-domain mappings → Core principles → Practice points → Case studies → Exercises
- **Self-improving** — The optimization layer continuously audits and patches models

---

*Version: 4.6.1 · Author: Arthur · License: MIT*
