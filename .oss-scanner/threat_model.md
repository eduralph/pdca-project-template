# Threat model: {{PROJECT_NAME}}

Reviewer-facing summary of what an attacker can reach and how bad each outcome is. The PDCA
security-review leaf reads this file first and rates every patch against it, so keep it
current: a change that adds an untrusted input or moves a trust boundary updates this file
in the same PR. Where the design and the code differ, this file describes the code.

_Fill in each section; delete the italic prompts. Models:
[wyrd](https://github.com/getwyrd/wyrd/blob/main/.oss-scanner/threat_model.md),
[nl-shell](https://github.com/eduralph/nl-shell/blob/main/.oss-scanner/threat_model.md)._

## What this project does

_The components and how data flows between them, in a few paragraphs or a small diagram._

## Where untrusted input enters

Treat all of the following as attacker-controlled:

1. _Each input an attacker can control: where it enters, who controls it, which component
   parses it._

Trusted: _what is not attacker-controlled, and why._

## What must hold

- _The properties a finding breaks. These are what the security review checks._

## Components that matter most

In order: _the components, most exposed first._

Lower priority: _test tools, build automation._

Out of scope: _generated code; third-party code (report a dependency bug only if this
project's use of it is what makes it exploitable)._

## Known gaps: do not report these on their own

- _Each known, accepted gap, and what about it is still in scope._

## How to exercise it

_The test command, how to run the system locally, and how to drive the exposed inputs._

## How we rate severity

- **Critical:** _…_
- **High:** _…_
- **Medium:** _…_
- **Low:** _…_

A clean reproducer matters more than a severity label. The best form is a failing test in
the style of the existing ones.
