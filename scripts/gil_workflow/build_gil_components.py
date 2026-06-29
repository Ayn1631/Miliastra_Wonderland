from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from create_components import build_components
from extract_structs import extract_structs


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
RESOURCES_DIR = SCRIPTS_DIR / "resources"
DEFAULT_TEMPLATE_GIL = RESOURCES_DIR / "gil_templates" / "Template.gil"


def load_components_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"components": data}
    if not isinstance(data, dict):
        raise ValueError("components JSON must be an object or a component array")
    if "components" not in data:
        raise ValueError("components JSON object must contain a components array")
    return data


def build_workflow_spec(args: argparse.Namespace, structs_json: Path) -> dict[str, Any]:
    components_doc = load_components_json(args.components_json)
    spec: dict[str, Any] = {
        "format": "gil_component_workflow_spec",
        "version": 1,
        "input_gil": str(args.input_gil.resolve()),
        "template_gil": str(args.template_gil.resolve()),
        "template_component": args.template_component,
        "structs_json": str(structs_json.resolve()),
        "output_gil": str(args.output_gil.resolve()),
        "overwrite": args.overwrite,
        "components": components_doc["components"],
    }
    if "id_policy" in components_doc:
        spec["id_policy"] = components_doc["id_policy"]
    else:
        spec["id_policy"] = {
            "component_definition_start": args.component_definition_start,
            "component_index_start": args.component_index_start,
            "value_ref_start": args.value_ref_start,
        }
    return spec


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a processed .gil from a map .gil and a components/variables JSON."
    )
    parser.add_argument("input_gil", type=Path, help="input map/save .gil")
    parser.add_argument("components_json", type=Path, help="components and variables JSON")
    parser.add_argument("output_gil", type=Path, help="output processed .gil")
    parser.add_argument(
        "--template-gil",
        type=Path,
        default=DEFAULT_TEMPLATE_GIL,
        help="GIL that contains Template component with all variable type templates",
    )
    parser.add_argument("--template-component", default="Template")
    parser.add_argument("--structs-json", type=Path, help="where to write/read extracted structs JSON")
    parser.add_argument("--spec-output", type=Path, help="where to write generated workflow spec")
    parser.add_argument("--component-definition-start", type=int, default=1077940000)
    parser.add_argument("--component-index-start", type=int, default=1077950000)
    parser.add_argument("--value-ref-start", type=int, default=1075000000)
    parser.add_argument("--overwrite", action="store_true", help="overwrite output_gil if it already exists")
    args = parser.parse_args()

    if not args.input_gil.exists():
        raise FileNotFoundError(f"input GIL not found: {args.input_gil}")
    if not args.components_json.exists():
        raise FileNotFoundError(f"components JSON not found: {args.components_json}")
    if not args.template_gil.exists():
        raise FileNotFoundError(f"template GIL not found: {args.template_gil}")

    structs_json = args.structs_json or args.output_gil.with_suffix(".structs.json")
    spec_output = args.spec_output or args.output_gil.with_suffix(".workflow.json")

    structs = extract_structs(args.input_gil)
    structs_json.parent.mkdir(parents=True, exist_ok=True)
    structs_json.write_text(
        json.dumps(structs, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    spec = build_workflow_spec(args, structs_json)
    spec_output.parent.mkdir(parents=True, exist_ok=True)
    spec_output.write_text(
        json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = build_components(spec_output)
    print(
        json.dumps(
            {
                "input_gil": str(args.input_gil),
                "components_json": str(args.components_json),
                "structs_json": str(structs_json),
                "workflow_spec": str(spec_output),
                "output_gil": summary["output"],
                "generated_count": summary["generated_count"],
                "warnings": summary["warnings"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
