---
name: prism
description: "Prism specialist entrypoint — the domain-routing and specialist-mapping layer of the stack. Use when generic reasoning or orchestration must branch into deeper, more specialized domain work."
version: 0.1.0
author: Arthur
---

# Prism

Prism is the specialist layer of the skills stack. It routes work from the generic core and enabler layers into deeper domain-specific paths and more specialized execution.

## Use This Layer When

- a problem needs deeper domain routing than the generic layer can provide
- an agent must map work into specialist subdomains or domain-specific methods
- the next step is not more orchestration, but more specialization

## Current Surfaces

- this file as the layer entrypoint
- [`domains/README.md`](domains/README.md): placeholder surface for future specialist domain packs
- [`../.aries_harness/references/domain/README.md`](../.aries_harness/references/domain/README.md): current design placeholder for future domain packages

## Current Status

Prism is now materialized as a dedicated layer entrypoint. It is intentionally light today: the specialist-layer contract is explicit, but the deeper domain packs are still future work.

## Load Pattern

1. Use [`../xuan-master/SKILL.md`](../xuan-master/SKILL.md) for core model routing.
2. Use [`../archon/SKILL.md`](../archon/SKILL.md) when the work needs orchestration or actions.
3. Use Prism when the next step is deeper domain mapping or specialist routing beyond those generic layers.

## Related Layers

- [`../xuan-master/SKILL.md`](../xuan-master/SKILL.md): core meta-cognition layer
- [`../archon/SKILL.md`](../archon/SKILL.md): enabler layer
- [`../optimization/SKILL.md`](../optimization/SKILL.md): cross-cutting quality loop
