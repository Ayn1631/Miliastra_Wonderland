from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path
from typing import Any


HEADER_SIZE = 20
FOOTER_SIZE = 4

CAMERA_FIELD_NAMES = {
    1: "name",
    2: "default_distance",
    3: "field_of_view",
    4: "viewpoint_offset",
    5: "min_distance",
    6: "max_distance",
    12: "camera_mode",
    13: "follow_rotation",
    14: "field_14",
    15: "min_horizontal_angle",
    16: "max_horizontal_angle",
    17: "min_pitch_angle",
    18: "max_pitch_angle",
    19: "ignore_collision",
    20: "horizontal_angle",
}

CAMERA_MODE_NAMES = {
    1: "3D背镜头",
    2: "2.5D镜头",
    3: "第一人称镜头",
    4: "第三人称镜头",
    5: "经典镜头",
}


def read_varint(data: bytes, pos: int) -> tuple[int, int]:
    value = 0
    shift = 0
    start = pos
    while True:
        if pos >= len(data):
            raise ValueError(f"truncated varint at offset {start}")
        byte = data[pos]
        pos += 1
        value |= (byte & 0x7F) << shift
        if byte < 0x80:
            return value, pos
        shift += 7
        if shift > 63:
            raise ValueError(f"varint too long at offset {start}")


def parse_message(data: bytes, base_offset: int = 0) -> list[dict[str, Any]]:
    fields: list[dict[str, Any]] = []
    pos = 0
    while pos < len(data):
        field_offset = base_offset + pos
        key, pos = read_varint(data, pos)
        field_no = key >> 3
        wire_type = key & 7
        field: dict[str, Any] = {
            "offset": field_offset,
            "field": field_no,
            "wire_type": wire_type,
        }

        if wire_type == 0:
            value, pos = read_varint(data, pos)
            field["type"] = "varint"
            field["value"] = value
        elif wire_type == 1:
            raw = data[pos : pos + 8]
            if len(raw) != 8:
                raise ValueError(f"truncated fixed64 at offset {field_offset}")
            pos += 8
            field["type"] = "fixed64"
            field["raw_hex"] = raw.hex(" ")
            field["double_le"] = struct.unpack("<d", raw)[0]
        elif wire_type == 2:
            length, pos = read_varint(data, pos)
            raw = data[pos : pos + length]
            if len(raw) != length:
                raise ValueError(f"truncated length-delimited field at offset {field_offset}")
            pos += length
            field["type"] = "length_delimited"
            field["length"] = length
            field["raw_hex"] = raw.hex(" ")
            try:
                field["utf8"] = raw.decode("utf-8")
            except UnicodeDecodeError:
                field["children"] = parse_message(raw, base_offset + pos - length)
        elif wire_type == 5:
            raw = data[pos : pos + 4]
            if len(raw) != 4:
                raise ValueError(f"truncated fixed32 at offset {field_offset}")
            pos += 4
            field["type"] = "fixed32"
            field["raw_hex"] = raw.hex(" ")
            field["uint32_le"] = struct.unpack("<I", raw)[0]
            field["float_le"] = struct.unpack("<f", raw)[0]
        else:
            raise ValueError(f"unsupported protobuf wire type {wire_type} at offset {field_offset}")

        fields.append(field)
    return fields


