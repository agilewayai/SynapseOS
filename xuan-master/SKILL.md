---
name: xuan-master
description: "Xuan Master core entrypoint — the meta-cognition layer and 27-model knowledge kernel. Use when an agent needs the core cognitive models, scene routing, and the foundational reasoning surface of the stack."
version: 0.1.0
author: Arthur
---

# Xuan Master

Xuan Master is the core of the skills stack. It provides the meta-cognition layer, the 27 cognitive models, and the catalog that routes a problem to the right models.

## Use This Layer When

- you need the core cognitive models directly
- you need scene-based model routing
- you want the reasoning kernel without execution or specialist behavior

## Current Surfaces

- [`00-entry/SKILL.md`](00-entry/SKILL.md): catalog, scene combinations, and model routing
- `001-layered-architecture/` through `027-ai-native-mindset/`: the 27 model directories

## Load Pattern

1. Start with [`00-entry/SKILL.md`](00-entry/SKILL.md).
2. Load the relevant model `SKILL.md` files from the numbered directories.
3. If the problem needs orchestration, actions, or structured generation, hand off to [`../archon/SKILL.md`](../archon/SKILL.md).
4. If the work needs deeper domain-specific routing, hand off to [`../prism/SKILL.md`](../prism/SKILL.md).

## Related Layers

- [`../archon/SKILL.md`](../archon/SKILL.md): execution, calibration, actions, generation
- [`../prism/SKILL.md`](../prism/SKILL.md): specialist routing and deeper domain mapping
- [`../optimization/SKILL.md`](../optimization/SKILL.md): cross-cutting quality and evolution loop
