from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path
import sys
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from parse_component_variables import (  # noqa: E402
    HEADER_SIZE,
    all_fields,
    children,
    find_variable_messages,
    first_field,
    parse_message,
    try_read_varint_bytes,
    utf8,
    varint,
)


TYPE_INFO: dict[int, dict[str, Any]] = {
    1: {"name": "object", "value_field": 11, "example": None},
    2: {"name": "GUID", "value_field": 12, "example": ""},
    3: {"name": "int", "value_field": 13, "example": 0},
    4: {"name": "bool", "value_field": 14, "example": False},
    5: {"name": "float", "value_field": 15, "example": 0.0},
    6: {"name": "str", "value_field": 16, "example": "hello world"},
    7: {"name": "GUID_list", "value_field": 17, "example": [""]},
    8: {"name": "int_list", "value_field": 18, "example": [0]},
    9: {"name": "bool_list", "value_field": 19, "example": [False]},
    10: {"name": "float_list", "value_field": 20, "example": [0.0]},
    11: {"name": "str_list", "value_field": 21, "example": ["hello world"]},
    12: {"name": "vector", "value_field": 22, "example": {"x": 0.0, "y": 0.0, "z": 0.0}},
    13: {"name": "object_list", "value_field": 23, "example": []},
    15: {"name": "vector_list", "value_field": 25, "example": []},
    17: {"name": "camp", "value_field": 27, "example": 1},
    20: {"name": "configurationID", "value_field": 30, "example": None},
    21: {"name": "componentID", "value_field": 31, "example": None},
    22: {"name": "configurationID_list", "value_field": 32, "example": []},
    23: {"name": "componentID_list", "value_field": 33, "example": []},
    24: {"name": "camp_list", "value_field": 34, "example": [0]},
    25: {"name": "struct", "value_field": 35, "example": {"struct": "TemplateStruct"}},
    26: {"name": "struct_list", "value_field": 36, "example": [{"struct": "TemplateStruct"}]},
    27: {"name": "dict", "value_field": 37, "example": {"key": "value"}},
}


def raw_hex(field: dict[str, Any] | None) -> str:
    if not field:
        return ""
    return field.get("raw", b"").hex(" ")


