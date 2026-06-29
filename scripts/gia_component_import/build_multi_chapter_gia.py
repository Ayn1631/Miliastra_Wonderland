from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
VARIABLES_SCRIPT_DIR = SCRIPT_DIR.parent / "gia_component_variables"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(VARIABLES_SCRIPT_DIR))

from import_component_variables import (
    FOOTER_SIZE,
    HEADER_SIZE,
    encode_varint,
    key,
    length_field,
    load_reports,
    report_items,
    serialize_message,
    string_field,
    string_list_payload,
    varint_field,
)
from parse_component_variables import (
    all_fields,
    children,
    extract_variable,
    find_variable_messages,
    first_field,
    parse_component_variables,
    parse_message,
    utf8,
    varint,
)


CHAPTER_NAMES = [
    "第一章",
    "第二章",
    "第三章",
    "第四章",
    "第五章",
    "第六章",
    "第七章",
    "第八章",
    "第九章",
    "第十章",
]


def set_length_delimited_utf8(field: dict[str, Any], value: str) -> None:
    raw = value.encode("utf-8")
    field["utf8"] = value
    field["raw"] = raw
    field["length"] = len(raw)
    field.pop("children", None)
    field["_raw_override"] = raw


def type_ref(type_code: int, struct_id: int | None = None) -> bytes:
    nested = varint_field(1, type_code)
    if struct_id is None:
        nested += length_field(2, b"")
    else:
        nested += length_field(2, varint_field(1, 1) + varint_field(2, struct_id))
    return varint_field(1, type_code) + length_field(2, nested)


def encode_string_list_value(values: list[str]) -> bytes:
    return (
        varint_field(1, 11)
        + length_field(2, varint_field(1, 11) + length_field(2, b""))
        + length_field(21, string_list_payload(values))
    )


def encode_param_slot(param: dict[str, Any]) -> bytes:
    param_type = param["param_type"]
    value = param["value"]
    if param_type == "String":
        return (
            varint_field(1, 6)
            + length_field(2, varint_field(1, 6) + length_field(2, b""))
            + length_field(16, string_list_payload([value]))
        )
    if param_type == "StringList":
        return (
            varint_field(1, 11)
            + length_field(2, varint_field(1, 11) + length_field(2, b""))
            + length_field(21, string_list_payload(value))
        )
    if param_type == "Int32List":
        return (
            varint_field(1, 8)
            + length_field(2, varint_field(1, 8) + length_field(2, b""))
            + length_field(
                18,
                b"".join(length_field(1, encode_varint(int(item))) for item in value),
            )
        )
    raise ValueError(f"unsupported param_type: {param_type}")


def encode_story_node(item: dict[str, Any], node_object_id: int, story_node_struct_id: int) -> bytes:
    node_params = item["value"]["value"]
    payload = (
        b"".join(length_field(1, encode_param_slot(param)) for param in node_params)
        + varint_field(501, story_node_struct_id)
        + length_field(502, varint_field(2, 28) + varint_field(4, node_object_id))
    )
    return (
        varint_field(1, 25)
        + length_field(2, type_ref(25, story_node_struct_id))
        + length_field(35, payload)
    )


def encode_story_value(
    report: dict[str, Any],
    value_ref_id: int,
    node_object_ids: list[int],
    story_list_struct_id: int,
    story_node_struct_id: int,
) -> bytes:
    items = report_items(report)
    if len(items) != len(node_object_ids):
        raise ValueError("node object ID count does not match report item count")

    story_blob = (
        b"".join(
            length_field(1, encode_story_node(item, node_id, story_node_struct_id))
            for item, node_id in zip(items, node_object_ids)
        )
        + varint_field(501, story_node_struct_id)
    )
    custom_value = (
        varint_field(1, 26)
        + length_field(2, type_ref(26, story_node_struct_id))
        + length_field(36, story_blob)
        + string_field(501, "Story_List")
    )
    custom_group = (
        length_field(1, custom_value)
        + varint_field(501, story_list_struct_id)
        + length_field(502, varint_field(2, 28) + varint_field(4, value_ref_id))
    )
    return (
        varint_field(1, 25)
        + length_field(2, type_ref(25, story_list_struct_id))
        + length_field(35, custom_group)
    )


def detect_story_struct_ids(component_record: dict[str, Any]) -> tuple[int, int]:
    story_variable = next(
        variable
        for variable in find_variable_messages(component_record)
        if extract_variable(variable, 0).get("kind") == "story"
    )
    value_field = first_field(children(story_variable), 4)
    value_type = first_field(children(value_field), 2)
    story_list_struct_id = varint(children(first_field(children(value_type), 2)), 2)

    custom_group_root = first_field(children(value_field), 35)
    custom_group = first_field(children(custom_group_root), 1)
    custom_type = first_field(children(custom_group), 2)
    story_node_struct_id = varint(children(first_field(children(custom_type), 2)), 2)
    story_blob = first_field(children(custom_group), 36)
    blob_struct_id = varint(children(story_blob), 501)
    if isinstance(blob_struct_id, int):
        story_node_struct_id = blob_struct_id
    group_struct_id = varint(children(custom_group_root), 501)
    if isinstance(group_struct_id, int):
        story_list_struct_id = group_struct_id

    if not isinstance(story_list_struct_id, int) or not isinstance(story_node_struct_id, int):
        raise ValueError("failed to detect Story_List/StoryNode struct IDs from template")
    return story_list_struct_id, story_node_struct_id


