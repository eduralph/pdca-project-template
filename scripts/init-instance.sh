#!/usr/bin/env bash
# Render the PDCA instance repo for a project created from pdca-project-template.
#
#   scripts/init-repo.sh          # first: fills the placeholders this script reads
#   scripts/init-instance.sh      # renders ../<name>-pdca next to this checkout
#
# This script:
#   1. asks for the gate runner the instance delegates to (PDCA_GATES_RUNNER, e.g.
#      "cargo xtask" or "./engine/nox.sh"; blank = gate commands written inline);
#   2. runs `copier copy` from pdca-harness (PDCA_HARNESS, default gh:eduralph/pdca-harness;
#      its latest release unless PDCA_HARNESS_REF names another) into
#      ../<name>-pdca (PDCA_INSTANCE_DIR) with the answers in pdca/copier-answers.yml;
#   3. applies pdca/pdca.standard.toml to its pdca.toml, adds the security-review role
#      prompt and fills the parts of its docs/INTEGRATION.md this template already answers
#      (pdca/apply.py);
#   4. runs `git init` there and stops, leaving everything uncommitted for you to review.
#
# It never touches GitHub; the last lines it prints say how to publish the instance.
set -euo pipefail

die() { echo "init-instance: $*" >&2; exit 1; }

command -v copier >/dev/null || die "copier is not installed (pipx install copier)"
command -v python3 >/dev/null || die "python3 is not installed"
python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))' || die "python3 >= 3.11 is needed (tomllib)"
cd "$(git rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git checkout"
[ -f pdca/copier-answers.yml ] || die "pdca/ is gone; the instance was set up already"
if grep -q '{{[A-Z_]*}}' pdca/copier-answers.yml pdca/pdca.standard.toml pdca/integration.toml; then
  die "placeholders not filled yet; run scripts/init-repo.sh first"
fi

NAME="$(basename "$PWD")"
DEST="${PDCA_INSTANCE_DIR:-../$NAME-pdca}"
HARNESS="${PDCA_HARNESS:-gh:eduralph/pdca-harness}"
[ -e "$DEST" ] && die "$DEST exists already; remove it or set PDCA_INSTANCE_DIR"

# --- 1. gate runner -----------------------------------------------------------------
RUNNER="${PDCA_GATES_RUNNER-}"
if [ -z "${PDCA_GATES_RUNNER+set}" ] && [ -t 0 ]; then
  read -r -p "Gate runner the instance delegates to (e.g. 'cargo xtask'; blank = inline): " RUNNER
fi

# --- 2. render ----------------------------------------------------------------------
echo "Rendering $DEST from $HARNESS"
args=(copy --defaults --quiet --data-file pdca/copier-answers.yml --data "gates_runner=$RUNNER")
[ -n "${PDCA_HARNESS_REF:-}" ] && args+=(--vcs-ref "$PDCA_HARNESS_REF")
copier "${args[@]}" "$HARNESS" "$DEST"

# --- 3. standard setup --------------------------------------------------------------
echo "Applying the standard setup"
python3 -I pdca/apply.py "$DEST"

# --- 4. hand over -------------------------------------------------------------------
git -C "$DEST" init -q -b main
CLI="$(sed -n 's/^cli_name: *//p' "$DEST/.copier-answers.yml" | tr -d "'\"")"
OWNER="$(git remote get-url origin | sed -E 's#^.*[:/]([^/]+)/[^/]+$#\1#')"
cat <<EOF

Done. $DEST is rendered and uncommitted. Next:
  cd $DEST
  make install && $CLI doctor       # checks the toolchain and ../$NAME
  # read pdca.toml's standard block at the end, and docs/INTEGRATION.md; fill its TODOs
  git add -A && git commit -s -m "chore: render from pdca-harness"
  gh repo create $OWNER/$(basename "$DEST") --public --source . --push
Then delete pdca/ and scripts/init-instance.sh from this repo in a PR.
EOF
