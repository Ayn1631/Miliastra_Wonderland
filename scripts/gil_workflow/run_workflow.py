from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from create_components import build_components
from extract_structs import extract_structs


def load_spec(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_workflow(spec_path: Path) -> dict[str, Any]:
    spec = load_spec(spec_path)
    base_dir = spec_path.parent
    input_gil = (base_dir / spec["input_gil"]).resolve()

    structs_json = spec.get("structs_json")
    if structs_json:
        structs_path = (base_dir / structs_json).resolve()
    else:
        structs_path = input_gil.with_suffix(".structs.json")
        spec["structs_json"] = str(structs_path.relative_to(base_dir))
        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    structs = extract_structs(input_gil)
    structs_path.parent.mkdir(parents=True, exist_ok=True)
    structs_path.write_text(json.dumps(structs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    generated = build_components(spec_path)
    return {
        "spec": str(spec_path),
        "input_gil": str(input_gil),
        "structs_json": str(structs_path),
        "struct_count": structs["struct_count"],
        "output_gil": generated["output"],
        "generated_count": generated["generated_count"],
        "summary": generated,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract structs and create components in one workflow.")
    parser.add_argument("spec", type=Path, help="workflow/component generation JSON")
    args = parser.parse_args()
    print(json.dumps(run_workflow(args.spec), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