def collect_numeric_values(fields: list[dict[str, Any]]) -> set[int]:
    values: set[int] = set()
    for field in fields:
        if isinstance(field.get("value"), int):
            values.add(field["value"])
        values.update(collect_numeric_values(field.get("children", [])))
    return values


def update_component_identity(component_record: dict[str, Any], component_name: str, component_id: int) -> None:
    record_fields = children(component_record)
    meta = first_field(record_fields, 1)
    meta_id = first_field(children(meta), 4)
    if meta_id is None:
        raise ValueError("component meta id not found")
    meta_id["value"] = component_id
    meta_id["_dirty"] = True

    name_field = first_field(record_fields, 3)
    if name_field is None:
        raise ValueError("component name field not found")
    set_length_delimited_utf8(name_field, component_name)

    data = first_field(children(first_field(record_fields, 11)), 1)
    data_fields = children(data)
    data_id = first_field(data_fields, 1)
    if data_id is None:
        raise ValueError("component inner id not found")
    data_id["value"] = component_id
    data_id["_dirty"] = True

    name_param = next(
        (
            field
            for field in all_fields(data_fields, 6)
            if varint(children(field), 1) == 1
        ),
        None,
    )
    if name_param is None:
        raise ValueError("component display name param not found")
    name_payload = first_field(children(name_param), 11)
    name_value = first_field(children(name_payload), 1)
    if name_value is None:
        raise ValueError("component display name value not found")
    set_length_delimited_utf8(name_value, component_name)


def update_string_list_variable(variable: dict[str, Any], count: int) -> None:
    value_field = first_field(children(variable), 4)
    if value_field is None:
        raise ValueError("string list variable has no value field")
    value_field["_raw_override"] = encode_string_list_value([str(index) for index in range(1, count + 1)])


def update_story_variable(
    variable: dict[str, Any],
    variable_name: str,
    report: dict[str, Any],
    value_ref_id: int,
    node_object_ids: list[int],
    story_list_struct_id: int,
    story_node_struct_id: int,
) -> None:
    fields = children(variable)
    name_field = first_field(fields, 2)
    if name_field is None:
        raise ValueError("story variable name field not found")
    set_length_delimited_utf8(name_field, variable_name)

    value_field = first_field(fields, 4)
    if value_field is None:
        raise ValueError(f"story variable {variable_name} has no value field")
    value_field["_raw_override"] = encode_story_value(
        report,
        value_ref_id,
        node_object_ids,
        story_list_struct_id,
        story_node_struct_id,
    )


def replace_variable_list(
    component_record: dict[str, Any],
    reports: list[tuple[Path, dict[str, Any]]],
    story_list_struct_id: int,
    story_node_struct_id: int,
    next_object_id: int,
) -> tuple[int, list[dict[str, Any]]]:
    variables = find_variable_messages(component_record)
    if len(variables) < 2:
        raise ValueError("template must contain one string-list variable and at least one story variable")

    string_list_variable = variables[0]
    story_template = variables[1]
    story_variables = [
        copy.deepcopy(variables[index + 1]) if index + 1 < len(variables) else copy.deepcopy(story_template)
        for index in range(len(reports))
    ]
    update_string_list_variable(string_list_variable, len(reports))

    imported: list[dict[str, Any]] = []
    for index, (variable, (report_path, report)) in enumerate(zip(story_variables, reports), start=1):
        value_ref_id = next_object_id
        next_object_id += 1
        items = report_items(report)
        node_ids = list(range(next_object_id, next_object_id + len(items)))
        next_object_id += len(items)
        update_story_variable(
            variable,
            str(index),
            report,
            value_ref_id,
            node_ids,
            story_list_struct_id,
            story_node_struct_id,
        )
        imported.append(
            {
                "variable": str(index),
                "report": str(report_path),
                "value_ref_id": value_ref_id,
                "node_count": len(items),
                "first_node_id": node_ids[0] if node_ids else None,
                "last_node_id": node_ids[-1] if node_ids else None,
            }
        )

    variable_list = None
    data = first_field(children(first_field(children(component_record), 11)), 1)
    for block in all_fields(children(data), 8):
        block_fields = children(block)
        if varint(block_fields, 1) == 1 and varint(block_fields, 2) == 1:
            variable_list = first_field(block_fields, 11)
            break
    if variable_list is None:
        raise ValueError("component variable list not found")
    variable_list["children"] = [string_list_variable, *story_variables]
    variable_list.pop("_raw_override", None)
    return next_object_id, imported


