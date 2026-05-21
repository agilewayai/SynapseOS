---
name: archon
description: "Archon enabler entrypoint — the calibration, orchestration, actions, and structured-generation layer above Xuan Master. Use when an agent needs problem clarification, execution flow, or output-generation abilities such as document and PDF workflows."
version: 0.1.0
author: Arthur
---

# Archon

Archon is the enabler layer of the skills stack. It sits above Xuan Master and turns a clarified problem into an execution flow, action plan, or generated output.

## Use This Layer When

- the problem needs clarification before deep reasoning
- the agent needs orchestration across multiple models
- the workflow includes actions, output generation, or document/PDF-style deliverables

## Current Surfaces

- [`interview/SKILL.md`](interview/SKILL.md): calibration and structured interview protocol
- [`enabled/SKILL.md`](enabled/SKILL.md): orchestration, synthesis, and generation workflow

## Load Pattern

1. If the problem is vague or under-specified, start with [`interview/SKILL.md`](interview/SKILL.md).
2. Route clarified work into [`enabled/SKILL.md`](enabled/SKILL.md) for orchestration, actions, and output generation.
3. Load [`../xuan-master/SKILL.md`](../xuan-master/SKILL.md) when direct core-model reasoning is needed.
4. Hand deeper specialist routing to [`../prism/SKILL.md`](../prism/SKILL.md) when the work must branch into domain-specific execution.

## Related Layers

- [`../xuan-master/SKILL.md`](../xuan-master/SKILL.md): core model layer
- [`../prism/SKILL.md`](../prism/SKILL.md): specialist layer
- [`../optimization/SKILL.md`](../optimization/SKILL.md): cross-cutting quality loop
