from __future__ import annotations

import copy
import json
import math
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import streamlit as st
import streamlit.components.v1 as components


SCRIPTS_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = SCRIPTS_DIR / "resources"
GIL_WORKFLOW_DIR = SCRIPTS_DIR / "gil_workflow"
GIA_CAMERA_DIR = SCRIPTS_DIR / "gia_camera"
GIA_COMPONENT_IMPORT_DIR = SCRIPTS_DIR / "gia_component_import"
STORY_DIR = SCRIPTS_DIR / "Story"
DEFAULT_TEMPLATE_GIL = RESOURCES_DIR / "gil_templates" / "Template.gil"
DEFAULT_TEMPLATE_GIA = RESOURCES_DIR / "gil_templates" / "Template.gia"
COMPONENTS_EXAMPLE_JSON = GIL_WORKFLOW_DIR / "components.example.json"
COMPONENTS_JSON_GUIDE = GIL_WORKFLOW_DIR / "COMPONENTS_JSON_GUIDE.md"
STORY_PAGE_CSS = """
<style>
html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
  height: 100%;
  overflow: hidden;
}

[data-testid="stHeader"],
footer {
  display: none;
}

[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {
  height: 100vh;
  max-height: 100vh;
  padding: 0;
  overflow: hidden;
}

[data-testid="stVerticalBlock"],
[data-testid="element-container"]:has(iframe[data-testid="stIFrame"]) {
  height: 100vh;
  max-height: 100vh;
  padding: 0;
  overflow: hidden;
  gap: 0;
}

[data-testid="element-container"]:has(style) {
  height: 0 !important;
  min-height: 0 !important;
  max-height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}

[data-testid="stIFrame"] {
  width: 100% !important;
  height: 100vh !important;
  min-height: 100vh !important;
  max-height: 100vh !important;
  display: block;
  border: 0;
}
</style>
"""

import sys

