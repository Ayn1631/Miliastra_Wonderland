from __future__ import annotations

import argparse
import json
from pathlib import Path

from extract_structs import extract_structs


def main() -> None:
    parser = argparse.ArgumentParser(description="Export all struct schemas from a Qianxing .gil save.")
    parser.add_argument("input_gil", type=Path, help="input save/map .gil")
    parser.add_argument("output_json", type=Path, help="output structs JSON")
    args = parser.parse_args()

    result = extract_structs(args.input_gil)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "input_gil": str(args.input_gil),
                "output_json": str(args.output_json),
                "struct_count": result["struct_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
