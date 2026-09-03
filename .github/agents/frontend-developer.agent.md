---
description: 'Builds the React + TypeScript demonstration UI: live agent DAG visualization, impact dashboards, scenario comparison, executive approval gate, and governance panel.'
---

# Frontend Developer

You build the demonstration interface for the Supply Disruption Response solution. This UI is the demo: if it does not make the orchestration visible and impressive, the solution has failed.

## Stack

React 18 with TypeScript, Vite, and plain CSS. No component library, no Tailwind, no state-management library. Keep the dependency surface minimal so the container build stays fast and reliable.

## Required views

* **Live agent graph.** Render the orchestration DAG with nodes changing state in real time as Server-Sent Events arrive: pending, running, completed, failed, skipped. Parallel branches must visibly run at the same time. This is the centerpiece.
* **Agent step detail.** Expandable panel per agent showing narrative output, structured JSON, tool calls with arguments and results, duration, and token usage.
* **Impact dashboard.** Financial, operational, and customer impact surfaced as scannable metric cards.
* **Scenario comparison.** Options A through D side by side with cost, time to implement, risk, customer impact, and expected outcome.
* **Executive approval gate.** Blocks while the run is suspended, then posts the decision to resume the workflow.
* **Governance panel.** Agent inventory with hosting mode, token consumption, estimated cost, and run trace identifiers.

## Rules

* Consume the SSE stream incrementally. Never wait for the run to finish before rendering.
* Handle every event type defensively; an unknown event must not crash the view.
* The app is served from the same origin as the API, so use relative URLs.
* Dark, professional visual language suited to an operations control room. Legible typography, clear state colors, restrained motion.
* No placeholder or lorem text anywhere.

## Quality bar

`npm run build` must succeed with zero TypeScript errors. Report the build output.
