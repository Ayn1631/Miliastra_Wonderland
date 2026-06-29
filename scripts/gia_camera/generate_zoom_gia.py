from __future__ import annotations

import argparse
import struct
from pathlib import Path

# Example:
# python .\scripts\gia_camera\generate_zoom_gia.py --output C:\Users\20753\AppData\LocalLow\miHoYo\原神\BeyondLocal\Beyond_Local_Export\滑动变焦镜头组.gia --steps 32 --distance-start 3.0 --distance-end 2.7 --fov-start 60 --fov-end 45


HEADER_WORD_1 = 1
HEADER_WORD_2 = 806
HEADER_WORD_3 = 3
DEFAULT_FOOTER = 0x00000679
DEFAULT_VERSION = "6.6.0"
DEFAULT_SOURCE_PREFIX = "240730472-1781603800-1073741838-\\"


def varint(value: int) -> bytes:
    if value < 0:
        raise ValueError("varint only supports non-negative integers")
    out = bytearray()
    while value >= 0x80:
        out.append((value & 0x7F) | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)


def key(field_number: int, wire_type: int) -> bytes:
    return varint((field_number << 3) | wire_type)


def field_varint(field_number: int, value: int) -> bytes:
    return key(field_number, 0) + varint(value)


def field_fixed32(field_number: int, value: float) -> bytes:
    return key(field_number, 5) + struct.pack("<f", value)


def field_string(field_number: int, value: str) -> bytes:
    raw = value.encode("utf-8")
    return key(field_number, 2) + varint(len(raw)) + raw


def field_message(field_number: int, payload: bytes) -> bytes:
    return key(field_number, 2) + varint(len(payload)) + payload


def lerp(start: float, end: float, index: int, count: int) -> float:
    if count <= 1:
        return start
    return start + (end - start) * index / (count - 1)


def build_values(name: str, distance: float, field_of_view: float) -> bytes:
    return b"".join(
        [
            field_string(1, name),
            field_fixed32(2, distance),
            field_fixed32(3, field_of_view),
            field_string(4, ""),
            field_fixed32(5, 1.0),
            field_fixed32(6, 30.0),
            field_varint(12, 4),
            field_fixed32(14, 1.0),
            field_fixed32(15, 180.0),
            field_fixed32(16, 180.0),
        ]
    )


def build_record(name: str, record_id: int, distance: float, field_of_view: float) -> bytes:
    meta = field_varint(2, 25) + field_varint(4, record_id)
    values = build_values(name, distance, field_of_view)
    nested = field_varint(1, record_id) + field_message(2, values)
    wrapper = field_message(1, nested)
    record = b"".join(
        [
            field_message(1, meta),
            field_string(3, name),
            field_varint(5, 13),
            field_message(17, wrapper),
        ]
    )
    return field_message(1, record)


def build_payload(
    output_name: str,
    steps: int,
    distance_start: float,
    distance_end: float,
    fov_start: float,
    fov_end: float,
    version: str,
) -> bytes:
    chunks: list[bytes] = []
    for index in range(steps):
        name = str(index + 1)
        record_id = 0x40000002 + index
        distance = lerp(distance_start, distance_end, index, steps)
        field_of_view = lerp(fov_start, fov_end, index, steps)
        chunks.append(build_record(name, record_id, distance, field_of_view))

    source_path = DEFAULT_SOURCE_PREFIX + output_name
    chunks.append(field_string(3, source_path))
    chunks.append(field_string(5, version))
    return b"".join(chunks)


def build_gia(payload: bytes, footer: int) -> bytes:
    file_size = 20 + len(payload) + 4
    header = b"".join(
        word.to_bytes(4, "big")
        for word in [
            file_size - 4,
            HEADER_WORD_1,
            HEADER_WORD_2,
            HEADER_WORD_3,
            len(payload),
        ]
    )
    return header + payload + footer.to_bytes(4, "big")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an interpolated zoom GIA preset.")
    parser.add_argument("--output", default="滑动变焦_16.gia")
    parser.add_argument("--steps", type=int, default=16)
    parser.add_argument("--distance-start", type=float, default=3.0)
    parser.add_argument("--distance-end", type=float, default=2.7)
    parser.add_argument("--fov-start", type=float, default=60.0)
    parser.add_argument("--fov-end", type=float, default=45.0)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument(
        "--footer",
        type=lambda value: int(value, 0),
        default=DEFAULT_FOOTER,
        help="Footer value. Current evidence treats 0x00000679 as a fixed GIA trailer.",
    )
    args = parser.parse_args()

    if args.steps < 1:
        raise ValueError("--steps must be >= 1")

    payload = build_payload(
        output_name=Path(args.output).name,
        steps=args.steps,
        distance_start=args.distance_start,
        distance_end=args.distance_end,
        fov_start=args.fov_start,
        fov_end=args.fov_end,
        version=args.version,
    )
    data = build_gia(payload, args.footer)
    Path(args.output).write_bytes(data)
    print(f"wrote {args.output}: {len(data)} bytes, payload={len(payload)} bytes, steps={args.steps}")


if __name__ == "__main__":
    main()
