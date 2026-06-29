from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_DIR.parent
VARIABLES_SCRIPT_DIR = SCRIPTS_DIR / "gia_component_variables"
IMPORT_SCRIPT_DIR = SCRIPTS_DIR / "gia_component_import"
sys.path.insert(0, str(VARIABLES_SCRIPT_DIR))
sys.path.insert(0, str(IMPORT_SCRIPT_DIR))

from import_component_variables import FOOTER_SIZE, HEADER_SIZE, serialize_message
from parse_component_variables import children, first_field, parse_message


TEMPLATE_COMPONENT_ID = 1077936129
TEMPLATE_VALUE_REF_ID = 1073741833
TEMPLATE_NODE_IDS = list(range(1610612737, 1610612746))


def set_utf8(field: dict[str, Any], value: str) -> None:
    raw = value.encode("utf-8")
    field["utf8"] = value
    field["raw"] = raw
    field["length"] = len(raw)
    field.pop("children", None)
    field["_raw_override"] = raw


def mark_dirty(field: dict[str, Any]) -> None:
    field["_dirty"] = True


def walk(field: dict[str, Any]):
    yield field
    for child in field.get("children", []):
        yield from walk(child)


def replace_varint_values(field: dict[str, Any], replacements: dict[int, int]) -> None:
    for item in walk(field):
        value = item.get("value")
        if isinstance(value, int) and value in replacements:
            item["value"] = replacements[value]
            mark_dirty(item)


def replace_utf8_values(field: dict[str, Any], replacements: dict[str, str]) -> None:
    for item in walk(field):
        value = item.get("utf8")
        if isinstance(value, str) and value in replacements:
            set_utf8(item, replacements[value])


def top_field(root: list[dict[str, Any]], field_no: int) -> dict[str, Any]:
    field = first_field(root, field_no)
    if field is None:
        raise ValueError(f"root field not found: {field_no}")
    return field


def root_children(root: list[dict[str, Any]], field_no: int) -> list[dict[str, Any]]:
    return children(top_field(root, field_no))


def set_child_varint(field: dict[str, Any], field_no: int, value: int) -> None:
    child = first_field(children(field), field_no)
    if child is None or child.get("wire_type") != 0:
        raise ValueError(f"varint child not found: f{field_no} at {field.get('offset')}")
    child["value"] = value
    mark_dirty(child)


def find_named_record(records: list[dict[str, Any]], name: str) -> dict[str, Any]:
    for record in records:
        if any(item.get("utf8") == name for item in walk(record)):
            return record
    raise ValueError(f"record containing name not found: {name}")


