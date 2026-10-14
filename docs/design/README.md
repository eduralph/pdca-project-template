---
created: {{DATE}}
type: index
tags:
  - index
---
# {{PROJECT_NAME}} — design documentation

The design documentation is organized into four classes, each with its own purpose and
change process. The split follows [wyrd](https://github.com/getwyrd/wyrd/tree/main/docs/design):
some documents describe the system and change with it, some record decisions and never
change, and some are contracts that other code must honour.

## The four document classes

| Class | Location | Nature | Change process |
|-------|----------|--------|----------------|
| 1. Specifications | `specs/` | Normative, versioned | Strict; a stable version is never edited, only replaced by a new version |
| 2. Architecture overview | `architecture/` | Descriptive, living | Edited continuously; always describes the current system |
| 3. Decision records (ADRs) | `adr/` | Immutable history | Append-only; superseded, never edited |
| 4. Enhancement proposals | `proposals/` | The change process | Draft → accepted → implemented; accepted records are immutable |

### 1. Specifications (`specs/`)

Contracts that more than one piece of code depends on — a file format, a wire format, a log
schema — written in RFC 2119 language (MUST / SHOULD / MAY). Write one before a second
consumer depends on the format.

### 2. Architecture overview (`architecture/`)

A trimmed [arc42](https://arc42.org/) structure (a standard set of chapters for describing a
software architecture). It describes the system as it currently is, and must not lag the
code: "update the architecture doc" is a legitimate merge requirement on a PR that changes
structure. Before there is code, it describes the design the code is being built to.

### 3. Architecture Decision Records (`adr/`)

Short, numbered records of *why* a decision was made, so the same debate is not reopened in
every issue. An ADR is never edited after acceptance; a later ADR supersedes it. Format: a
lightweight [Nygard-style](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
template. See [ADR-0001](adr/0001-record-architecture-decisions.md).

### 4. Enhancement proposals (`proposals/`)

How larger changes and milestone plans are proposed (modeled on Kubernetes KEPs and Rust
RFCs). A proposal moves from `draft/` to `accepted/` and carries motivation, design,
alternatives and graduation criteria. Proposal 0001 is usually the implementation arc — the
milestone plan the GitHub milestones point to.

The fill-in templates for all four classes are in [`templates/`](templates/README.md).

## Conventions

- **Diagrams as code.** Diagrams are Mermaid source in the Markdown, never binary exports.
- **Docs live with code.** Documentation is in the same repository as the code it describes
  and is reviewed in the same pull requests.
- **ADR-first habit.** When a design question is settled, the output is an ADR, not an issue
  comment.
- **Security has its own file.** The threat model is
  [`.oss-scanner/threat_model.md`](../../.oss-scanner/threat_model.md); the PDCA
  security-review leaf rates every patch against it.

## Reading order for newcomers

1. [`architecture/01-introduction-and-goals.md`](architecture/01-introduction-and-goals.md) — what this is and why.
2. [`architecture/08-crosscutting-concepts.md`](architecture/08-crosscutting-concepts.md) — the core concepts.
3. [`adr/`](adr/README.md) — the founding decisions.
4. [`architecture/09-build-order-and-roadmap.md`](architecture/09-build-order-and-roadmap.md) — the milestones and where to start.
