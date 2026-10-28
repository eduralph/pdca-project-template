"""Apply this folder's standard setup to a freshly rendered PDCA instance.

    python3 -I pdca/apply.py <instance-dir>

Called by scripts/init-instance.sh after `copier copy`. It edits the instance in place:

1. merges pdca.standard.toml into <instance>/pdca.toml, keeping the rendered file's
   comments (see the header of pdca.standard.toml for the rules), then checks with
   tomllib that every standard value came out as written;
2. adds the security-review role prompt (agents/ and its .claude/agents/ wrapper) unless
   the harness already shipped one;
3. fills the docs/INTEGRATION.md items listed in integration.toml.

Exits non-zero if pdca.toml would not parse or a value didn't land; a skipped block or an
INTEGRATION.md line that is no longer there is reported, not fatal.
"""

import pathlib
import re
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent
TABLE = re.compile(r"^\[([^\[\]]+)\]\s*(#.*)?$")
ARRAY = re.compile(r"^\[\[([^\[\]]+)\]\]\s*(#.*)?$")
KEY = re.compile(r"^\s*([A-Za-z0-9_-]+)\s*=")


def blocks(text):
    """Split pdca.standard.toml into (kind, name, comment+header+body lines, body lines)."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        lines = para.strip("\n").splitlines()
        heads = [i for i, line in enumerate(lines) if TABLE.match(line) or ARRAY.match(line)]
        if not heads:
            continue  # the file's own header comment
        if len(heads) > 1:
            sys.exit(f"apply: put a blank line between blocks: {lines[heads[1]]}")
        head = lines[heads[0]]
        kind, name = ("array", ARRAY.match(head)[1]) if ARRAY.match(head) else ("table", TABLE.match(head)[1])
        out.append((kind, name.strip(), lines, lines[heads[0] + 1:]))
    return out


def lookup(doc, dotted):
    cur = doc
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def merge_toml(instance):
    path = instance / "pdca.toml"
    text = path.read_text(encoding="utf-8")
    rendered = tomllib.loads(text)
    lines = text.splitlines()
    appended, expected, report = [], [], []

    for kind, name, block, body in blocks((HERE / "pdca.standard.toml").read_text(encoding="utf-8")):
        want = tomllib.loads(f"[{name}]\n" + "\n".join(body)) if kind == "table" else \
            tomllib.loads(f"[[{name}]]\n" + "\n".join(body))
        want = lookup(want, name)
        if kind == "array":
            want = want[0]
            have = lookup(rendered, name) or []
            clash = [e for e in have if e.get("id") == want.get("id")] if "id" in want else have
            if clash:
                report.append(f"kept the instance's own [[{name}]]"
                              + (f" id={want['id']}" if "id" in want else "") + "; standard block skipped")
                continue
            appended.append(block)
            expected.append((kind, name, want))
            continue

        head = next((i for i, line in enumerate(lines)
                     if TABLE.match(line) and TABLE.match(line)[1].strip() == name), None)
        if head is None:
            appended.append(block)
        else:
            end = next((i for i in range(head + 1, len(lines))
                        if TABLE.match(lines[i]) or ARRAY.match(lines[i])), len(lines))
            for line in body:
                if not KEY.match(line):
                    continue
                key = KEY.match(line)[1]
                at = next((i for i in range(head + 1, end)
                           if KEY.match(lines[i]) and KEY.match(lines[i])[1] == key), None)
                if at is None:
                    lines.insert(head + 1, line)
                    end += 1
                else:
                    if lines[at].count("[") != lines[at].count("]"):
                        sys.exit(f"apply: [{name}] {key} spans several lines in pdca.toml; set it by hand")
                    lines[at] = line
        expected.append((kind, name, want))

    out = "\n".join(lines).rstrip("\n") + "\n"
    if appended:
        out += "\n# --- Standard settings from pdca-project-template (pdca/pdca.standard.toml) ---\n"
        out += "".join("\n" + "\n".join(b) + "\n" for b in appended)
    try:
        merged = tomllib.loads(out)
    except tomllib.TOMLDecodeError as e:
        sys.exit(f"apply: merged pdca.toml does not parse ({e}); nothing written")
    for kind, name, want in expected:
        got = lookup(merged, name)
        ok = want in (got or []) if kind == "array" else \
            isinstance(got, dict) and all(got.get(k) == v for k, v in want.items())
        if not ok:
            sys.exit(f"apply: [{name}] did not come out as written; nothing written")
    path.write_text(out, encoding="utf-8")
    print(f"  pdca.toml: {len(expected)} standard blocks applied")
    for line in report:
        print(f"  pdca.toml: {line}")


def add_agents(instance):
    name = instance.name
    for src in sorted((HERE / "agents").glob("*.md")):
        dest = instance / "agents" / src.name
        wrapper = instance / ".claude" / "agents" / src.name
        if dest.exists() or wrapper.exists():
            print(f"  agents/{src.name}: the harness ships one already; kept it")
            continue
        body = src.read_text(encoding="utf-8")
        dest.write_text(body, encoding="utf-8")
        wrapper.write_text(
            "---\n"
            f"name: {src.stem}\n"
            "description: >-\n"
            f"  SECURITY Check reviewer for {name}: reads the patch the way an attacker would\n"
            "  (who controls each input the diff touches and what they can make it do) and rates\n"
            "  findings against the target's own threat model\n"
            "  ($PDCA_TARGET/.oss-scanner/threat_model.md). Advisory only; it never gates.\n"
            "  Execute + read, no write to the fix. Invoke as a configured advisory leaf.\n"
            "tools: Read, Bash, Grep, Glob\n"
            "model: inherit\n"
            "---\n\n" + body, encoding="utf-8")
        print(f"  agents/{src.name} and .claude/agents/{src.name} added")


def fill_integration(instance):
    path = instance / "docs" / "INTEGRATION.md"
    text = path.read_text(encoding="utf-8")
    fills = tomllib.loads((HERE / "integration.toml").read_text(encoding="utf-8"))["fill"]
    done, missing = 0, []
    for fill in fills:
        if fill["replace"] in text:
            done += 1  # filled by an earlier run
        elif text.count(fill["find"]) == 1:
            text = text.replace(fill["find"], fill["replace"], 1)
            done += 1
        else:
            missing.append(fill["find"])
    path.write_text(text, encoding="utf-8")
    print(f"  docs/INTEGRATION.md: {done} of {len(fills)} items filled")
    for line in missing:
        print(f"  docs/INTEGRATION.md: not found, fill by hand: {line[:90]}")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    instance = pathlib.Path(sys.argv[1]).resolve()
    if not (instance / "pdca.toml").is_file():
        sys.exit(f"apply: {instance} has no pdca.toml")
    merge_toml(instance)
    add_agents(instance)
    fill_integration(instance)


if __name__ == "__main__":
    main()