def find_variable_list_field(record: dict[str, Any]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for item in walk(record):
        if item.get("field") != 11 or item.get("wire_type") != 2:
            continue
        variable_fields = [child for child in children(item) if child.get("field") == 1]
        if not variable_fields:
            continue
        for variable in variable_fields:
            variable_name = first_field(children(variable), 2)
            variable_type = first_field(children(variable), 3)
            if isinstance(variable_name, dict) and isinstance(variable_name.get("utf8"), str):
                if isinstance(variable_type, dict) and isinstance(variable_type.get("value"), int):
                    candidates.append(item)
                    break
    if not candidates:
        raise ValueError(f"variable list field not found in record at {record.get('offset')}")
    return candidates[-1]


def clone_variables(record: dict[str, Any], variable_names: list[str], struct_id: int, value_ref_start: int) -> None:
    variable_list = find_variable_list_field(record)
    template_variables = [field for field in children(variable_list) if field.get("field") == 1]
    if not template_variables:
        raise ValueError("template variable not found")
    template = template_variables[0]

    new_variables: list[dict[str, Any]] = []
    for index, variable_name in enumerate(variable_names):
        variable = copy.deepcopy(template)
        name_field = first_field(children(variable), 2)
        if name_field is None:
            raise ValueError("variable name field not found")
        set_utf8(name_field, variable_name)
        replace_varint_values(
            variable,
            {
                TEMPLATE_COMPONENT_ID: struct_id,
                TEMPLATE_VALUE_REF_ID: value_ref_start + index,
            },
        )
        new_variables.append(variable)

    variable_list["children"] = new_variables
    variable_list.pop("_raw_override", None)
    mark_dirty(variable_list)


def unique_variable_names(component: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for variable in component.get("variables", []):
        name = str(variable.get("name", "")).strip()
        if name and name not in names:
            names.append(name)
    while len(names) < 3:
        fallback = f"struct_var_{len(names) + 1}"
        if fallback not in names:
            names.append(fallback)
    return names


def clone_definition_record(template: dict[str, Any], component_name: str, component_id: int, value_ref_start: int, variable_names: list[str]) -> dict[str, Any]:
    record = copy.deepcopy(template)
    set_child_varint(record, 1, component_id)
    replace_utf8_values(record, {"test": component_name})
    replace_varint_values(record, {TEMPLATE_COMPONENT_ID: component_id})
    clone_variables(record, variable_names, component_id, value_ref_start)
    return record


def clone_instance_record(
    template: dict[str, Any],
    component_name: str,
    component_id: int,
    instance_id: int,
    value_ref_start: int,
    variable_names: list[str],
) -> dict[str, Any]:
    record = copy.deepcopy(template)
    set_child_varint(record, 1, instance_id)
    ref = first_field(children(record), 2)
    if ref is not None:
        ref_id = first_field(children(ref), 1)
        if ref_id is not None and ref_id.get("wire_type") == 0:
            ref_id["value"] = component_id
            mark_dirty(ref_id)
    replace_utf8_values(record, {"test": component_name})
    replace_varint_values(record, {TEMPLATE_COMPONENT_ID: component_id})
    clone_variables(record, variable_names, component_id, value_ref_start)
    return record


def clone_index_record(template: dict[str, Any], component_name: str, component_id: int, value_ref_start: int, variable_names: list[str]) -> dict[str, Any]:
    record = copy.deepcopy(template)
    set_child_varint(record, 1, component_id)
    ref = first_field(children(record), 2)
    if ref is not None:
        ref_id = first_field(children(ref), 1)
        if ref_id is not None and ref_id.get("wire_type") == 0:
            ref_id["value"] = component_id
            mark_dirty(ref_id)
    replace_utf8_values(record, {"test": component_name})
    replace_varint_values(record, {TEMPLATE_COMPONENT_ID: component_id})
    clone_variables(record, variable_names, component_id, value_ref_start)
    return record


def clone_struct_schema(template: dict[str, Any], struct_name: str, struct_id: int) -> dict[str, Any]:
    record = copy.deepcopy(template)
    replace_utf8_values(record, {"test": struct_name})
    replace_varint_values(record, {TEMPLATE_COMPONENT_ID: struct_id})
    return record


def clone_struct_nodes(
    templates: list[dict[str, Any]],
    struct_name: str,
    struct_id: int,
    node_id_start: int,
) -> list[dict[str, Any]]:
    node_map = {old: node_id_start + index for index, old in enumerate(TEMPLATE_NODE_IDS)}
    cloned: list[dict[str, Any]] = []
    for template in templates:
        record = copy.deepcopy(template)
        replace_utf8_values(record, {"test": struct_name})
        replace_varint_values(record, {TEMPLATE_COMPONENT_ID: struct_id, **node_map})
        cloned.append(record)
    return cloned


def update_container_header(original: bytes, payload: bytes) -> bytes:
    header = bytearray(original[:HEADER_SIZE])
    new_size = HEADER_SIZE + len(payload) + FOOTER_SIZE
    header[0:4] = (new_size - 4).to_bytes(4, "big")
    header[16:20] = len(payload).to_bytes(4, "big")
    return bytes(header) + payload + original[-FOOTER_SIZE:]


def validate_container(data: bytes) -> None:
    payload_len = int.from_bytes(data[16:20], "big")
    if HEADER_SIZE + payload_len + FOOTER_SIZE != len(data):
        raise ValueError("generated GIL header payload size mismatch")
    parse_message(data[HEADER_SIZE : HEADER_SIZE + payload_len], HEADER_SIZE)


def build_multi_component_gil(spec_path: Path) -> dict[str, Any]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    base_dir = spec_path.parent
    base_gil = base_dir / spec["base_gil"]
    output_gil = base_dir / spec["output_gil"]

    original = base_gil.read_bytes()
    payload_len = int.from_bytes(original[16:20], "big")
    payload_end = HEADER_SIZE + payload_len
    if payload_end + FOOTER_SIZE != len(original):
        raise ValueError("base GIL payload length mismatch")

    root = parse_message(original[HEADER_SIZE:payload_end], HEADER_SIZE)
    f4_children = root_children(root, 4)
    f5_children = root_children(root, 5)
    f8_children = root_children(root, 8)
    f10_children = root_children(root, 10)

    definition_template = find_named_record(f4_children, "test")
    instance_template = find_named_record(f5_children, "test")
    index_template = find_named_record(f8_children, "test")
    struct_node_templates = [field for field in f10_children if field.get("field") == 2][:9]
    struct_schema_template = next(field for field in f10_children if field.get("field") == 6)
    if len(struct_node_templates) != 9:
        raise ValueError("expected 9 struct node templates")

    id_policy = spec.get("id_policy", {})
    component_id_next = int(id_policy.get("component_definition_start", 1077936200))
    instance_id_next = int(id_policy.get("component_instance_start", 1077936300))
    node_id_next = int(id_policy.get("struct_node_start", 1610612800))
    value_ref_next = 1073741900

    generated: list[dict[str, Any]] = []
    for component in spec.get("components", []):
        component_name = str(component["name"])
        variable_names = unique_variable_names(component)
        component_id = component_id_next
        instance_id = instance_id_next
        value_ref_start = value_ref_next
        node_id_start = node_id_next

        f4_children.append(clone_definition_record(definition_template, component_name, component_id, value_ref_start, variable_names))
        f5_children.append(clone_instance_record(instance_template, component_name, component_id, instance_id, value_ref_start, variable_names))
        f8_children.append(clone_index_record(index_template, component_name, component_id, value_ref_start, variable_names))
        f10_children.extend(clone_struct_nodes(struct_node_templates, component_name, component_id, node_id_start))
        f10_children.append(clone_struct_schema(struct_schema_template, component_name, component_id))

        generated.append(
            {
                "component": component_name,
                "component_id": component_id,
                "instance_id": instance_id,
                "struct_id": component_id,
                "variable_names": variable_names,
                "value_ref_start": value_ref_start,
                "struct_node_id_start": node_id_start,
            }
        )
        component_id_next += 1
        instance_id_next += 1
        value_ref_next += len(variable_names)
        node_id_next += 9

    for field_no in (4, 5, 8, 10):
        field = top_field(root, field_no)
        field.pop("_raw_override", None)
        mark_dirty(field)

    payload = serialize_message(root)
    output = update_container_header(original, payload)
    validate_container(output)
    output_gil.write_bytes(output)

    summary = {
        "input": str(base_gil),
        "output": str(output_gil),
        "output_size": len(output),
        "payload_size": len(payload),
        "footer_hex": output[-FOOTER_SIZE:].hex(" "),
        "generated_count": len(generated),
        "generated": generated,
        "note": "Generated variables are cloned as type_code=25 struct variables from the confirmed template.",
    }
    summary_path = output_gil.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a multi-component GIL from the observed test component template.")
    parser.add_argument("spec", type=Path, help="generation spec JSON")
    args = parser.parse_args()
    print(json.dumps(build_multi_component_gil(args.spec), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