for path in (GIL_WORKFLOW_DIR, GIA_CAMERA_DIR, GIA_COMPONENT_IMPORT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import build_multi_chapter_gia as gia_chapters  # noqa: E402
from build_chapter_components_spec import build_spec  # noqa: E402
from create_components import BuildContext, build_components, encode_value_message  # noqa: E402
from extract_structs import extract_structs  # noqa: E402
from gil_common import TYPE_INFO  # noqa: E402
from generate_zoom_gia import (  # noqa: E402
    DEFAULT_FOOTER,
    DEFAULT_VERSION,
    build_gia,
    build_record,
    field_string,
)


STRUCT_ID = "1077936130"
NODE_STRUCT_ID = "1077936129"
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


PARAM_TYPE_BY_CODE = {
    3: "Int32",
    4: "Bool",
    5: "Float",
    6: "String",
    8: "Int32List",
    9: "BoolList",
    10: "FloatList",
    11: "StringList",
    25: "Struct",
    26: "StructList",
}

LIST_TYPE_CODES = {7, 8, 9, 10, 11, 13, 15, 22, 23, 24}


def write_upload(uploaded_file: Any, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(uploaded_file.getvalue())
    return path


def read_text_upload(uploaded_file: Any) -> str:
    raw = uploaded_file.getvalue()
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def default_components_json_text() -> str:
    if COMPONENTS_EXAMPLE_JSON.exists():
        return COMPONENTS_EXAMPLE_JSON.read_text(encoding="utf-8")
    return json.dumps({"components": []}, ensure_ascii=False, indent=2) + "\n"


def normalize_components_doc(data: Any) -> dict[str, Any]:
    if isinstance(data, list):
        data = {"components": data}
    if not isinstance(data, dict):
        raise ValueError("顶层必须是对象，或直接是 components 数组。")
    components = data.get("components")
    if not isinstance(components, list):
        raise ValueError("JSON 必须包含 components 数组。")
    for index, component in enumerate(components, start=1):
        if not isinstance(component, dict):
            raise ValueError(f"components[{index}] 必须是对象。")
        if not str(component.get("name", "")).strip():
            raise ValueError(f"components[{index}] 缺少 name。")
        variables = component.get("variables")
        if not isinstance(variables, list):
            raise ValueError(f"components[{index}] 必须包含 variables 数组。")
        for var_index, variable in enumerate(variables, start=1):
            if not isinstance(variable, dict):
                raise ValueError(f"components[{index}].variables[{var_index}] 必须是对象。")
            if not str(variable.get("name", "")).strip():
                raise ValueError(f"components[{index}].variables[{var_index}] 缺少 name。")
            if "type" not in variable and "type_code" not in variable:
                raise ValueError(f"components[{index}].variables[{var_index}] 缺少 type 或 type_code。")
    return data


def find_struct_doc(structs_doc: dict[str, Any], struct_name: str) -> dict[str, Any] | None:
    for item in structs_doc.get("structs", []):
        if str(item.get("name", "")) == struct_name or str(item.get("id", "")) == struct_name:
            return item
    return None


def field_nested_struct_ref(field: dict[str, Any]) -> str | None:
    type_code = int(field.get("type_code", 0))
    if type_code == 25:
        ref = field.get("struct_id") or field.get("structId") or field.get("struct")
    elif type_code == 26:
        ref = (
            field.get("element_struct_id")
            or field.get("elementStructId")
            or field.get("item_struct_id")
            or field.get("itemStructId")
            or field.get("struct_id")
            or field.get("struct")
        )
    else:
        ref = None
    return str(ref) if ref is not None and str(ref).strip() else None


def resolve_nested_struct_doc(
    field: dict[str, Any],
    structs_doc: dict[str, Any],
) -> dict[str, Any] | None:
    nested_ref = field_nested_struct_ref(field)
    if nested_ref:
        return find_struct_doc(structs_doc, nested_ref)

    # 兼容旧版 Story 结构定义：早期 JSON 没有保存 Story_List 的元素结构体 ID。
    if field.get("name") == "Story_List":
        return find_struct_doc(structs_doc, NODE_STRUCT_ID) or find_struct_doc(structs_doc, "StoryNode")
    return None


def nested_struct_label(struct_doc: dict[str, Any] | None) -> str:
    if not struct_doc:
        return "未解析"
    name = str(struct_doc.get("name") or "")
    struct_id = struct_doc.get("id")
    return f"{name} ({struct_id})" if struct_id is not None else name


def default_value_for_type(type_code: int) -> Any:
    if type_code == 6:
        return ""
    if type_code in (11, 8, 9, 10, 24, 7, 13, 15, 22, 23):
        return []
    if type_code in (3, 17):
        return 0
    if type_code == 5:
        return 0.0
    if type_code == 4:
        return False
    if type_code in (25, 12):
        return {}
    if type_code == 26:
        return []
    if type_code == 27:
        return {"entries": []}
    return None


def build_struct_value_template(
    struct_doc: dict[str, Any],
    nested_structs: dict[str, str],
) -> dict[str, Any]:
    value: dict[str, Any] = {}
    struct_types: dict[str, str] = {}
    for field in struct_doc.get("fields", []):
        field_name = str(field.get("name") or "").strip()
        if not field_name:
            continue
        type_code = int(field.get("type_code", 0))
        value[field_name] = default_value_for_type(type_code)
        if type_code in (25, 26) and nested_structs.get(field_name):
            struct_types[field_name] = nested_structs[field_name]
    if struct_types:
        value["__struct_types__"] = struct_types
    return value


def build_struct_variable_template(
    variable_name: str,
    struct_doc: dict[str, Any],
    variable_type: str,
    nested_structs: dict[str, str],
) -> dict[str, Any]:
    struct_name = str(struct_doc.get("name") or struct_doc.get("id"))
    value = build_struct_value_template(struct_doc, nested_structs)
    if variable_type == "struct_list":
        value = [value]
    return {
        "name": variable_name,
        "type": variable_type,
        "struct": struct_name,
        "value": value,
    }


def append_variable_to_component(
    components_doc: dict[str, Any],
    component_name: str,
    variable: dict[str, Any],
) -> dict[str, Any]:
    components = components_doc.setdefault("components", [])
    for component in components:
        if component.get("name") == component_name:
            component.setdefault("variables", []).append(variable)
            return components_doc
    components.append({"name": component_name, "variables": [variable]})
    return components_doc


def infer_story_structs_from_gia(gia_path: Path) -> dict[str, Any]:
    data = gia_path.read_bytes()
    if len(data) < gia_chapters.HEADER_SIZE + gia_chapters.FOOTER_SIZE:
        raise ValueError("文件太小，不是有效的 GIA 容器。")

    payload_len = int.from_bytes(data[16:20], "big")
    payload_end = gia_chapters.HEADER_SIZE + payload_len
    if payload_end + gia_chapters.FOOTER_SIZE != len(data):
        raise ValueError("GIA payload 长度校验失败。")

    story_node = {
        "id": int(NODE_STRUCT_ID),
        "name": "StoryNode",
        "field_count": 3,
        "fields": [
            {"index": 1, "name": "status", "type_code": 6, "type": "str"},
            {"index": 2, "name": "str", "type_code": 11, "type": "str_list"},
            {"index": 3, "name": "next", "type_code": 8, "type": "int_list"},
        ],
        "source": "inferred_from_gia_story_variable",
    }
    story = {
        "id": int(STRUCT_ID),
        "name": "Story",
        "field_count": 1,
        "fields": [
            {"index": 1, "name": "Story_List", "type_code": 26, "type": "struct_list"},
        ],
        "source": "inferred_from_gia_story_variable",
    }
    structs = [story_node, story]
    return {
        "file": str(gia_path),
        "size": len(data),
        "source_format": "gia",
        "extraction_mode": "inferred_story_structs",
        "note": "GIA 文件没有 GIL 的 root.f10 结构体定义区；这里根据 Story 元件变量格式推断 Story/StoryNode 结构体。",
        "struct_count": len(structs),
        "structs": structs,
        "structs_by_name": {item["name"]: item["id"] for item in structs},
        "structs_by_id": {str(item["id"]): item for item in structs},
    }


def nested_varint_value(message: dict[str, Any], path: list[int]) -> int | None:
    current = message
    for field_id in path[:-1]:
        current = gia_chapters.first_field(gia_chapters.children(current), field_id)
        if current is None:
            return None
    return gia_chapters.varint(gia_chapters.children(current), path[-1])


def iter_message_tree(message: dict[str, Any]) -> Any:
    stack = [message]
    while stack:
        current = stack.pop()
        yield current
        stack.extend(reversed(gia_chapters.children(current)))


def parse_gia_struct_schema_candidate(
    candidate: dict[str, Any],
    struct_id: int,
    *,
    source_record_index: int,
    schema_path: str,
) -> dict[str, Any] | None:
    candidate_fields = gia_chapters.children(candidate)
    struct_name = gia_chapters.utf8(candidate_fields, 501)
    field_messages = gia_chapters.all_fields(candidate_fields, 3)
    if not struct_name or not field_messages:
        return None

    fields: list[dict[str, Any]] = []
    for field_message in field_messages:
        field_fields = gia_chapters.children(field_message)
        field_name = gia_chapters.utf8(field_fields, 501) or gia_chapters.utf8(field_fields, 5)
        type_code = gia_chapters.varint(field_fields, 502)
        field_index = gia_chapters.varint(field_fields, 503)
        if not field_name or type_code is None or field_index is None:
            return None
        field_doc = {
            "index": int(field_index),
            "name": field_name,
            "type_code": int(type_code),
            "type": TYPE_INFO.get(int(type_code), {}).get("name", f"type_{type_code}"),
        }
        nested_struct_id = nested_varint_value(field_message, [1, 2, 2])
        if nested_struct_id is not None and int(type_code) in (25, 26):
            key_name = "element_struct_id" if int(type_code) == 26 else "struct_id"
            field_doc[key_name] = int(nested_struct_id)
        fields.append(field_doc)

    fields.sort(key=lambda item: item["index"])
    return {
        "id": int(struct_id),
        "name": struct_name,
        "field_count": len(fields),
        "fields": fields,
        "schema_offset": candidate.get("offset"),
        "schema_length": candidate.get("length"),
        "source_record_index": source_record_index,
        "schema_path": schema_path,
    }


def extract_structs_from_gia_schema(gia_path: Path) -> dict[str, Any]:
    data = gia_path.read_bytes()
    if len(data) < gia_chapters.HEADER_SIZE + gia_chapters.FOOTER_SIZE:
        raise ValueError("文件太小，不是有效的 GIA 容器。")

    payload_len = int.from_bytes(data[16:20], "big")
    payload_end = gia_chapters.HEADER_SIZE + payload_len
    if payload_end + gia_chapters.FOOTER_SIZE != len(data):
        raise ValueError("GIA payload 长度校验失败。")

    root = gia_chapters.parse_message(data[gia_chapters.HEADER_SIZE : payload_end], gia_chapters.HEADER_SIZE)
    structs: list[dict[str, Any]] = []
    seen_signatures: set[tuple[int, str]] = set()

    for record_index, record in enumerate(gia_chapters.all_fields(root, 1), start=1):
        struct_id = nested_varint_value(record, [1, 4])
        if struct_id is None:
            continue

        for candidate in iter_message_tree(record):
            schema = parse_gia_struct_schema_candidate(
                candidate,
                int(struct_id),
                source_record_index=record_index,
                schema_path=f"record[{record_index}]",
            )
            if not schema:
                continue
            signature = (schema["id"], schema["name"])
            if signature in seen_signatures:
                continue
            seen_signatures.add(signature)
            structs.append(schema)
            break

    if not structs:
        raise ValueError("没有在 GIA 中找到结构体定义记录。")

    return {
        "file": str(gia_path),
        "size": len(data),
        "source_format": "gia",
        "extraction_mode": "gia_schema_records",
        "struct_count": len(structs),
        "structs": structs,
        "structs_by_name": {item["name"]: item["id"] for item in structs},
        "structs_by_id": {str(item["id"]): item for item in structs},
    }


def extract_structs_by_uploaded_format(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".gil":
        result = extract_structs(path)
        result["source_format"] = "gil"
        result["extraction_mode"] = "root_f10_schema"
        return result
    if suffix == ".gia":
        try:
            return extract_structs_from_gia_schema(path)
        except ValueError:
            return infer_story_structs_from_gia(path)
    raise ValueError(f"不支持的文件格式：{path.suffix}。请上传 .gil 或 .gia。")


def normalize_structs_doc(data: Any, *, source_name: str = "") -> dict[str, Any]:
    if isinstance(data, list):
        data = {"structs": data}
    if not isinstance(data, dict):
        raise ValueError("结构体数据顶层必须是对象，或直接是结构体数组。")
    structs = data.get("structs")
    if not isinstance(structs, list) or not structs:
        raise ValueError("结构体数据必须包含非空 structs 数组。")
    for index, struct in enumerate(structs, start=1):
        if not isinstance(struct, dict):
            raise ValueError(f"structs[{index}] 必须是对象。")
        if not (struct.get("name") or struct.get("id")):
            raise ValueError(f"structs[{index}] 缺少 name 或 id。")
        fields = struct.get("fields")
        if not isinstance(fields, list):
            raise ValueError(f"structs[{index}] 必须包含 fields 数组。")
    data["struct_count"] = int(data.get("struct_count") or len(structs))
    data["structs_by_name"] = {
        str(item.get("name")): item.get("id")
        for item in structs
        if item.get("name") and item.get("id") is not None
    }
    data["structs_by_id"] = {
        str(item.get("id")): item
        for item in structs
        if item.get("id") is not None
    }
    if source_name and not data.get("file"):
        data["file"] = source_name
    return data


def struct_id_text(struct_doc: dict[str, Any]) -> str:
    struct_id = struct_doc.get("id")
    if struct_id is None:
        raise ValueError(f"结构体缺少 id：{struct_doc.get('name')}")
    return str(struct_id)


def coerce_param_value(type_code: int, value: Any) -> Any:
    if type_code in (3, 17, 20, 21):
        return int(value or 0)
    if type_code == 4:
        return bool(value)
    if type_code == 5:
        return float(value or 0.0)
    if type_code == 6:
        return "" if value is None else str(value)
    if type_code in (8, 24):
        return [str(int(item or 0)) for item in (value or [])]
    if type_code in (9,):
        return [bool(item) for item in (value or [])]
    if type_code in (10,):
        return [float(item or 0.0) for item in (value or [])]
    if type_code in (7, 11, 13, 22, 23):
        return [str(item) for item in (value or [])]
    if type_code == 12:
        vector = value if isinstance(value, dict) else {}
        return {
            "x": float(vector.get("x") or 0.0),
            "y": float(vector.get("y") or 0.0),
            "z": float(vector.get("z") or 0.0),
        }
    if type_code in (15,):
        vectors = value if isinstance(value, list) else []
        return [
            {
                "x": float((item or {}).get("x") or 0.0),
                "y": float((item or {}).get("y") or 0.0),
                "z": float((item or {}).get("z") or 0.0),
            }
            for item in vectors
            if isinstance(item, dict)
        ]
    return value


def struct_value_to_data_json(
    struct_doc: dict[str, Any],
    structs_doc: dict[str, Any],
    value: dict[str, Any],
) -> dict[str, Any]:
    params: list[dict[str, Any]] = []
    for field in sorted(struct_doc.get("fields", []), key=lambda item: int(item.get("index", 0))):
        field_name = str(field.get("name") or "").strip()
        if not field_name:
            continue
        type_code = int(field.get("type_code", 0))
        param_type = PARAM_TYPE_BY_CODE.get(type_code) or TYPE_INFO.get(type_code, {}).get("name", f"type_{type_code}")
        field_value = value.get(field_name) if isinstance(value, dict) else None

        if type_code == 25:
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            if nested_doc is None:
                raise ValueError(f"字段 {field_name} 缺少嵌套结构体类型。")
            params.append(
                {
                    "param_type": "Struct",
                    "value": struct_value_to_data_json(nested_doc, structs_doc, field_value or {}),
                }
            )
            continue

        if type_code == 26:
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            if nested_doc is None:
                raise ValueError(f"字段 {field_name} 缺少结构体列表元素类型。")
            items = field_value if isinstance(field_value, list) else []
            params.append(
                {
                    "param_type": "StructList",
                    "value": {
                        "structId": struct_id_text(nested_doc),
                        "value": [
                            {
                                "param_type": "Struct",
                                "value": struct_value_to_data_json(nested_doc, structs_doc, item or {}),
                            }
                            for item in items
                        ],
                    },
                }
            )
            continue

        params.append(
            {
                "param_type": param_type,
                "value": coerce_param_value(type_code, field_value),
            }
        )

    return {
        "structId": struct_id_text(struct_doc),
        "type": "Struct",
        "value": params,
    }


def find_gia_variable_list(component_record: dict[str, Any]) -> dict[str, Any]:
    data = gia_chapters.first_field(
        gia_chapters.children(gia_chapters.first_field(gia_chapters.children(component_record), 11)),
        1,
    )
    for block in gia_chapters.all_fields(gia_chapters.children(data), 8):
        block_fields = gia_chapters.children(block)
        if gia_chapters.varint(block_fields, 1) == 1 and gia_chapters.varint(block_fields, 2) == 1:
            variable_list = gia_chapters.first_field(block_fields, 11)
            if variable_list:
                return variable_list
    raise ValueError("模板 GIA 中找不到变量列表。")


def clone_gia_variable_template(component_record: dict[str, Any], type_code: int) -> dict[str, Any]:
    variables = gia_chapters.find_variable_messages(component_record)
    for variable in variables:
        if gia_chapters.varint(gia_chapters.children(variable), 3) == type_code:
            return copy.deepcopy(variable)
    raise ValueError(f"模板 GIA 中找不到 type_code={type_code} 的变量模板。")


def update_gia_variable(
    variable: dict[str, Any],
    variable_name: str,
    type_code: int,
    value_payload: bytes,
) -> None:
    fields = gia_chapters.children(variable)
    name_field = gia_chapters.first_field(fields, 2)
    type_field = gia_chapters.first_field(fields, 3)
    value_field = gia_chapters.first_field(fields, 4)
    if name_field is None or type_field is None or value_field is None:
        raise ValueError("变量模板缺少 name/type/value 字段。")
    gia_chapters.set_length_delimited_utf8(name_field, variable_name)
    type_field["value"] = type_code
    type_field["_dirty"] = True
    value_field["_raw_override"] = value_payload


def build_struct_component_gia(
    template_gia: Path,
    structs_doc: dict[str, Any],
    component_name: str,
    variable_name: str,
    struct_name: str,
    value: dict[str, Any],
    output_gia: Path,
) -> dict[str, Any]:
    if not template_gia.exists():
        raise FileNotFoundError(f"template GIA not found: {template_gia}")
    original = template_gia.read_bytes()
    payload_len = int.from_bytes(original[16:20], "big")
    payload_end = gia_chapters.HEADER_SIZE + payload_len
    if payload_end + gia_chapters.FOOTER_SIZE != len(original):
        raise ValueError("template GIA payload length mismatch")

    root = gia_chapters.parse_message(original[gia_chapters.HEADER_SIZE:payload_end], gia_chapters.HEADER_SIZE)
    root_records = gia_chapters.all_fields(root, 1)
    component_templates = [
        record
        for record in root_records
        if gia_chapters.utf8(gia_chapters.children(record), 3)
        and gia_chapters.find_variable_messages(record)
    ]
    if not component_templates:
        raise ValueError("template GIA does not contain a named component with variables")

    component = copy.deepcopy(component_templates[0])
    used_values = gia_chapters.collect_numeric_values(root)
    component_like_ids = [item for item in used_values if 1_077_000_000 <= item < 1_078_000_000]
    component_id = (max(component_like_ids) + 1) if component_like_ids else 1_077_000_000
    gia_chapters.update_component_identity(component, component_name, component_id)

    value_ref_ids = [item for item in used_values if 1_073_000_000 <= item < 1_075_000_000]
    value_ref_start = (max(value_ref_ids) + 1) if value_ref_ids else 1_073_742_200
    ctx = BuildContext(structs_doc, set(used_values), value_ref_start)
    value_payload = encode_value_message(
        25,
        value,
        ctx,
        variable_spec={"type": "struct", "struct": struct_name},
    )

    variable = clone_gia_variable_template(component, 25)
    update_gia_variable(variable, variable_name, 25, value_payload)
    variable_list = find_gia_variable_list(component)
    variable_list["children"] = [variable]
    variable_list.pop("_raw_override", None)

    preserved_root_records = [
        record
        for record in root_records
        if not (
            gia_chapters.utf8(gia_chapters.children(record), 3)
            and gia_chapters.find_variable_messages(record)
        )
    ]
    new_root = [component] + preserved_root_records + [field for field in root if field["field"] != 1]
    gia_chapters.update_source_path(new_root, output_gia)
    new_payload = gia_chapters.serialize_message(new_root)

    new_header = bytearray(original[: gia_chapters.HEADER_SIZE])
    new_size = gia_chapters.HEADER_SIZE + len(new_payload) + gia_chapters.FOOTER_SIZE
    new_header[0:4] = (new_size - 4).to_bytes(4, "big")
    new_header[16:20] = len(new_payload).to_bytes(4, "big")
    output_gia.parent.mkdir(parents=True, exist_ok=True)
    output_gia.write_bytes(bytes(new_header) + new_payload + original[payload_end:])
    return {
        "template": str(template_gia),
        "output": str(output_gia),
        "component_name": component_name,
        "component_id": component_id,
        "variable_name": variable_name,
        "struct": struct_name,
        "warnings": ctx.warnings,
        "new_size": new_size,
    }


def list_text_to_values(text: str, type_code: int) -> list[Any]:
    values = [line.strip() for line in text.replace(",", "\n").splitlines() if line.strip()]
    if type_code in (8, 24):
        return [int(value) for value in values]
    if type_code == 10:
        return [float(value) for value in values]
    if type_code == 9:
        return [value.lower() in ("1", "true", "yes", "y", "是") for value in values]
    return values


def render_scalar_field_input(field: dict[str, Any], key: str) -> Any:
    field_name = str(field.get("name") or "")
    type_code = int(field.get("type_code", 0))
    type_name = field.get("type") or TYPE_INFO.get(type_code, {}).get("name", f"type_{type_code}")
    label = f"{field_name} ({type_name})"
    if type_code == 6:
        return st.text_input(label, value="", key=key)
    if type_code == 3:
        return int(st.number_input(label, value=0, step=1, key=key))
    if type_code == 5:
        return float(st.number_input(label, value=0.0, key=key))
    if type_code == 4:
        return st.checkbox(label, value=False, key=key)
    if type_code in (11, 8, 9, 10, 24):
        help_text = "一行一个值，也可以用英文逗号分隔。"
        text = st.text_area(label, value="", help=help_text, key=key)
        return list_text_to_values(text, type_code)
    if type_code == 12:
        cols = st.columns(3)
        return {
            "x": float(cols[0].number_input(f"{field_name}.x", value=0.0, key=f"{key}_x")),
            "y": float(cols[1].number_input(f"{field_name}.y", value=0.0, key=f"{key}_y")),
            "z": float(cols[2].number_input(f"{field_name}.z", value=0.0, key=f"{key}_z")),
        }
    st.caption(f"{label} 暂按默认空值导出。")
    return default_value_for_type(type_code)


def render_struct_value_editor(
    struct_doc: dict[str, Any],
    structs_doc: dict[str, Any],
    key_prefix: str,
    *,
    depth: int = 0,
    max_depth: int = 3,
) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for field in struct_doc.get("fields", []):
        field_name = str(field.get("name") or "").strip()
        if not field_name:
            continue
        type_code = int(field.get("type_code", 0))
        field_key = f"{key_prefix}_{field_name}_{type_code}_{depth}"
        if type_code == 25:
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            st.text_input(
                f"{field_name} (struct) 的结构体类型",
                value=nested_struct_label(nested_doc),
                disabled=True,
                key=f"{field_key}_struct_fixed",
            )
            if nested_doc and depth < max_depth:
                with st.expander(f"编辑 {field_name}", expanded=True):
                    value[field_name] = render_struct_value_editor(
                        nested_doc,
                        structs_doc,
                        f"{field_key}_nested",
                        depth=depth + 1,
                        max_depth=max_depth,
                    )
            else:
                if not nested_doc:
                    st.error(f"{field_name} 的结构定义里没有可解析的内层结构体类型。")
                value[field_name] = {}
            continue
        if type_code == 26:
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            st.text_input(
                f"{field_name} (struct_list) 的元素结构体类型",
                value=nested_struct_label(nested_doc),
                disabled=True,
                key=f"{field_key}_struct_list_fixed",
            )
            count = int(st.number_input(
                f"{field_name} 数量",
                min_value=0,
                max_value=200,
                value=1,
                step=1,
                key=f"{field_key}_count",
            ))
            items: list[dict[str, Any]] = []
            for index in range(count):
                if nested_doc and depth < max_depth:
                    with st.expander(f"{field_name} #{index + 1}", expanded=index == 0):
                        items.append(
                            render_struct_value_editor(
                                nested_doc,
                                structs_doc,
                                f"{field_key}_item_{index}",
                                depth=depth + 1,
                                max_depth=max_depth,
                            )
                        )
                else:
                    if not nested_doc:
                        st.error(f"{field_name} 的结构定义里没有可解析的元素结构体类型。")
                    items.append({})
            value[field_name] = items
            continue
        value[field_name] = render_scalar_field_input(field, field_key)
    return value


def make_report() -> dict[str, Any]:
    return {
        "structId": STRUCT_ID,
        "type": "Struct",
        "value": [
            {
                "param_type": "StructList",
                "value": {"structId": NODE_STRUCT_ID, "value": []},
            }
        ],
    }


def parse_story_line(line: str) -> dict[str, Any]:
    status, text, next_ref = line.strip().split("|", 2)
    unit = copy.deepcopy(UNIT_TEMPLATE)
    unit["value"]["value"][0]["value"] = status.strip()
    unit["value"]["value"][1]["value"] = [item.strip() for item in text.strip().split(";")]
    unit["value"]["value"][2]["value"] = [item.strip() for item in next_ref.strip().split(";")]
    return unit


def write_story_reports(story_text: str, chapter_dir: Path, max_lines_per_file: int) -> dict[str, Any]:
    if max_lines_per_file < 1:
        raise ValueError("max_lines_per_file must be >= 1")

    lines = [line for line in story_text.splitlines() if line.strip()]
    units = [parse_story_line(line) for line in lines]
    chapter_dir.mkdir(parents=True, exist_ok=True)

    files: list[dict[str, Any]] = []
    for index, start in enumerate(range(0, len(units), max_lines_per_file), start=1):
        part = units[start : start + max_lines_per_file]
        report = make_report()
        report["value"][0]["value"]["value"].extend(part)
        name = f"report_{index:03d}.json"
        (chapter_dir / name).write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        files.append({"file": name, "start_next": start, "end_next": start + len(part) - 1})

    manifest = {
        "source": "streamlit_story_upload.txt",
        "max_lines_per_file": max_lines_per_file,
        "total_lines": len(units),
        "files": files,
    }
    (chapter_dir / "report_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def build_story_component_gia(
    template_gia: Path,
    story_text: str,
    component_name: str,
    output_gia: Path,
    max_lines_per_file: int,
) -> dict[str, Any]:
    reports_root = output_gia.parent / "_story_gia_reports"
    chapter_dir = reports_root / "chapter_001"
    manifest = write_story_reports(story_text, chapter_dir, max_lines_per_file)

    original = template_gia.read_bytes()
    payload_len = int.from_bytes(original[16:20], "big")
    payload_end = gia_chapters.HEADER_SIZE + payload_len
    if payload_end + gia_chapters.FOOTER_SIZE != len(original):
        raise ValueError("template GIA payload length mismatch")

    root = gia_chapters.parse_message(original[gia_chapters.HEADER_SIZE:payload_end], gia_chapters.HEADER_SIZE)
    root_records = gia_chapters.all_fields(root, 1)
    component_templates = [
        record
        for record in root_records
        if gia_chapters.utf8(gia_chapters.children(record), 3)
        and gia_chapters.find_variable_messages(record)
    ]
    if not component_templates:
        raise ValueError("template GIA must contain a named component with variables")

    template_component = copy.deepcopy(component_templates[0])
    preserved_root_records = [
        record
        for record in root_records
        if not (
            gia_chapters.utf8(gia_chapters.children(record), 3)
            and gia_chapters.find_variable_messages(record)
        )
    ]
    story_list_struct_id, story_node_struct_id = gia_chapters.detect_story_struct_ids(template_component)

    reports = gia_chapters.load_reports(chapter_dir)
    if not reports:
        raise ValueError("story.txt did not produce report_*.json")

    used_values = gia_chapters.collect_numeric_values(root)
    story_object_ids = [value for value in used_values if 1_074_000_000 <= value < 1_075_000_000]
    component_like_ids = [value for value in used_values if 1_077_000_000 <= value < 1_078_000_000]
    if not story_object_ids or not component_like_ids:
        raise ValueError("failed to find existing 107... object ID ranges in template GIA")

    next_object_id = max(story_object_ids) + 1
    component_id = max(component_like_ids) + 1
    gia_chapters.update_component_identity(template_component, component_name, component_id)
    next_object_id, imported = gia_chapters.replace_variable_list(
        template_component,
        reports,
        story_list_struct_id,
        story_node_struct_id,
        next_object_id,
    )

    new_root = [template_component] + preserved_root_records + [field for field in root if field["field"] != 1]
    gia_chapters.update_source_path(new_root, output_gia)
    new_payload = gia_chapters.serialize_message(new_root)

    output_gia.parent.mkdir(parents=True, exist_ok=True)
    new_header = bytearray(original[:gia_chapters.HEADER_SIZE])
    new_size = gia_chapters.HEADER_SIZE + len(new_payload) + gia_chapters.FOOTER_SIZE
    new_header[0:4] = (new_size - 4).to_bytes(4, "big")
    new_header[16:20] = len(new_payload).to_bytes(4, "big")
    output_gia.write_bytes(bytes(new_header) + new_payload + original[payload_end:])

    summary = {
        "template": str(template_gia),
        "output": str(output_gia),
        "component": component_name,
        "component_id": component_id,
        "report_count": len(reports),
        "node_count": sum(item["node_count"] for item in imported),
        "story_list_struct_id": story_list_struct_id,
        "story_node_struct_id": story_node_struct_id,
        "story_manifest": manifest,
        "imported": imported,
        "next_object_id": next_object_id,
        "new_size": new_size,
    }
    output_gia.with_suffix(".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def build_story_gil(
    input_gil: Path,
    template_gil: Path,
    story_text: str,
    component_name: str,
    output_gil: Path,
    max_lines_per_file: int,
) -> dict[str, Any]:
    structs_json = output_gil.with_suffix(".structs.json")
    spec_json = output_gil.with_suffix(".workflow.json")
    chapters_root = output_gil.parent / "_story_reports"
    chapter_dir = chapters_root / component_name

    manifest = write_story_reports(story_text, chapter_dir, max_lines_per_file)
    structs = extract_structs(input_gil)
    structs_json.write_text(json.dumps(structs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    args = SimpleNamespace(
        chapters_root=chapters_root,
        input_gil=input_gil,
        template_gil=template_gil,
        template_component="Template",
        structs_json=structs_json,
        output_gil=output_gil,
        spec_output=spec_json,
        component_prefix="",
        component_definition_start=1077940000,
        component_index_start=1077950000,
        value_ref_start=1075000000,
        overwrite=True,
    )
    spec = build_spec(args)
    spec_json.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = build_components(spec_json)
    summary["story_manifest"] = manifest
    return summary


def build_components_gil(
    input_gil: Path,
    components_json: Path,
    template_gil: Path,
    output_gil: Path,
) -> dict[str, Any]:
    components_doc = json.loads(components_json.read_text(encoding="utf-8"))
    if isinstance(components_doc, list):
        components_doc = {"components": components_doc}
    if not isinstance(components_doc, dict) or "components" not in components_doc:
        raise ValueError("components JSON must be an object with components[] or a component array")

    structs_json = output_gil.with_suffix(".structs.json")
    spec_json = output_gil.with_suffix(".workflow.json")
    structs = extract_structs(input_gil)
    structs_json.write_text(json.dumps(structs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    spec: dict[str, Any] = {
        "format": "gil_component_workflow_spec",
        "version": 1,
        "input_gil": str(input_gil),
        "template_gil": str(template_gil),
        "template_component": "Template",
        "structs_json": str(structs_json),
        "output_gil": str(output_gil),
        "overwrite": True,
        "id_policy": components_doc.get(
            "id_policy",
            {
                "component_definition_start": 1077940000,
                "component_index_start": 1077950000,
                "value_ref_start": 1075000000,
            },
        ),
        "components": components_doc["components"],
    }
    spec_json.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return build_components(spec_json)


def curve_value(mode: str, t: float, strength: float) -> float:
    t = max(0.0, min(1.0, t))
    if mode == "linear":
        return t
    if mode == "ease_in_quad":
        return t * t
    if mode == "ease_out_quad":
        return 1 - (1 - t) * (1 - t)
    if mode == "ease_in_out_cubic":
        return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2
    if mode == "smoothstep":
        return t * t * (3 - 2 * t)
    if mode == "exponential":
        if abs(strength) < 0.001:
            return t
        numerator = math.exp(strength * t) - 1
        denominator = math.exp(strength) - 1
        return numerator / denominator
    raise ValueError(f"unsupported curve mode: {mode}")


def interpolate(start: float, end: float, index: int, count: int, mode: str, strength: float) -> float:
    t = 0.0 if count <= 1 else index / (count - 1)
    c = curve_value(mode, t, strength)
    return start + (end - start) * c


def build_camera_gia(
    output_name: str,
    steps: int,
    distance_start: float,
    distance_end: float,
    fov_start: float,
    fov_end: float,
    curve: str,
    strength: float,
    record_start: int,
    version: str,
) -> bytes:
    if steps < 1:
        raise ValueError("steps must be >= 1")
    chunks: list[bytes] = []
    for index in range(steps):
        name = str(index + 1)
        distance = interpolate(distance_start, distance_end, index, steps, curve, strength)
        fov = interpolate(fov_start, fov_end, index, steps, curve, strength)
        chunks.append(build_record(name, record_start + index, distance, fov))
    chunks.append(field_string(3, "240730472-1781603800-1073741838-\\" + output_name))
    chunks.append(field_string(5, version))
    return build_gia(b"".join(chunks), DEFAULT_FOOTER)


def load_story_board_html() -> str:
    html = (STORY_DIR / "story_board.html").read_text(encoding="utf-8")
    css_path = STORY_DIR / "story_board.css"
    js_path = STORY_DIR / "story_board.js"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        html = html.replace(
            '<link rel="stylesheet" href="story_board.css">',
            f"<style>\n{css}\n</style>",
        )
    if js_path.exists():
        js = js_path.read_text(encoding="utf-8")
        html = html.replace(
            '<script src="story_board.js"></script>',
            f"<script>\n{js}\n</script>",
        )
    return html


def page_story_builder() -> None:
    html_path = STORY_DIR / "story_board.html"
    if html_path.exists():
        st.markdown(STORY_PAGE_CSS, unsafe_allow_html=True)
        components.html(load_story_board_html(), height=1600, scrolling=False)
    else:
        st.error(f"找不到编辑器 HTML：{html_path}")


def page_extract_structs() -> None:
    st.header("导出结构体 JSON")
    uploaded = st.file_uploader("上传 .gil 或 .gia", type=["gil", "gia"], key="extract_structs_source")
    if st.button("导出结构体", type="primary", disabled=uploaded is None):
        with tempfile.TemporaryDirectory(prefix="qx_structs_") as tmp:
            suffix = Path(uploaded.name).suffix.lower()
            input_path = write_upload(uploaded, Path(tmp) / f"input{suffix}")
            try:
                result = extract_structs_by_uploaded_format(input_path)
            except Exception as exc:
                st.exception(exc)
                return
            data = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
            st.success(
                f"已识别为 {result.get('source_format', suffix.lstrip('.')).upper()}，"
                f"提取到 {result.get('struct_count', 0)} 个结构体"
            )
            st.json(result, expanded=False)
            st.download_button(
                "下载 structs.json",
                data.encode("utf-8"),
                file_name=f"{Path(uploaded.name).stem}.structs.json",
                mime="application/json",
            )


def page_components_builder() -> None:
    st.header("按 components JSON 构建 GIL")
    col_example, col_guide = st.columns(2)
    with col_example:
        if COMPONENTS_EXAMPLE_JSON.exists():
            st.download_button(
                "下载 components JSON 示例",
                COMPONENTS_EXAMPLE_JSON.read_bytes(),
                file_name=COMPONENTS_EXAMPLE_JSON.name,
                mime="application/json",
            )
        else:
            st.warning(f"找不到示例文件：{COMPONENTS_EXAMPLE_JSON}")
    with col_guide:
        if COMPONENTS_JSON_GUIDE.exists():
            st.download_button(
                "下载填写帮助文档",
                COMPONENTS_JSON_GUIDE.read_bytes(),
                file_name=COMPONENTS_JSON_GUIDE.name,
                mime="text/markdown",
            )
        else:
            st.warning(f"找不到帮助文档：{COMPONENTS_JSON_GUIDE}")

    with st.form("components_to_gil"):
        input_gil_upload = st.file_uploader("输入地图 .gil", type=["gil"], key="components_gil")
        components_upload = st.file_uploader("components.example.json 同格式 JSON", type=["json"], key="components_json")
        # template_upload = st.file_uploader("Template.gil，可不传", type=["gil"], key="components_template")
        template_upload = None
        output_name = st.text_input("输出文件名", value="components_output.gil")
        submitted = st.form_submit_button("生成 GIL", type="primary")

    if submitted:
        if not input_gil_upload or not components_upload:
            st.error("需要上传地图 .gil 和 components JSON。")
            return
        if not template_upload and not DEFAULT_TEMPLATE_GIL.exists():
            st.error(f"默认 Template.gil 不存在：{DEFAULT_TEMPLATE_GIL}")
            return
        with tempfile.TemporaryDirectory(prefix="qx_components_") as tmp:
            tmp_dir = Path(tmp)
            input_gil = write_upload(input_gil_upload, tmp_dir / "input.gil")
            components_json = write_upload(components_upload, tmp_dir / "components.json")
            template_gil = (
                write_upload(template_upload, tmp_dir / "Template.gil")
                if template_upload
                else DEFAULT_TEMPLATE_GIL
            )
            output_gil = tmp_dir / output_name
            try:
                summary = build_components_gil(input_gil, components_json, template_gil, output_gil)
            except Exception as exc:
                st.exception(exc)
                return
            st.success("GIL 已生成")
            st.json(summary, expanded=False)
            st.download_button("下载处理后的 GIL", output_gil.read_bytes(), file_name=output_gil.name)


def page_import_variables() -> None:
    st.header("导入变量")
    st.caption("上传结构体 JSON、结构体定义 GIA 或地图 GIL 后，按字段可视化编辑一个结构体值，并导出为 P2Gia 同格式的数据结构 JSON。")

    structs_doc: dict[str, Any] | None = None
    structs_upload = st.file_uploader(
        "上传结构体格式 structs.json、数据结构.gia 或 地图.gil",
        type=["json", "gia", "gil"],
        key="visual_structs_source",
    )
    if structs_upload:
        try:
            suffix = Path(structs_upload.name).suffix.lower()
            if suffix == ".json":
                structs_doc = normalize_structs_doc(
                    json.loads(read_text_upload(structs_upload)),
                    source_name=structs_upload.name,
                )
            elif suffix in (".gia", ".gil"):
                with tempfile.TemporaryDirectory(prefix="qx_struct_schema_source_") as tmp:
                    source_path = write_upload(structs_upload, Path(tmp) / structs_upload.name)
                    structs_doc = extract_structs_by_uploaded_format(source_path)
            else:
                raise ValueError("只支持 .json、.gia 或 .gil。")
            struct_count = int(structs_doc.get("struct_count") or len(structs_doc.get("structs", [])))
            source_format = structs_doc.get("source_format") or suffix.lstrip(".")
            extraction_mode = structs_doc.get("extraction_mode") or "structs_json"
            st.success(f"已读取结构体：{struct_count} 个（{source_format} / {extraction_mode}）")
        except Exception as exc:
            st.error(f"结构体格式解析失败：{exc}")
            structs_doc = None

    if not structs_doc or not structs_doc.get("structs"):
        st.info("先上传从“导出结构体 JSON”得到的 structs.json，或上传包含结构体定义的 数据结构.gia / 地图.gil。")
        return

    struct_names = [
        str(item.get("name") or item.get("id"))
        for item in structs_doc.get("structs", [])
        if item.get("name") or item.get("id")
    ]
    selected_struct = st.selectbox("选择要编辑的结构体", struct_names, key="visual_struct_name")
    selected_struct_doc = find_struct_doc(structs_doc, selected_struct)
    if not selected_struct_doc:
        st.error("未找到选中的结构体。")
        return

    output_name = st.text_input("输出 JSON 文件名", value=f"{selected_struct}.json", key="visual_output_json_name")

    with st.expander("结构体字段", expanded=False):
        st.dataframe(
            [
                {
                    "字段": field.get("name"),
                    "类型": field.get("type") or TYPE_INFO.get(int(field.get("type_code", 0)), {}).get("name"),
                    "type_code": field.get("type_code"),
                }
                for field in selected_struct_doc.get("fields", [])
            ],
            use_container_width=True,
        )

    st.subheader("编辑结构体字段")
    value = render_struct_value_editor(selected_struct_doc, structs_doc, "visual_struct_editor")
    try:
        data_json = struct_value_to_data_json(selected_struct_doc, structs_doc, value)
        preview_json = json.dumps(data_json, ensure_ascii=False, indent=4) + "\n"
    except Exception as exc:
        st.error(f"结构体数据 JSON 生成失败：{exc}")
        return

    with st.expander("预览数据结构 JSON", expanded=True):
        st.code(preview_json, language="json")

    output_name = output_name.strip() or f"{selected_struct}.json"
    if not output_name.lower().endswith(".json"):
        output_name += ".json"
    st.download_button(
        "下载数据结构 JSON",
        preview_json.encode("utf-8"),
        file_name=output_name,
        mime="application/json",
        type="primary",
        key="visual_download_data_json",
    )


def page_story_gil_export() -> None:
    st.subheader("story.txt 写入地图 GIL")
    with st.form("story_to_gil"):
        input_gil_upload = st.file_uploader("关卡 .gil", type=["gil"], key="story_gil_export_gil")
        story_upload = st.file_uploader("story_board 导出的 story.txt", type=["txt"], key="story_gil_export_txt")
        template_upload = st.file_uploader("Template.gil，可不传", type=["gil"], key="story_gil_export_template")
        component_name = st.text_input(
            "新增元件名称",
            value="",
            placeholder="例如：第一章",
            key="story_gil_export_name",
        )
        max_lines = st.number_input(
            "每个 Story 变量包含的节点数",
            min_value=1,
            max_value=200,
            value=10,
            key="story_gil_export_max_lines",
        )
        output_name = st.text_input("输出文件名", value="story_output.gil", key="story_gil_export_output")
        submitted = st.form_submit_button("生成处理后的 GIL", type="primary")

    if submitted:
        if not input_gil_upload or not story_upload:
            st.error("需要上传关卡 .gil 和 story.txt。")
            return
        component_name = component_name.strip()
        if not component_name:
            st.error("需要输入新增元件名称。")
            return
        if not template_upload and not DEFAULT_TEMPLATE_GIL.exists():
            st.error(f"默认 Template.gil 不存在：{DEFAULT_TEMPLATE_GIL}")
            return
        with tempfile.TemporaryDirectory(prefix="qx_story_gil_") as tmp:
            tmp_dir = Path(tmp)
            input_gil = write_upload(input_gil_upload, tmp_dir / "input.gil")
            template_gil = (
                write_upload(template_upload, tmp_dir / "Template.gil")
                if template_upload
                else DEFAULT_TEMPLATE_GIL
            )
            output_gil = tmp_dir / output_name
            try:
                summary = build_story_gil(
                    input_gil,
                    template_gil,
                    read_text_upload(story_upload),
                    component_name,
                    output_gil,
                    int(max_lines),
                )
            except Exception as exc:
                st.exception(exc)
                return
            st.success("GIL 已生成")
            st.json(summary, expanded=False)
            st.download_button("下载处理后的 GIL", output_gil.read_bytes(), file_name=output_gil.name)


def page_export_component() -> None:
    st.header("导出元件")
    # st.caption("工程类导出能力集中在这里，避免可视化剧情页加载过多逻辑。")
    tab_story, tab_structs, tab_components = st.tabs(
        ["story.txt 写入 GIL", "导出结构体 JSON", "components JSON 构建 GIL"]
    )
    with tab_story:
        page_story_gil_export()
    with tab_structs:
        page_extract_structs()
    with tab_components:
        page_components_builder()


def page_camera_generator() -> None:
    st.header("镜头 GIA 生成")
    with st.form("camera_gia"):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            steps = st.number_input("镜头数量", min_value=1, max_value=500, value=16)
            output_name = st.text_input("输出文件名", value="camera_zoom.gia")
        with col_b:
            distance_start = st.number_input("起始距离", value=3.0)
            distance_end = st.number_input("结束距离", value=2.7)
        with col_c:
            fov_start = st.number_input("起始 FOV", value=60.0)
            fov_end = st.number_input("结束 FOV", value=45.0)

        curve = st.selectbox(
            "变化方式",
            [
                "linear",
                "ease_in_quad",
                "ease_out_quad",
                "ease_in_out_cubic",
                "smoothstep",
                "exponential",
            ],
            format_func={
                "linear": "线性",
                "ease_in_quad": "非线性：慢起",
                "ease_out_quad": "非线性：慢停",
                "ease_in_out_cubic": "非线性：慢起慢停",
                "smoothstep": "平滑 S 曲线",
                "exponential": "指数曲线",
            }.get,
        )
        strength = st.slider("指数曲线强度", min_value=-6.0, max_value=6.0, value=2.0, step=0.1)
        record_start = st.number_input("起始镜头 ID", min_value=1, value=0x40000002)
        version = st.text_input("版本字段", value=DEFAULT_VERSION)
        submitted = st.form_submit_button("生成 GIA", type="primary")

    if submitted:
        try:
            data = build_camera_gia(
                output_name=output_name,
                steps=int(steps),
                distance_start=float(distance_start),
                distance_end=float(distance_end),
                fov_start=float(fov_start),
                fov_end=float(fov_end),
                curve=curve,
                strength=float(strength),
                record_start=int(record_start),
                version=version,
            )
        except Exception as exc:
            st.exception(exc)
            return
        st.success(f"GIA 已生成：{len(data)} bytes")
        st.download_button("下载镜头 GIA", data, file_name=output_name)


def main() -> None:
    st.set_page_config(page_title="千星工具箱", layout="wide")

    page = st.sidebar.radio(
        "功能",
        [
            "可视化剧情构建",
            "导入变量",
            "导出元件",
            "镜头 GIA 生成",
        ],
    )

    if page == "可视化剧情构建":
        page_story_builder()
    elif page == "导入变量":
        st.title("千星工具箱")
        page_import_variables()
    elif page == "导出元件":
        st.title("千星工具箱")
        page_export_component()
    elif page == "镜头 GIA 生成":
        st.title("千星工具箱")
        page_camera_generator()


if __name__ == "__main__":
    main()
