# PDCA instance setup

This folder sets up the companion instance repo, `{{PROJECT_NAME}}-pdca`, that runs the PDCA
quality cycle against this project. It is used once by `scripts/init-instance.sh`; delete the
folder and the script afterwards.

The instance itself comes from [pdca-harness](https://github.com/eduralph/pdca-harness), which
renders it with copier (a tool that fills a template from a list of answers). What this folder
adds is the setup the existing own-repo instances (wyrd-pdca, nl-shell-pdca, autobook-pdca,
pdca-pdca) all ended up with after turning settings on by hand:

| File | What it holds |
|---|---|
| `copier-answers.yml` | The copier answers: own-repo, Claude builds, Codex reviews, GitHub tracker, `main`, real leaves instead of stubs. |
| `pdca.standard.toml` | Settings merged into the instance's `pdca.toml`: a 16G memory bound per leaf, the sizer on, Opus from the 2nd build attempt, results committed, the planner reading this repo's issues, the `adversary`, `security-review` and `plan-reviewer` advisory reviewers, and doctor checks for the sibling checkout and the threat model. |
| `agents/security-review.md` | The security reviewer's role prompt. It rates each patch against `.oss-scanner/threat_model.md` in this repo. |
| `integration.toml` | Answers for the instance's `docs/INTEGRATION.md` that this template already gives: how PRs link issues, milestones as the release field, no maintenance branches, accepted docs superseded rather than edited, design docs read in place, no upstream, commit conventions and governance. |
| `apply.py` | Applies the three files above to a rendered instance. |

Two of these are stopgaps: the advisory reviewers move into a copier answer with
[pdca-harness#795](https://github.com/eduralph/pdca-harness/issues/795), and the
security-review prompt into the harness with
[pdca-harness#794](https://github.com/eduralph/pdca-harness/issues/794). `apply.py` already
keeps the harness's version when one exists, so the stopgaps can be dropped from this
template once those land.

## Use

```bash
scripts/init-instance.sh      # after scripts/init-repo.sh
```

It asks for the gate runner the instance delegates to (for example `cargo xtask`, or blank to
write gate commands inline), renders `../{{PROJECT_NAME}}-pdca` from the latest pdca-harness
release, applies this folder, runs `git init` there and stops. Nothing is committed or pushed;
the script prints the steps to check and publish the instance. Settings it can't apply (because
the rendered file changed) are listed for you to set by hand.

Environment overrides: `PDCA_GATES_RUNNER`, `PDCA_INSTANCE_DIR` (default
`../{{PROJECT_NAME}}-pdca`), `PDCA_HARNESS` (default `gh:eduralph/pdca-harness`, or a local
checkout) and `PDCA_HARNESS_REF` (a tag or commit instead of the latest release).

Change anything here before running the script if this project differs, for example a
`code-review` advisory leaf (wyrd-pdca and pdca-pdca run one) or `[leaves.sandbox]
network_access = true` for gates that download dependencies.
