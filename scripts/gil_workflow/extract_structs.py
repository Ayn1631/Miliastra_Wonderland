from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from gil_common import TYPE_INFO, children, first_field, load_gil, root_children, varint


def utf8_child(field: dict[str, Any] | None, field_no: int) -> str | None:
    child = first_field(children(field), field_no) if field else None
    return child.get("utf8") if child else None


def nested_varint_value(message: dict[str, Any], path: list[int]) -> int | None:
    current = message
    for field_no in path[:-1]:
        current = first_field(children(current), field_no)
        if current is None:
            return None
    value = varint(children(current), path[-1])
    return value if isinstance(value, int) else None


def extract_struct_part(part: dict[str, Any]) -> dict[str, Any]:
    struct_id = varint(children(part), 1)
    struct_name = utf8_child(part, 501)
    fields: list[dict[str, Any]] = []

    for item in children(part):
        if item.get("field") != 3:
            continue
        item_children = children(item)
        field_name = utf8_child(item, 501) or utf8_child(item, 5)
        type_code = varint(item_children, 502)
        field_index = varint(item_children, 503)
        if not isinstance(type_code, int):
            continue
        field_doc = {
            "index": field_index,
            "name": field_name,
            "type_code": type_code,
            "type": TYPE_INFO.get(type_code, {}).get("name", f"type_{type_code}"),
        }
        nested_struct_id = nested_varint_value(item, [1, 2, 2])
        if nested_struct_id is not None and type_code in (25, 26):
            key_name = "element_struct_id" if type_code == 26 else "struct_id"
            field_doc[key_name] = nested_struct_id
        fields.append(field_doc)

    fields.sort(key=lambda item: item["index"] if isinstance(item.get("index"), int) else 10**9)
    return {
        "id": struct_id,
        "name": struct_name,
        "field_count": len(fields),
        "fields": fields,
    }


def extract_structs(gil_path: Path) -> dict[str, Any]:
    data, root = load_gil(gil_path)
    structs: list[dict[str, Any]] = []
    seen: set[int] = set()

    for record in root_children(root, 10):
        if record.get("field") != 6:
            continue
        part = first_field(children(record), 1)
        if part is None:
            continue
        parsed = extract_struct_part(part)
        struct_id = parsed.get("id")
        if not isinstance(struct_id, int) or struct_id in seen:
            continue
        seen.add(struct_id)
        parsed.update(
            {
                "schema_offset": record.get("offset"),
                "schema_length": record.get("length"),
            }
        )
        structs.append(parsed)

    structs.sort(key=lambda item: int(item["id"]))
    return {
        "file": str(gil_path),
        "size": len(data),
        "struct_count": len(structs),
        "structs": structs,
        "structs_by_name": {
            item["name"]: item["id"]
            for item in structs
            if isinstance(item.get("name"), str) and item.get("name")
        },
        "structs_by_id": {str(item["id"]): item for item in structs},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract struct schemas from a Qianxing .gil project.")
    parser.add_argument("gil", type=Path, help="input map/project .gil")
    parser.add_argument("--output", type=Path, help="write extracted structs JSON")
    args = parser.parse_args()

    result = extract_structs(args.gil)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