def update_source_path(root: list[dict[str, Any]], output_path: Path) -> None:
    source_field = first_field(root, 3)
    if source_field is None:
        return
    old = source_field.get("utf8", "")
    prefix = old.rsplit("\\", 1)[0] if "\\" in old else ""
    new_source = f"{prefix}\\{output_path.name}" if prefix else output_path.name
    set_length_delimited_utf8(source_field, new_source)


def chapter_name(index: int, path: Path) -> str:
    if index <= len(CHAPTER_NAMES):
        return CHAPTER_NAMES[index - 1]
    return path.name


def build_multi_chapter_gia(
    template_path: Path,
    chapters_dir: Path,
    output_path: Path,
    summary_path: Path | None = None,
) -> dict[str, Any]:
    original = template_path.read_bytes()
    payload_len = int.from_bytes(original[16:20], "big")
    payload_end = HEADER_SIZE + payload_len
    if payload_end + FOOTER_SIZE != len(original):
        raise ValueError("template payload length mismatch")

    root = parse_message(original[HEADER_SIZE:payload_end], HEADER_SIZE)
    root_records = all_fields(root, 1)
    component_templates = [
        record
        for record in root_records
        if utf8(children(record), 3) and find_variable_messages(record)
    ]
    if not component_templates:
        raise ValueError("template does not contain a named component with variables")
    template_component = copy.deepcopy(component_templates[0])
    preserved_root_records = [
        record
        for record in root_records
        if not (utf8(children(record), 3) and find_variable_messages(record))
    ]
    story_list_struct_id, story_node_struct_id = detect_story_struct_ids(template_component)

    chapter_dirs = sorted(path for path in chapters_dir.iterdir() if path.is_dir())
    if not chapter_dirs:
        raise ValueError(f"no chapter directories found: {chapters_dir}")

    used_values = collect_numeric_values(root)
    # The file contains sentinel values such as 0xffffffff. Object IDs observed in
    # exported GIA files live in narrower 107... ranges, so allocate inside those
    # ranges instead of using the absolute max numeric protobuf value.
    story_object_ids = [value for value in used_values if 1_074_000_000 <= value < 1_075_000_000]
    component_like_ids = [value for value in used_values if 1_077_000_000 <= value < 1_078_000_000]
    if not story_object_ids or not component_like_ids:
        raise ValueError("failed to find existing 107... object ID ranges in template")
    next_object_id = max(story_object_ids) + 1
    component_id_start = max(component_like_ids) + 1

    components: list[dict[str, Any]] = []
    imported_chapters: list[dict[str, Any]] = []
    for index, chapter_dir in enumerate(chapter_dirs, start=1):
        reports = load_reports(chapter_dir)
        if not reports:
            raise ValueError(f"no report_*.json files found in {chapter_dir}")
        component = copy.deepcopy(template_component)
        name = chapter_name(index, chapter_dir)
        component_id = component_id_start + index - 1
        update_component_identity(component, name, component_id)
        next_object_id, imported = replace_variable_list(
            component,
            reports,
            story_list_struct_id,
            story_node_struct_id,
            next_object_id,
        )
        components.append(component)
        imported_chapters.append(
            {
                "chapter_dir": str(chapter_dir),
                "component": name,
                "component_id": component_id,
                "report_count": len(reports),
                "node_count": sum(item["node_count"] for item in imported),
                "imported": imported,
            }
        )

    new_root = components + preserved_root_records + [field for field in root if field["field"] != 1]
    update_source_path(new_root, output_path)
    new_payload = serialize_message(new_root)

    new_header = bytearray(original[:HEADER_SIZE])
    new_size = HEADER_SIZE + len(new_payload) + FOOTER_SIZE
    new_header[0:4] = (new_size - 4).to_bytes(4, "big")
    new_header[16:20] = len(new_payload).to_bytes(4, "big")
    output_path.write_bytes(bytes(new_header) + new_payload + original[payload_end:])

    summary = {
        "template": str(template_path),
        "chapters_dir": str(chapters_dir),
        "output": str(output_path),
        "story_list_struct_id": story_list_struct_id,
        "story_node_struct_id": story_node_struct_id,
        "component_count": len(components),
        "new_size": new_size,
        "chapters": imported_chapters,
    }
    if summary_path:
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Build one GIA file containing one component per chapter report dir.")
    parser.add_argument("--template", type=Path, required=True, help="template/reference .gia with multi-component structure")
    parser.add_argument("--chapters", type=Path, required=True, help="directory containing chapter report dirs")
    parser.add_argument("--output", type=Path, required=True, help="output .gia file")
    parser.add_argument("--summary", type=Path, help="write build summary JSON")
    parser.add_argument("--overwrite", action="store_true", help="allow replacing existing output/summary files")
    args = parser.parse_args()

    if not args.overwrite and args.output.exists():
        raise FileExistsError(f"output already exists: {args.output}")
    if not args.overwrite and args.summary and args.summary.exists():
        raise FileExistsError(f"summary already exists: {args.summary}")

    summary = build_multi_chapter_gia(args.template, args.chapters, args.output, args.summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
