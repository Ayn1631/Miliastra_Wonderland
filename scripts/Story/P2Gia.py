import copy
import json
from pathlib import Path

STRUCT_ID = "1077936130"
NODE_STRUCT_ID = "1077936129"
MAX_LINES_PER_FILE = 10
SCRIPTS_DIR = Path(__file__).resolve().parents[1]
RESOURCES_DIR = SCRIPTS_DIR / "resources"
STORY_PATH = RESOURCES_DIR / "story_sources" / "05_snow_prayer.txt"
STORY_NAME = STORY_PATH.stem
OUT_DIR = RESOURCES_DIR / "story_reports" / "lutasiyi_chapters" / STORY_NAME

def make_report():
    return {
        "structId": STRUCT_ID,
        "type": "Struct",
        "value": [{
            "param_type": "StructList",
            "value": {"structId": NODE_STRUCT_ID, "value": []},
        }],
    }


UNIT_TEMPLATE = {
    "param_type": "Struct",
    "value": {
        "structId": NODE_STRUCT_ID,
        "type": "Struct",
        "value": [
            {"param_type": "String", "value": "0"},
            {"param_type": "StringList", "value": ["", ""]},
            {"param_type": "Int32List", "value": ["0", "0"]},
        ],
    },
}


def parse_unit(line):
    status, string, next_ref = line.strip().split("|", 2)
    unit = copy.deepcopy(UNIT_TEMPLATE)
    unit["value"]["value"][0]["value"] = status.strip()
    unit["value"]["value"][1]["value"] = string.strip().split(";")
    unit["value"]["value"][2]["value"] = next_ref.strip().split(";")
    return unit


def chunks(items, size):
    for start in range(0, len(items), size):
        yield start, items[start:start + size]


def write_json(path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    if OUT_DIR.exists():
        for file in OUT_DIR.iterdir():
            if file.is_file():
                file.unlink()
    lines = [line for line in STORY_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    units = [parse_unit(line) for line in lines]
    OUT_DIR.mkdir(exist_ok=True)
    files = []

    for file_index, (start, part) in enumerate(chunks(units, MAX_LINES_PER_FILE), start=1):
        report = make_report()
        report["value"][0]["value"]["value"].extend(part)
        name = f"report_{file_index:03d}.json"
        write_json(OUT_DIR / name, report)
        files.append({"file": name, "start_next": start, "end_next": start + len(part) - 1})

    write_json(OUT_DIR / "report_manifest.json", {
        "source": str(STORY_PATH),
        "max_lines_per_file": MAX_LINES_PER_FILE,
        "total_lines": len(units),
        "formula": {
            "file_no_1_based": "next // max_lines_per_file + 1",
            "line_no_1_based": "next % max_lines_per_file + 1",
            "line_index_0_based": "next % max_lines_per_file",
        },
        "files": files,
    })


if __name__ == "__main__":
    main()
