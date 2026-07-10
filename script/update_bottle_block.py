from __future__ import annotations

import json
from pathlib import Path
import re
import sys


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: update_bottle_block.py FORMULA_PATH BOTTLE_JSON ROOT_URL"
        )

    formula_path = Path(sys.argv[1])
    bottle_json_path = Path(sys.argv[2])
    root_url = sys.argv[3]

    bottle_data = _load_bottle_data(bottle_json_path)
    bottle_block = _render_bottle_block(bottle_data, root_url)

    original = formula_path.read_text()
    updated = _replace_bottle_block(original, bottle_block)
    if updated != original:
        formula_path.write_text(updated)
    return 0


def _load_bottle_data(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text())
    bottle = _find_bottle_data(payload)
    if bottle is None:
        raise ValueError("unexpected bottle JSON format")
    return bottle


def _find_bottle_data(value: object) -> dict[str, object] | None:
    if isinstance(value, dict):
        bottle = value.get("bottle")
        if isinstance(bottle, dict) and isinstance(bottle.get("files"), dict):
            return bottle
        if isinstance(value.get("files"), dict):
            return value  # already at the bottle object level
        for nested in value.values():
            found = _find_bottle_data(nested)
            if found is not None:
                return found
        return None

    if isinstance(value, list):
        for item in value:
            found = _find_bottle_data(item)
            if found is not None:
                return found

    return None


def _render_bottle_block(bottle_data: dict[str, object], root_url: str) -> str:
    files = bottle_data["files"]
    if not isinstance(files, dict):
        raise ValueError("unexpected bottle file data")

    lines = ["  bottle do", f'    root_url "{root_url}"']
    for tag, payload in sorted(files.items()):
        if not isinstance(payload, dict):
            continue
        cellar = _render_cellar(str(payload["cellar"]))
        sha256 = payload["sha256"]
        lines.append(f'    sha256 cellar: {cellar}, {tag}: "{sha256}"')
    lines.append("  end")
    return "\n".join(lines)


def _render_cellar(value: str) -> str:
    normalized = value.strip().lstrip(":")
    if normalized in {"any", "any_skip_relocation"}:
        return f":{normalized}"
    return f'"{value}"'


def _replace_bottle_block(contents: str, bottle_block: str) -> str:
    existing = re.compile(r"(?ms)^  bottle do\n.*?\n  end\n")
    if existing.search(contents):
        return existing.sub(f"{bottle_block}\n", contents, count=1)

    anchor = '  license "MIT"\n'
    if anchor not in contents:
        raise ValueError("could not find license anchor for bottle block")
    return contents.replace(anchor, f'{anchor}\n{bottle_block}\n', 1)


if __name__ == "__main__":
    raise SystemExit(main())
