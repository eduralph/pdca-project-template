---
created: {{DATE}}
type: adr
status: Accepted
tags:
  - adr
---
# 0002. Apache-2.0 license and DCO sign-off

## Context

The project is public. Contributions need a clear license, and contributors need a
lightweight way to certify they may contribute what they send.

## Decision

The code is licensed under Apache-2.0. Contributions are accepted under the same license and
gated on the Developer Certificate of Origin (`git commit -s`). Third-party material that
ships with the project keeps its own license and is documented in `NOTICE`.

## Consequences

A permissive license with a patent grant, the same as the pdca-harness tooling. No
contributor license agreement is needed. Every commit must carry a `Signed-off-by` trailer.