def summarize_record(field: dict[str, Any]) -> dict[str, Any]:
    # Shape observed in 镜头.gia:
    # root.f1 -> record, record.f17.f1.f2 -> numeric payload.
    result: dict[str, Any] = {}
    children = field.get("children", [])
    for child in children:
        if child["field"] == 1:
            for meta in child.get("children", []):
                if meta["field"] == 2:
                    result["type_or_kind"] = meta["value"]
                elif meta["field"] == 4:
                    result["id"] = meta["value"]
        elif child["field"] == 3:
            result["name"] = child.get("utf8")
        elif child["field"] == 5:
            result["class_or_flags"] = child["value"]
        elif child["field"] == 17:
            for wrapper in child.get("children", []):
                for nested in wrapper.get("children", []):
                    if nested["field"] == 1:
                        result["nested_id"] = nested["value"]
                    elif nested["field"] == 2:
                        values: dict[str, Any] = {}
                        camera_data: dict[str, Any] = {}
                        for scalar in nested.get("children", []):
                            key = f"f{scalar['field']}"
                            if scalar["type"] == "fixed32":
                                value = scalar["float_le"]
                            elif scalar["type"] == "varint":
                                value = scalar["value"]
                            elif scalar["type"] == "length_delimited":
                                if "children" in scalar and scalar["field"] == 4:
                                    offset_values: dict[str, float] = {}
                                    for item in scalar["children"]:
                                        if item["type"] == "fixed32":
                                            axis = {1: "x", 2: "y", 3: "z"}.get(item["field"], f"f{item['field']}")
                                            offset_values[axis] = item["float_le"]
                                    value = offset_values
                                else:
                                    value = scalar.get("utf8", "")
                            else:
                                continue
                            values[key] = value
                            field_name = CAMERA_FIELD_NAMES.get(scalar["field"])
                            if field_name:
                                camera_data[field_name] = value
                        if "camera_mode" in camera_data:
                            camera_data["camera_mode_name"] = CAMERA_MODE_NAMES.get(camera_data["camera_mode"])
                        result["values"] = values
                        result["camera_data"] = camera_data
                        result["distance"] = camera_data.get("default_distance", values.get("f2"))
                        result["field_of_view"] = camera_data.get("field_of_view", values.get("f3"))
                        result["horizontal_left_range_x"] = camera_data.get("min_horizontal_angle", values.get("f15", 0.0))
                        result["horizontal_right_range_y"] = camera_data.get("max_horizontal_angle", values.get("f16", 0.0))
                        result["pitch_min_range"] = camera_data.get("min_pitch_angle", values.get("f17", 0.0))
                        result["pitch_max_range"] = camera_data.get("max_pitch_angle", values.get("f18", 0.0))
    return result


def parse_gia(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if len(data) < HEADER_SIZE + FOOTER_SIZE:
        raise ValueError("file is too small to be a GIA sample with the observed container")

    header_words = [
        int.from_bytes(data[offset : offset + 4], "big")
        for offset in range(0, HEADER_SIZE, 4)
    ]
    payload_len = header_words[4]
    payload_start = HEADER_SIZE
    payload_end = payload_start + payload_len
    if payload_end + FOOTER_SIZE != len(data):
        raise ValueError(
            f"payload length mismatch: header says {payload_len}, "
            f"but file size is {len(data)}"
        )

    payload = data[payload_start:payload_end]
    fields = parse_message(payload, payload_start)
    records = [summarize_record(field) for field in fields if field["field"] == 1]

    return {
        "file": str(path),
        "size": len(data),
        "container": {
            "header_size": HEADER_SIZE,
            "header_u32_be": header_words,
            "observed_checks": {
                "header_u32_be[0] == file_size - 4": header_words[0] == len(data) - 4,
                "header_u32_be[4] == payload_size": header_words[4] == len(payload),
            },
            "payload_offset": payload_start,
            "payload_size": len(payload),
            "footer_u32_be": int.from_bytes(data[payload_end:], "big"),
            "footer_hex": data[payload_end:].hex(" "),
        },
        "summary": {
            "record_count": len(records),
            "records": records,
            "source_path": next((f.get("utf8") for f in fields if f["field"] == 3), None),
            "version": next((f.get("utf8") for f in fields if f["field"] == 5), None),
        },
        "protobuf_fields": fields,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect observed GIA container/protobuf data.")
    parser.add_argument("path", nargs="?", default="镜头.gia")
    parser.add_argument("--full", action="store_true", help="print full decoded protobuf tree")
    args = parser.parse_args()

    parsed = parse_gia(Path(args.path))
    if not args.full:
        parsed.pop("protobuf_fields", None)
    print(json.dumps(parsed, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