def list_items(container: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not container:
        return []
    return all_fields(children(container), 1)


def nested_type_owner(value_field: dict[str, Any] | None) -> int | None:
    if not value_field:
        return None
    type_field = first_field(children(value_field), 2)
    type_payload = first_field(children(type_field), 2) if type_field else None
    owner = varint(children(type_payload), 2) if type_payload else None
    return owner if isinstance(owner, int) else None


def nested_value_ref(value_payload: dict[str, Any] | None) -> int | None:
    if not value_payload:
        return None
    ref = first_field(children(value_payload), 502)
    value = varint(children(ref), 4) if ref else None
    return value if isinstance(value, int) else None


def scalar_value(value_field: dict[str, Any] | None, type_code: int) -> Any:
    value_slot = first_field(children(value_field), TYPE_INFO.get(type_code, {}).get("value_field", -1))
    if type_code == 6:
        values = [item.get("utf8") for item in list_items(value_slot) if isinstance(item.get("utf8"), str)]
        return values[0] if values else ""
    if type_code == 3:
        child = first_field(children(value_slot), 1) if value_slot else None
        return child.get("value", 0) if child else 0
    if type_code == 5:
        raw = value_slot.get("raw", b"") if value_slot else b""
        return struct.unpack("<f", raw)[0] if len(raw) == 4 else 0.0
    if type_code == 4:
        child = first_field(children(value_slot), 1) if value_slot else None
        return bool(child.get("value", 0)) if child else False
    if type_code in (7, 8, 9, 10, 11, 13, 24):
        result: list[Any] = []
        for item in list_items(value_slot):
            raw = item.get("raw", b"")
            if type_code == 11:
                result.append(item.get("utf8", ""))
            elif type_code == 10 and len(raw) == 4:
                result.append(struct.unpack("<f", raw)[0])
            elif type_code == 9:
                value = try_read_varint_bytes(raw) if raw else 0
                result.append(bool(value))
            else:
                result.append(try_read_varint_bytes(raw) if raw else 0)
        return result
    if type_code in (25, 26):
        return {
            "owner_id": nested_type_owner(value_field),
            "value_ref_id": nested_value_ref(value_slot),
            "raw_hex_prefix": raw_hex(value_slot)[:96],
        }
    return {
        "raw_hex": raw_hex(value_slot),
        "note": "default/empty or not yet semantically decoded",
    }


def dict_value(value_field: dict[str, Any]) -> dict[str, Any]:
    dict_payload = first_field(children(value_field), TYPE_INFO[27]["value_field"])
    key_type_code = varint(children(dict_payload), 503)
    value_type_code = varint(children(dict_payload), 504)
    key_type_code = key_type_code if isinstance(key_type_code, int) else None
    value_type_code = value_type_code if isinstance(value_type_code, int) else None

    entries: list[dict[str, Any]] = []
    for entry in list_items(dict_payload):
        struct_payload = first_field(children(entry), 35)
        pair_values = list_items(struct_payload)
        key = scalar_value(pair_values[0], key_type_code) if key_type_code and len(pair_values) > 0 else None
        value = scalar_value(pair_values[1], value_type_code) if value_type_code and len(pair_values) > 1 else None
        entries.append({"key": key, "value": value})

    return {
        "key_type_code": key_type_code,
        "key_type": TYPE_INFO.get(key_type_code or -1, {}).get("name"),
        "value_type_code": value_type_code,
        "value_type": TYPE_INFO.get(value_type_code or -1, {}).get("name"),
        "entries": entries,
        "raw_hex_prefix": raw_hex(dict_payload)[:96],
    }


def analyze_template(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    payload_len = int.from_bytes(data[16:20], "big")
    payload_end = HEADER_SIZE + payload_len
    if payload_end + 4 != len(data):
        raise ValueError("payload length mismatch")

    root = parse_message(data[HEADER_SIZE:payload_end], HEADER_SIZE)
    record = all_fields(root, 1)[0]
    variables = find_variable_messages(record)
    result: list[dict[str, Any]] = []
    dict_key_types: dict[int, str] = {}
    dict_value_types: dict[int, str] = {}

    for index, variable in enumerate(variables, start=1):
        fields = children(variable)
        name = utf8(fields, 2)
        type_code = varint(fields, 3)
        value_field = first_field(fields, 4)
        if not isinstance(type_code, int):
            continue
        info = TYPE_INFO.get(type_code, {"name": "unknown", "value_field": None, "example": None})
        decoded = dict_value(value_field) if type_code == 27 and value_field else scalar_value(value_field, type_code)
        if type_code == 27:
            key_code = decoded.get("key_type_code")
            value_code = decoded.get("value_type_code")
            if isinstance(key_code, int):
                dict_key_types[key_code] = decoded.get("key_type") or f"type_{key_code}"
            if isinstance(value_code, int):
                dict_value_types[value_code] = decoded.get("value_type") or f"type_{value_code}"
        result.append(
            {
                "index": index,
                "name": name,
                "type_code": type_code,
                "type_name": info["name"],
                "value_field": info["value_field"],
                "minimal_example": info["example"],
                "decoded_value": decoded,
            }
        )

    return {
        "file": str(path),
        "component": "Template",
        "variable_count": len(result),
        "type_mappings": [
            {
                "type_code": code,
                "type_name": info["name"],
                "value_field": info["value_field"],
                "minimal_example": info["example"],
            }
            for code, info in sorted(TYPE_INFO.items())
        ],
        "dict_rule": {
            "type_code": 27,
            "key_type_codes_observed": [
                {"type_code": code, "type_name": name}
                for code, name in sorted(dict_key_types.items())
            ],
            "value_type_codes_observed": [
                {"type_code": code, "type_name": name}
                for code, name in sorted(dict_value_types.items())
            ],
            "key_type_field": "value.f37.f503",
            "value_type_field": "value.f37.f504",
            "entries_field": "value.f37.f1[]",
        },
        "variables": result,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Template.gia variable type mappings generically.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", type=Path, help="write analysis JSON")
    args = parser.parse_args()

    result = analyze_template(args.path)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json:
        args.json.write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
