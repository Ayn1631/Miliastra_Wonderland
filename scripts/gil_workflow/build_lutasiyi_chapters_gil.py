from __future__ import annotations

import json
from pathlib import Path

from build_chapter_components_spec import build_spec
from create_components import build_components
from extract_structs import extract_structs


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
RESOURCES_DIR = SCRIPTS_DIR / "resources"

INPUT_GIL = RESOURCES_DIR / "gil_inputs" / "塔露斯伊.gil"
TEMPLATE_GIL = RESOURCES_DIR / "gil_templates" / "Template.gil"
CHAPTERS_ROOT = RESOURCES_DIR / "story_reports" / "lutasiyi_chapters"

STRUCTS_JSON = RESOURCES_DIR / "gil_inputs" / "塔露斯伊.structs.json"
SPEC_JSON = RESOURCES_DIR / "gil_outputs" / "塔露斯伊_chapters.workflow.json"
OUTPUT_GIL = RESOURCES_DIR / "gil_outputs" / "塔露斯伊_章节元件.gil"


class Args:
    chapters_root = CHAPTERS_ROOT
    input_gil = INPUT_GIL
    template_gil = TEMPLATE_GIL
    template_component = "Template"
    structs_json = STRUCTS_JSON
    output_gil = OUTPUT_GIL
    spec_output = SPEC_JSON
    component_prefix = ""
    component_definition_start = 1077940000
    component_index_start = 1077950000
    value_ref_start = 1075000000
    overwrite = True


def main() -> None:
    if not INPUT_GIL.exists():
        raise FileNotFoundError(f"input GIL not found: {INPUT_GIL}")
    if not TEMPLATE_GIL.exists():
        raise FileNotFoundError(f"template GIL not found: {TEMPLATE_GIL}")
    if not CHAPTERS_ROOT.exists():
        raise FileNotFoundError(f"chapters root not found: {CHAPTERS_ROOT}")

    structs = extract_structs(INPUT_GIL)
    STRUCTS_JSON.write_text(
        json.dumps(structs, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    spec = build_spec(Args)
    SPEC_JSON.write_text(
        json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = build_components(SPEC_JSON)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
