from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def story_nodes_from_report(report: dict[str, Any]) -> list[dict[str, Any]]:
    if str(report.get("structId")) != "1077936130":
        raise ValueError(f"report is not Story struct: {report.get('structId')}")
    values = report.get("value", [])
    if len(values) != 1 or values[0].get("param_type") != "StructList":
        raise ValueError("Story report must contain exactly one StructList value")
    struct_list = values[0].get("value", {})
    if str(struct_list.get("structId")) != "1077936129":
        raise ValueError(f"Story_List is not StoryNode struct list: {struct_list.get('structId')}")

    nodes: list[dict[str, Any]] = []
    for item in struct_list.get("value", []):
        node_value = item.get("value", {})
        fields = node_value.get("value", [])
        if len(fields) != 3:
            raise ValueError("StoryNode report item must contain status, str and next")
        nodes.append(
            {
                "status": str(fields[0].get("value", "")),
                "str": [str(value) for value in fields[1].get("value", [])],
                "next": [int(value) for value in fields[2].get("value", [])],
            }
        )
    return nodes


def chapter_title(chapter_dir: Path) -> str:
    manifest = chapter_dir / "report_manifest.json"
    if not manifest.exists():
        return chapter_dir.name
    data = json.loads(manifest.read_text(encoding="utf-8"))
    source = str(data.get("source", ""))
    stem = Path(source).stem
    return stem or chapter_dir.name


def build_component_for_chapter(chapter_dir: Path, component_prefix: str = "") -> dict[str, Any]:
    report_files = [
        path
        for path in sorted(chapter_dir.glob("report_*.json"))
        if path.name != "report_manifest.json"
    ]
    if not report_files:
        raise ValueError(f"no report_*.json files found in {chapter_dir}")

    section_names = [str(index) for index in range(1, len(report_files) + 1)]
    component_name = f"{component_prefix}{chapter_dir.name}" if component_prefix else chapter_dir.name
    variables: list[dict[str, Any]] = [
        {
            "name": "小节",
            "type": "str_list",
            "value": section_names,
        }
    ]

    for section_name, report_path in zip(section_names, report_files):
        report = load_report(report_path)
        variables.append(
            {
                "name": section_name,
                "type": "struct",
                "struct": "Story",
                "value": {
                    "__struct_types__": {
                        "Story_List": "StoryNode"
                    },
                    "Story_List": story_nodes_from_report(report),
                },
                "source_report": str(report_path),
            }
        )

    return {
        "name": component_name,
        "chapter_dir": str(chapter_dir),
        "chapter_title": chapter_title(chapter_dir),
        "section_count": len(section_names),
        "variables": variables,
    }


def build_spec(args: argparse.Namespace) -> dict[str, Any]:
    chapters_root = args.chapters_root.resolve()
    chapter_dirs = sorted(path for path in chapters_root.iterdir() if path.is_dir())
    if not chapter_dirs:
        raise ValueError(f"no chapter directories found in {chapters_root}")

    return {
        "format": "gil_component_workflow_spec",
        "version": 1,
        "input_gil": str(args.input_gil.resolve()),
        "template_gil": str(args.template_gil.resolve()),
        "template_component": args.template_component,
        "structs_json": str(args.structs_json.resolve()),
        "output_gil": str(args.output_gil.resolve()),
        "overwrite": args.overwrite,
        "id_policy": {
            "component_definition_start": args.component_definition_start,
            "component_index_start": args.component_index_start,
            "value_ref_start": args.value_ref_start,
        },
        "source": {
            "chapters_root": str(chapters_root),
            "chapter_count": len(chapter_dirs),
        },
        "components": [
            build_component_for_chapter(chapter_dir, args.component_prefix)
            for chapter_dir in chapter_dirs
        ],
    }


def main() -> None:
    scripts_dir = Path(__file__).resolve().parents[1]
    default_template_gil = scripts_dir / "resources" / "gil_templates" / "Template.gil"
    parser = argparse.ArgumentParser(
        description="Build a GIL workflow spec: one component per chapter, one Story variable per report file."
    )
    parser.add_argument("--chapters-root", type=Path, required=True)
    parser.add_argument("--input-gil", type=Path, required=True)
    parser.add_argument("--template-gil", type=Path, default=default_template_gil)
    parser.add_argument("--template-component", default="Template")
    parser.add_argument("--structs-json", type=Path, required=True)
    parser.add_argument("--output-gil", type=Path, required=True)
    parser.add_argument("--spec-output", type=Path, required=True)
    parser.add_argument("--component-prefix", default="")
    parser.add_argument("--component-definition-start", type=int, default=1077940000)
    parser.add_argument("--component-index-start", type=int, default=1077950000)
    parser.add_argument("--value-ref-start", type=int, default=1075000000)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    spec = build_spec(args)
    args.spec_output.parent.mkdir(parents=True, exist_ok=True)
    args.spec_output.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "spec_output": str(args.spec_output),
                "chapter_count": len(spec["components"]),
                "section_counts": {
                    component["name"]: component["section_count"]
                    for component in spec["components"]
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
