from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from parse_component_variables import (
    FOOTER_SIZE,
    HEADER_SIZE,
    all_fields,
    children,
    find_variable_messages,
    nested_varint,
    parse_message,
    utf8,
)


def json_safe(value: Any) -> Any:
    if isinstance(value, bytes):
        return value.hex(" ")
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if key == "raw":
                result["raw_hex"] = json_safe(item)
            else:
                result[key] = json_safe(item)
        return result
    return value


def dump_full(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if len(data) < HEADER_SIZE + FOOTER_SIZE:
        raise ValueError("file is too small to be a GIA container")

    header_words = [
        int.from_bytes(data[offset : offset + 4], "big")
        for offset in range(0, HEADER_SIZE, 4)
    ]
    payload_len = header_words[4]
    payload_end = HEADER_SIZE + payload_len
    if payload_end + FOOTER_SIZE != len(data):
        raise ValueError(
            f"payload length mismatch: header says {payload_len}, file size is {len(data)}"
        )

    root = parse_message(data[HEADER_SIZE:payload_end], HEADER_SIZE)
    records = []
    for index, record in enumerate(all_fields(root, 1), start=1):
        record_children = children(record)
        variables = find_variable_messages(record)
        records.append(
            {
                "index": index,
                "offset": record["offset"],
                "length": record.get("length"),
                "name": utf8(record_children, 3),
                "id": nested_varint(record, [1, 4]),
                "variable_count": len(variables),
                "variable_names": [utf8(children(variable), 2) for variable in variables],
            }
        )

    return {
        "file": str(path),
        "size": len(data),
        "container": {
            "header_size": HEADER_SIZE,
            "header_u32_be": header_words,
            "payload_offset": HEADER_SIZE,
            "payload_size": payload_len,
            "footer_u32_be": int.from_bytes(data[payload_end:], "big"),
            "footer_hex": data[payload_end:].hex(" "),
        },
        "record_summary": records,
        "root_fields": json_safe(root),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Dump the full protobuf tree of an observed GIA file.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    parsed = dump_full(args.path)
    args.output.write_text(
        json.dumps(parsed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "size": parsed["size"],
                "record_summary": parsed["record_summary"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
