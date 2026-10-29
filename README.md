# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

<!-- template:begin -->
> **This is a GitHub template repository** for projects driven by the
> [PDCA quality cycle](https://github.com/eduralph/pdca-harness). It holds everything
> [project-template](https://github.com/eduralph/project-template) holds, with
> [wyrd](https://github.com/getwyrd/wyrd) as the reference:
>
> - the design-documentation layout: four document classes under `docs/design/`,
>   governance under `docs/governance/`, and the `docs-immutability` check;
> - the PR rules: DCO sign-off (`dco`) and a linked issue on every PR
>   (`require-linked-issue`), plus a contributing guide that points at the
>   [shared one](https://github.com/eduralph/.github/blob/main/CONTRIBUTING.md);
> - issue handling: bug and enhancement templates, the `new` label kept in step with the
>   milestone, and automated priority triage (ADR-0005) that stays off until it is set up;
> - SECURITY.md, Dependabot, the agent rules in AGENTS.md and Claude Code permissions;
> - hardened workflows: every action pinned to a commit hash, no credentials left after
>   checkout, CodeQL code scanning, and a weekly OpenSSF Scorecard run.
>
> On top of that it adds the PDCA parts: one milestone per planned release, and the standard
> setup for the companion **instance** repo that runs the cycle (`pdca/`). The instance is
> rendered from `pdca-harness`; this repo keeps only the product.
>
> Each file still to be written carries a **How to fill this in** block.
>
> ### Start a new project
>
> ```bash
> gh repo create <owner>/<name> --public --template eduralph/pdca-project-template \
>   --description "<one line>" --clone
> cd <name>
> scripts/init-repo.sh          # asks three questions, fills placeholders, applies settings
> scripts/init-instance.sh      # renders ../<name>-pdca with the standard PDCA setup
> ```
>
> `init-repo.sh` asks for the license (Apache-2.0 by default), the contact address for
> conduct and policy reports, and the package ecosystem for Dependabot. It replaces the
> `{{…}}` placeholders and commits and pushes that once to `main`, removing this block. It
> then creates the labels and the first milestone (`Milestone 0.1.0`), deletes branches after
> merge, turns on the security settings (vulnerability reporting, Dependabot security
> updates, secret scanning with push protection and generic-secret patterns, CodeQL code
> scanning, a read-only Actions token, the immutable OIDC subject), and protects `main` (PRs
> required; `dco`, `docs-check`, `docs-immutability`, `gate` and `require-linked-issue`
> required; admins included). GitHub doesn't copy labels, milestones, settings or protection
> rules from a template, which is why the script exists. At the end it prints what is left to
> do by hand.
>
> `init-instance.sh` runs `copier copy` from pdca-harness into `../<name>-pdca` with the
> answers in `pdca/copier-answers.yml`, applies `pdca/pdca.standard.toml` to its
> `pdca.toml`, and fills the parts of its `docs/INTEGRATION.md` that this template already
> answers. It leaves the result uncommitted for you to review; see [`pdca/`](pdca/README.md).
> Once the instance is set up, delete `pdca/` and `scripts/init-instance.sh` from this repo.
>
> Changes to the template itself are tested by `template-test`, which runs `init-repo.sh`
> against a stub `gh` (`.github/template-test/`). It runs only in the template repo.
<!-- template:end -->

## Status

Early. See the [open milestones](https://github.com/{{OWNER}}/{{PROJECT_NAME}}/milestones) for
what is in work; the lowest one is the next release.

## Documentation

[`docs/`](docs/README.md) is the map. Design documents are in [`docs/design/`](docs/design/README.md):
architecture, decision records (ADRs), proposals and specifications. Governance and the Code
of Conduct are in [`docs/governance/`](docs/governance/GOVERNANCE.md).

## Development process

Changes to this repo are driven by a PDCA quality cycle (Plan → Do → Check → Act) run from
the companion instance repo
[{{PROJECT_NAME}}-pdca](https://github.com/{{OWNER}}/{{PROJECT_NAME}}-pdca), rendered from
[pdca-harness](https://github.com/eduralph/pdca-harness). The instance keeps the per-issue
result bundles and the process log; this repo keeps the product and its design documents,
which the instance reads in place.

Every change starts from an issue on an open milestone and ships as one pull request that
links it. See [CONTRIBUTING.md](CONTRIBUTING.md) and, for coding agents, [AGENTS.md](AGENTS.md).

## Releases

Versions are git tags of the form `vX.Y.0` — a minor bump per release (patch stays `0`);
each tag is annotated with its release notes (`git show vX.Y.0`). Each release is one
**GitHub milestone**; the implementation arc (the first proposal in
[`docs/design/proposals/`](docs/design/proposals/README.md)) plans them:

- **Every planned release has an open milestone.** The first is opened at setup, the rest
  when the implementation arc plans them. The **lowest open milestone is the next version to
  ship**; the higher ones collect work already known to belong to a later release.
- **A new issue is filed against the milestone of the release it belongs to**, or the lowest
  open one when that is unclear. An issue with no milestone carries the `new` label (set by
  the Issue triage workflow) until it is triaged.
- **When a version is released** — cut as a `vX.Y.0` tag — its milestone is **closed**, and
  the next open milestone becomes the next version to ship. A release beyond the arc gets
  its milestone when it is planned, by a proposal that extends the arc.

## License

Copyright © {{YEAR}} {{AUTHOR}}.

{{PROJECT_NAME}} is licensed under the **{{LICENSE_NAME}}** ([LICENSE](LICENSE)).

Contributions are accepted under the same license and gated on the
[Developer Certificate of Origin](DCO). Sign off commits with `git commit -s`.
