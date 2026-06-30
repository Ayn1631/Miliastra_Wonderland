from __future__ import annotations

import copy
import hashlib
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
STRUCT_PARSER_CACHE_VERSION = "gia-inline-layout-v5-keyed-sample"
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

APP_PAGE_CSS = """
<style>
:root {
  --qx-bg: #f5f7fb;
  --qx-panel: #ffffff;
  --qx-panel-soft: #f8fafc;
  --qx-border: #d9e1ec;
  --qx-text: #172033;
  --qx-muted: #667085;
  --qx-accent: #e5484d;
  --qx-accent-hover: #d7353d;
  --qx-green-bg: #e8f7ee;
  --qx-green-text: #087443;
}

.stApp {
  background: var(--qx-bg);
  color: var(--qx-text);
}

[data-testid="stHeader"] {
  background: transparent;
}

[data-testid="stSidebar"] {
  background: #eef2f7;
  border-right: 1px solid var(--qx-border);
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
  gap: 0.65rem;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
  border-radius: 8px;
  padding: 0.32rem 0.42rem;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
  background: #e3e9f2;
}

[data-testid="stMainBlockContainer"],
.block-container {
  max-width: 1180px;
  padding-top: 2rem;
  padding-bottom: 3rem;
}

h1 {
  color: var(--qx-text);
  font-size: 2.35rem !important;
  line-height: 1.14 !important;
  margin-bottom: 0.35rem !important;
}

h2, h3 {
  color: var(--qx-text);
  letter-spacing: 0;
}

[data-testid="stCaptionContainer"] {
  color: var(--qx-muted);
}

[data-testid="stForm"],
[data-testid="stExpander"],
[data-testid="stFileUploader"],
[data-testid="stDataFrame"],
[data-testid="stJson"] {
  border-radius: 8px;
}

[data-testid="stForm"] {
  background: var(--qx-panel);
  border: 1px solid var(--qx-border);
  padding: 1.1rem 1.15rem 1.25rem;
}

[data-testid="stFileUploader"] section {
  background: var(--qx-panel-soft);
  border: 1px dashed #b7c3d4;
  border-radius: 8px;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="select"] > div {
  border-radius: 8px !important;
  border-color: #cfd8e6 !important;
  background: #f9fbfd !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: #7a8da8 !important;
  box-shadow: 0 0 0 1px #7a8da8 inset !important;
}

[data-testid="stTextInput"] input:disabled {
  color: #596579;
  -webkit-text-fill-color: #596579;
  background: #eef2f7 !important;
}

.stButton > button,
.stDownloadButton > button,
[data-testid="stFormSubmitButton"] button {
  border-radius: 8px;
  font-weight: 650;
  border: 1px solid #cbd5e1;
  min-height: 2.45rem;
}

.stButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"],
[data-testid="stFormSubmitButton"] button[kind="primary"] {
  background: var(--qx-accent);
  border-color: var(--qx-accent);
}

.stButton > button[kind="primary"]:hover,
.stDownloadButton > button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] button[kind="primary"]:hover {
  background: var(--qx-accent-hover);
  border-color: var(--qx-accent-hover);
}

[data-testid="stTabs"] [role="tablist"] {
  gap: 0.25rem;
  border-bottom: 1px solid var(--qx-border);
}

[data-testid="stTabs"] [role="tab"] {
  border-radius: 8px 8px 0 0;
  padding: 0.55rem 0.8rem;
}

[data-testid="stTabs"] [aria-selected="true"] {
  background: var(--qx-panel);
  color: var(--qx-text);
}

[data-testid="stAlert"] {
  border-radius: 8px;
  border: 1px solid transparent;
}

[data-testid="stAlert"]:has([data-testid="stMarkdownContainer"] p) {
  box-shadow: none;
}

[data-testid="stSuccess"] {
  background: var(--qx-green-bg);
  color: var(--qx-green-text);
}

.qx-shell-title {
  font-size: 0.78rem;
  color: #667085;
  letter-spacing: 0;
  margin: 0.25rem 0 0.35rem;
}

.qx-shell-brand {
  font-size: 1.05rem;
  font-weight: 750;
  color: #172033;
  margin-bottom: 0.8rem;
}

.qx-page-kicker {
  color: #667085;
  font-size: 0.85rem;
  margin-bottom: 0.15rem;
}

.qx-page-title {
  color: #172033;
  font-size: 2.25rem;
  font-weight: 760;
  line-height: 1.15;
  margin: 0 0 1.2rem;
}

.qx-page-hero {
  background: #ffffff;
  border: 1px solid #d9e1ec;
  border-radius: 8px;
  padding: 1.1rem 1.2rem 1.2rem;
  margin-bottom: 1.15rem;
}

.qx-field-table-title {
  color: #667085;
  font-size: 0.82rem;
  margin: 0 0 0.35rem;
}

.qx-field-head {
  color: #475467;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  background: #eef2f7;
  border: 1px solid #d9e1ec;
  border-radius: 8px;
  padding: 0.45rem 0.6rem;
}

.qx-field-name {
  color: #172033;
  font-weight: 700;
  padding-top: 0.42rem;
}

.qx-field-meta {
  color: #667085;
  font-size: 0.78rem;
}

.qx-type-pill {
  display: inline-flex;
  align-items: center;
  min-height: 1.7rem;
  padding: 0.2rem 0.52rem;
  border-radius: 999px;
  background: #eef2f7;
  border: 1px solid #d9e1ec;
  color: #344054;
  font-size: 0.8rem;
  font-weight: 650;
  margin-top: 0.28rem;
}

.qx-field-divider {
  height: 1px;
  background: #e3e8f0;
  margin: 0.55rem 0;
}

.qx-nested-note {
  color: #667085;
  font-size: 0.8rem;
  margin: -0.15rem 0 0.45rem;
}

.qx-list-toolbar {
  color: #667085;
  font-size: 0.82rem;
  margin: 0.1rem 0 0.35rem;
}

code,
pre {
  border-radius: 8px !important;
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
    27: "Dict",
}

LIST_TYPE_CODES = {7, 8, 9, 10, 11, 13, 15, 22, 23, 24}


def write_upload(uploaded_file: Any, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(uploaded_file.getvalue())
    return path


def read_text_upload(uploaded_file: Any) -> str:
    return decode_text_bytes(uploaded_file.getvalue())


def decode_text_bytes(raw: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


@st.cache_data(show_spinner=False)
def parse_structs_upload_cached(file_name: str, raw: bytes, parser_version: str) -> dict[str, Any]:
    suffix = Path(file_name).suffix.lower()
    if suffix == ".json":
        return normalize_structs_doc(
            json.loads(decode_text_bytes(raw)),
            source_name=file_name,
        )
    if suffix in (".gia", ".gil"):
        with tempfile.TemporaryDirectory(prefix="qx_struct_schema_source_") as tmp:
            source_path = Path(tmp) / file_name
            source_path.parent.mkdir(parents=True, exist_ok=True)
            source_path.write_bytes(raw)
            result = extract_structs_by_uploaded_format(source_path)
            result["parser_cache_version"] = parser_version
            return result
    raise ValueError("只支持 .json、.gia 或 .gil。")


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


def struct_doc_identity(struct_doc: dict[str, Any]) -> str:
    struct_id = struct_doc.get("id")
    name = struct_doc.get("name")
    if struct_id is not None:
        return f"id:{struct_id}"
    if name:
        return f"name:{name}"
    return f"object:{id(struct_doc)}"


def param_type_name(type_code: int | None) -> str:
    if type_code is None:
        return "Unknown"
    return PARAM_TYPE_BY_CODE.get(type_code) or TYPE_INFO.get(type_code, {}).get("name", f"type_{type_code}")


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
        return {"type": "Dict", "key_type": "Int32", "value_type": "String", "value": []}
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


def parse_gia_inline_struct_layout_candidate(
    candidate: dict[str, Any],
    *,
    source_record_index: int,
    schema_path: str,
) -> dict[str, Any] | None:
    candidate_fields = gia_chapters.children(candidate)
    struct_id = gia_chapters.varint(candidate_fields, 501)
    field_messages = gia_chapters.all_fields(candidate_fields, 1)
    if not isinstance(struct_id, int) or not field_messages:
        return None

    fields: list[dict[str, Any]] = []
    for index, field_message in enumerate(field_messages, start=1):
        field_fields = gia_chapters.children(field_message)
        field_name = gia_chapters.utf8(field_fields, 501)
        type_code = gia_chapters.varint(field_fields, 1)
        if not field_name or type_code is None:
            return None

        field_doc = {
            "index": index,
            "name": field_name,
            "type_code": int(type_code),
            "type": TYPE_INFO.get(int(type_code), {}).get("name", f"type_{type_code}"),
        }

        nested_struct_id = nested_varint_value(field_message, [2, 2, 2])
        if nested_struct_id is not None and int(type_code) in (25, 26):
            key_name = "element_struct_id" if int(type_code) == 26 else "struct_id"
            field_doc[key_name] = int(nested_struct_id)

        if int(type_code) == 27:
            dict_meta = gia_chapters.first_field(field_fields, 37)
            dict_fields = gia_chapters.children(dict_meta)
            key_type_code = gia_chapters.varint(dict_fields, 503)
            value_type_code = gia_chapters.varint(dict_fields, 504)
            value_struct_id = gia_chapters.varint(dict_fields, 505)
            if key_type_code is not None:
                field_doc["dict_key_type_code"] = int(key_type_code)
            if value_type_code is not None:
                field_doc["dict_value_type_code"] = int(value_type_code)
            if value_struct_id is not None:
                field_doc["dict_value_struct_id"] = int(value_struct_id)

        fields.append(field_doc)

    return {
        "id": int(struct_id),
        "name": f"struct_{struct_id}",
        "field_count": len(fields),
        "fields": fields,
        "schema_offset": candidate.get("offset"),
        "schema_length": candidate.get("length"),
        "source_record_index": source_record_index,
        "schema_path": schema_path,
        "layout_source": "gia_inline_layout",
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
    inline_layouts: dict[int, dict[str, Any]] = {}
    seen_signatures: set[tuple[int, str]] = set()

    for record_index, record in enumerate(gia_chapters.all_fields(root, 1), start=1):
        struct_id = nested_varint_value(record, [1, 4])

        for candidate in iter_message_tree(record):
            inline_schema = parse_gia_inline_struct_layout_candidate(
                candidate,
                source_record_index=record_index,
                schema_path=f"record[{record_index}]",
            )
            if inline_schema:
                existing = inline_layouts.get(inline_schema["id"])
                if existing is None or inline_schema["field_count"] > existing["field_count"]:
                    inline_layouts[inline_schema["id"]] = inline_schema

            if struct_id is not None:
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

    if not structs:
        raise ValueError("没有在 GIA 中找到结构体定义记录。")

    for struct_doc in structs:
        inline_schema = inline_layouts.get(int(struct_doc["id"]))
        if not inline_schema:
            continue
        struct_doc["fields"] = inline_schema["fields"]
        struct_doc["field_count"] = inline_schema["field_count"]
        struct_doc["layout_source"] = inline_schema["layout_source"]
        struct_doc["layout_offset"] = inline_schema.get("schema_offset")
        struct_doc["layout_length"] = inline_schema.get("schema_length")

    return {
        "file": str(gia_path),
        "size": len(data),
        "source_format": "gia",
        "extraction_mode": "gia_schema_records_with_inline_layout",
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
        except ValueError as exc:
            raise ValueError(
                "没有在 GIA 中解析到可导出的高级数据结构定义，"
                "因此不会展示 Story/StoryNode 等推断结构体。请上传包含结构体定义的 .gia/.gil，"
                "或上传从真实结构体文件导出的 structs.json。"
            ) from exc
    raise ValueError(f"不支持的文件格式：{path.suffix}。请上传 .gil 或 .gia。")


def normalize_structs_doc(data: Any, *, source_name: str = "") -> dict[str, Any]:
    if isinstance(data, list):
        data = {"structs": data}
    if not isinstance(data, dict):
        raise ValueError("结构体数据顶层必须是对象，或直接是结构体数组。")
    if data.get("extraction_mode") == "inferred_story_structs":
        raise ValueError("这个 structs.json 是旧版推断结构体结果，不是真实高级数据结构定义。请重新上传含结构体定义的 GIA/GIL 导出。")
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


def coerce_param_value(type_code: int, value: Any, field: dict[str, Any] | None = None) -> Any:
    if type_code in (3, 17, 20, 21):
        return str(int(value or 0))
    if type_code == 4:
        return bool(value)
    if type_code == 5:
        return f"{float(value or 0.0):.2f}"
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
    if type_code == 27:
        field = field or {}
        key_type_code = field.get("dict_key_type_code")
        value_type_code = field.get("dict_value_type_code")
        value_struct_id = field.get("dict_value_struct_id")
        existing = value if isinstance(value, dict) else {}
        result = {
            "type": "Dict",
            "key_type": param_type_name(int(key_type_code)) if key_type_code is not None else existing.get("key_type") or "Int32",
            "value_type": param_type_name(int(value_type_code)) if value_type_code is not None else existing.get("value_type") or "String",
            "value": existing.get("value") if isinstance(existing.get("value"), list) else [],
        }
        if value_struct_id is not None:
            result["value_structId"] = str(value_struct_id)
        elif existing.get("value_structId") is not None:
            result["value_structId"] = str(existing.get("value_structId"))
        return result
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
                "value": coerce_param_value(type_code, field_value, field),
            }
        )

    return {
        "structId": struct_id_text(struct_doc),
        "type": "Struct",
        "value": params,
    }


def unwrap_exported_param(param: dict[str, Any]) -> dict[str, Any]:
    wrapped = param.get("value")
    if isinstance(wrapped, dict) and isinstance(wrapped.get("value"), (dict, list, str, int, float, bool, type(None))):
        if str(wrapped.get("param_type") or "").lower() == str(param.get("param_type") or "").lower():
            return wrapped
    return param


def is_keyed_export_json(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    params = data.get("value")
    return isinstance(params, list) and any(isinstance(item, dict) and "key" in item for item in params)


def find_struct_doc_by_name_or_id(structs_doc: dict[str, Any], name_or_id: Any) -> dict[str, Any] | None:
    text = str(name_or_id or "")
    return find_struct_doc(structs_doc, text)


def reorder_struct_fields_from_keyed_export(
    struct_doc: dict[str, Any],
    export_json: dict[str, Any],
) -> bool:
    params = export_json.get("value") if isinstance(export_json, dict) else None
    if not isinstance(params, list):
        return False

    fields = list(struct_doc.get("fields", []))
    fields_by_name = {str(field.get("name") or ""): field for field in fields}
    ordered_fields: list[dict[str, Any]] = []
    used_names: set[str] = set()

    for param in params:
        key = str(param.get("key") or "") if isinstance(param, dict) else ""
        if not key or key not in fields_by_name:
            return False
        field = copy.deepcopy(fields_by_name[key])
        expected_type = param_type_name(int(field.get("type_code", 0)))
        actual_type = str(param.get("param_type") or "")
        if actual_type.lower() != expected_type.lower():
            raise ValueError(f"{struct_doc.get('name')} 字段 {key} 期望 {expected_type}，但导出 JSON 是 {actual_type}。")
        used_names.add(key)
        ordered_fields.append(field)

    if len(ordered_fields) != len(fields):
        missing = [str(field.get("name") or "") for field in fields if str(field.get("name") or "") not in used_names]
        raise ValueError(f"{struct_doc.get('name')} 的导出 JSON 没有覆盖全部字段：{', '.join(missing)}")

    for index, field in enumerate(ordered_fields, start=1):
        field["index"] = index
    struct_doc["fields"] = ordered_fields
    struct_doc["field_count"] = len(ordered_fields)
    struct_doc["layout_source"] = "keyed_export_json"
    return True


def keyed_export_to_data_json(
    export_json: dict[str, Any],
    struct_doc: dict[str, Any],
    structs_doc: dict[str, Any],
) -> dict[str, Any]:
    params = export_json.get("value") if isinstance(export_json, dict) else None
    if not isinstance(params, list):
        raise ValueError("导出变量 JSON 缺少 value 数组。")

    converted_params: list[dict[str, Any]] = []
    for field, param in zip(sorted(struct_doc.get("fields", []), key=lambda item: int(item.get("index", 0))), params):
        if not isinstance(param, dict):
            continue
        inner = unwrap_exported_param(param)
        converted = {"param_type": inner.get("param_type") or param.get("param_type"), "value": inner.get("value")}
        type_code = int(field.get("type_code", 0))
        if type_code == 25 and isinstance(converted.get("value"), dict):
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            if nested_doc:
                converted["value"] = normalize_export_data_json(converted["value"], structs_doc, nested_doc)
        elif type_code == 26 and isinstance(converted.get("value"), dict):
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            raw_list = converted["value"]
            items = raw_list.get("value") if isinstance(raw_list.get("value"), list) else []
            normalized_items: list[dict[str, Any]] = []
            for item in items:
                if isinstance(item, dict) and item.get("param_type") == "Struct" and isinstance(item.get("value"), dict):
                    item_value = item["value"]
                    if nested_doc:
                        item_value = normalize_export_data_json(item_value, structs_doc, nested_doc)
                    normalized_items.append({"param_type": "Struct", "value": item_value})
            nested_struct_id = raw_list.get("structId")
            if not nested_struct_id and nested_doc:
                nested_struct_id = struct_id_text(nested_doc)
            converted["value"] = {"structId": nested_struct_id, "value": normalized_items}
        converted_params.append(converted)

    return {
        "structId": struct_id_text(struct_doc),
        "type": "Struct",
        "value": converted_params,
    }


def normalize_export_data_json(
    data_json: dict[str, Any],
    structs_doc: dict[str, Any],
    selected_struct_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if is_keyed_export_json(data_json):
        struct_doc = selected_struct_doc or find_struct_doc_by_name_or_id(structs_doc, data_json.get("name"))
        if struct_doc is None:
            raise ValueError(f"找不到导出变量 JSON 对应的结构体：{data_json.get('name')}")
        reorder_struct_fields_from_keyed_export(struct_doc, data_json)
        return keyed_export_to_data_json(data_json, struct_doc, structs_doc)
    return data_json


def coerce_widget_value(type_code: int, raw_value: Any) -> Any:
    if type_code in (3, 17, 20, 21):
        return int(raw_value or 0)
    if type_code == 4:
        return bool(raw_value)
    if type_code == 5:
        return float(raw_value or 0.0)
    if type_code == 6:
        return "" if raw_value is None else str(raw_value)
    if type_code in (8, 24):
        return [int(item or 0) for item in (raw_value or [])]
    if type_code == 9:
        return [bool(item) for item in (raw_value or [])]
    if type_code == 10:
        return [float(item or 0.0) for item in (raw_value or [])]
    if type_code in (7, 11, 13, 22, 23):
        return [str(item) for item in (raw_value or [])]
    if type_code in (12, 27):
        return raw_value if isinstance(raw_value, dict) else default_value_for_type(type_code)
    if type_code == 15:
        return raw_value if isinstance(raw_value, list) else []
    return raw_value


def data_json_to_struct_value(
    struct_doc: dict[str, Any],
    structs_doc: dict[str, Any],
    data_json: dict[str, Any],
) -> dict[str, Any]:
    params = data_json.get("value") if isinstance(data_json, dict) else None
    if not isinstance(params, list):
        return {}

    value: dict[str, Any] = {}
    fields = sorted(struct_doc.get("fields", []), key=lambda item: int(item.get("index", 0)))
    for index, field in enumerate(fields):
        param = params[index] if index < len(params) else None
        if not isinstance(param, dict):
            continue
        field_name = str(field.get("name") or "").strip()
        if not field_name:
            continue
        type_code = int(field.get("type_code", 0))
        expected_param_type = param_type_name(type_code)
        actual_param_type = str(param.get("param_type") or "")
        if actual_param_type.lower() != expected_param_type.lower():
            raise ValueError(
                f"结构体 {struct_doc.get('name') or struct_doc.get('id')} 第 {index + 1} 位字段 "
                f"{field_name} 期望 {expected_param_type}，但数据 JSON 是 {actual_param_type}。"
                "已停止导入，避免按类型重排导致字段错位。"
            )
        raw_value = param.get("value")

        if type_code == 25 and isinstance(raw_value, dict):
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            value[field_name] = data_json_to_struct_value(nested_doc, structs_doc, raw_value) if nested_doc else {}
            continue

        if type_code == 26 and isinstance(raw_value, dict):
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            raw_items = raw_value.get("value") if isinstance(raw_value.get("value"), list) else []
            items: list[dict[str, Any]] = []
            for raw_item in raw_items:
                item_value = raw_item.get("value") if isinstance(raw_item, dict) else None
                if nested_doc and isinstance(item_value, dict):
                    items.append(data_json_to_struct_value(nested_doc, structs_doc, item_value))
            value[field_name] = items
            continue

        value[field_name] = coerce_widget_value(type_code, raw_value)
    return value


def struct_order_is_extracted(struct_doc: dict[str, Any], structs_doc: dict[str, Any]) -> bool:
    if structs_doc.get("source_format") != "gia":
        return True
    return struct_doc.get("layout_source") in ("gia_inline_layout", "keyed_export_json")


def param_at(data_json: dict[str, Any] | None, index: int) -> dict[str, Any] | None:
    params = data_json.get("value") if isinstance(data_json, dict) else None
    if not isinstance(params, list) or index >= len(params):
        return None
    param = params[index]
    return param if isinstance(param, dict) else None


def collect_unverified_order_structs(
    struct_doc: dict[str, Any],
    structs_doc: dict[str, Any],
    data_json: dict[str, Any] | None = None,
    *,
    path: str = "",
    seen: set[str] | None = None,
) -> list[str]:
    seen = seen or set()
    struct_key = struct_id_text(struct_doc)
    if struct_key in seen:
        return []
    seen.add(struct_key)

    current_path = path or str(struct_doc.get("name") or struct_doc.get("id"))
    problems: list[str] = []

    if not struct_order_is_extracted(struct_doc, structs_doc):
        if data_json is None:
            problems.append(f"{current_path}：没有在 GIA 中提取到变量实际顺序，需要上传导出变量 JSON 校验。")
        else:
            try:
                data_json_to_struct_value(struct_doc, structs_doc, data_json)
            except Exception as exc:
                problems.append(f"{current_path}：导出变量 JSON 与当前解析顺序不一致，{exc}")

    fields = sorted(struct_doc.get("fields", []), key=lambda item: int(item.get("index", 0)))
    for index, field in enumerate(fields):
        type_code = int(field.get("type_code", 0))
        field_name = str(field.get("name") or f"field_{index + 1}")
        if type_code == 25:
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            nested_param = param_at(data_json, index)
            nested_data = nested_param.get("value") if isinstance(nested_param, dict) else None
            if nested_doc:
                problems.extend(
                    collect_unverified_order_structs(
                        nested_doc,
                        structs_doc,
                        nested_data if isinstance(nested_data, dict) else None,
                        path=f"{current_path}.{field_name}",
                        seen=seen.copy(),
                    )
                )
        elif type_code == 26:
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            nested_param = param_at(data_json, index)
            nested_data = nested_param.get("value") if isinstance(nested_param, dict) else None
            sample_items = nested_data.get("value") if isinstance(nested_data, dict) else None
            first_item = sample_items[0] if isinstance(sample_items, list) and sample_items else None
            first_item_data = first_item.get("value") if isinstance(first_item, dict) else None
            if nested_doc:
                if not struct_order_is_extracted(nested_doc, structs_doc) and data_json is not None and not isinstance(first_item_data, dict):
                    problems.append(f"{current_path}.{field_name}：结构体列表没有样本项，无法校验元素结构体顺序。")
                    continue
                problems.extend(
                    collect_unverified_order_structs(
                        nested_doc,
                        structs_doc,
                        first_item_data if isinstance(first_item_data, dict) else None,
                        path=f"{current_path}.{field_name}[]",
                        seen=seen.copy(),
                    )
                )
    return problems


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


def list_count_controls(key: str, *, default_count: int = 0, max_count: int = 200) -> int:
    count_key = f"{key}_count"
    if count_key not in st.session_state:
        st.session_state[count_key] = default_count

    current = int(st.session_state.get(count_key, default_count))
    current = max(0, min(max_count, current))
    st.session_state[count_key] = current

    if st.button("添加一项", key=f"{key}_add", disabled=current >= max_count):
        st.session_state[count_key] = min(max_count, current + 1)
        current = int(st.session_state[count_key])
    if st.button("删除最后一项", key=f"{key}_remove", disabled=current <= 0):
        st.session_state[count_key] = max(0, current - 1)
        current = int(st.session_state[count_key])
    st.markdown(
        f'<div class="qx-list-toolbar">当前 {current} 项</div>',
        unsafe_allow_html=True,
    )
    return current


def render_list_item_input(type_code: int, key: str, index: int, initial_value: Any = None) -> Any:
    label = f"第 {index + 1} 项"
    if type_code in (8, 24):
        return int(st.number_input(label, value=int(initial_value or 0), step=1, key=key, label_visibility="collapsed"))
    if type_code == 10:
        return float(st.number_input(label, value=float(initial_value or 0.0), key=key, label_visibility="collapsed"))
    if type_code == 9:
        return st.checkbox(label, value=bool(initial_value), key=key)
    if type_code == 15:
        vector = initial_value if isinstance(initial_value, dict) else {}
        return {
            "x": float(st.number_input("x", value=float(vector.get("x") or 0.0), key=f"{key}_x")),
            "y": float(st.number_input("y", value=float(vector.get("y") or 0.0), key=f"{key}_y")),
            "z": float(st.number_input("z", value=float(vector.get("z") or 0.0), key=f"{key}_z")),
        }
    return st.text_input(label, value="" if initial_value is None else str(initial_value), key=key, label_visibility="collapsed")


def render_list_field_input(type_code: int, key: str, initial_value: Any = None) -> list[Any]:
    initial_items = initial_value if isinstance(initial_value, list) else []
    count = list_count_controls(key, default_count=len(initial_items))
    values: list[Any] = []
    for index in range(count):
        st.markdown(
            f'<div class="qx-field-meta">#{index + 1}</div>',
            unsafe_allow_html=True,
        )
        item_initial = initial_items[index] if index < len(initial_items) else None
        values.append(render_list_item_input(type_code, f"{key}_item_{index}", index, item_initial))
    return values


def render_scalar_field_input(
    field: dict[str, Any],
    key: str,
    *,
    compact: bool = False,
    initial_value: Any = None,
) -> Any:
    field_name = str(field.get("name") or "")
    type_code = int(field.get("type_code", 0))
    type_name = field.get("type") or TYPE_INFO.get(type_code, {}).get("name", f"type_{type_code}")
    label = f"{field_name} ({type_name})"
    label_visibility = "collapsed" if compact else "visible"
    if type_code in LIST_TYPE_CODES:
        return render_list_field_input(type_code, key, initial_value)
    if type_code == 6:
        return st.text_input(label, value="" if initial_value is None else str(initial_value), key=key, label_visibility=label_visibility)
    if type_code == 3:
        return int(st.number_input(label, value=int(initial_value or 0), step=1, key=key, label_visibility=label_visibility))
    if type_code == 5:
        return float(st.number_input(label, value=float(initial_value or 0.0), key=key, label_visibility=label_visibility))
    if type_code == 4:
        return st.checkbox(label, value=bool(initial_value), key=key, label_visibility=label_visibility)
    if type_code == 12:
        vector = initial_value if isinstance(initial_value, dict) else {}
        if compact:
            return {
                "x": float(st.number_input("x", value=float(vector.get("x") or 0.0), key=f"{key}_x")),
                "y": float(st.number_input("y", value=float(vector.get("y") or 0.0), key=f"{key}_y")),
                "z": float(st.number_input("z", value=float(vector.get("z") or 0.0), key=f"{key}_z")),
            }
        cols = st.columns(3)
        return {
            "x": float(cols[0].number_input("x", value=float(vector.get("x") or 0.0), key=f"{key}_x")),
            "y": float(cols[1].number_input("y", value=float(vector.get("y") or 0.0), key=f"{key}_y")),
            "z": float(cols[2].number_input("z", value=float(vector.get("z") or 0.0), key=f"{key}_z")),
        }
    st.caption(f"{label} 暂按默认空值导出。")
    return default_value_for_type(type_code)


def render_struct_value_editor(
    struct_doc: dict[str, Any],
    structs_doc: dict[str, Any],
    key_prefix: str,
    *,
    depth: int = 0,
    ancestor_structs: tuple[str, ...] = (),
    initial_value: dict[str, Any] | None = None,
) -> dict[str, Any]:
    value: dict[str, Any] = {}
    initial_value = initial_value if isinstance(initial_value, dict) else {}
    current_struct_key = struct_doc_identity(struct_doc)
    current_ancestors = ancestor_structs + (current_struct_key,)
    st.markdown('<div class="qx-field-table-title">字段表格编辑</div>', unsafe_allow_html=True)
    header_cols = st.columns([1.5, 1.0, 3.7])
    header_cols[0].markdown('<div class="qx-field-head">字段</div>', unsafe_allow_html=True)
    header_cols[1].markdown('<div class="qx-field-head">类型</div>', unsafe_allow_html=True)
    header_cols[2].markdown('<div class="qx-field-head">值</div>', unsafe_allow_html=True)

    for field in struct_doc.get("fields", []):
        field_name = str(field.get("name") or "").strip()
        if not field_name:
            continue
        type_code = int(field.get("type_code", 0))
        type_name = field.get("type") or TYPE_INFO.get(type_code, {}).get("name", f"type_{type_code}")
        field_key = f"{key_prefix}_{field_name}_{type_code}_{depth}"
        field_initial = initial_value.get(field_name)
        st.markdown('<div class="qx-field-divider"></div>', unsafe_allow_html=True)
        field_cols = st.columns([1.5, 1.0, 3.7])
        field_cols[0].markdown(
            f"""
            <div class="qx-field-name">{field_name}</div>
            <div class="qx-field-meta">#{field.get("index", "")}</div>
            """,
            unsafe_allow_html=True,
        )
        field_cols[1].markdown(
            f'<span class="qx-type-pill">{type_name}</span>',
            unsafe_allow_html=True,
        )

        if type_code == 25:
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            nested_key = struct_doc_identity(nested_doc) if nested_doc else ""
            with field_cols[2]:
                st.text_input(
                    f"{field_name} (struct) 的结构体类型",
                    value=nested_struct_label(nested_doc),
                    disabled=True,
                    key=f"{field_key}_struct_fixed",
                    label_visibility="collapsed",
                )
            if nested_doc and nested_key in current_ancestors:
                st.warning("检测到结构体自引用。为避免页面无限递归，内层结构体保留为空对象。")
                value[field_name] = {}
            elif nested_doc:
                with st.expander(f"编辑 {field_name}", expanded=True):
                    value[field_name] = render_struct_value_editor(
                        nested_doc,
                        structs_doc,
                        f"{field_key}_nested",
                        depth=depth + 1,
                        ancestor_structs=current_ancestors,
                        initial_value=field_initial if isinstance(field_initial, dict) else {},
                    )
            else:
                st.error(f"{field_name} 的结构定义里没有可解析的内层结构体类型。")
                value[field_name] = {}
            continue
        if type_code == 26:
            nested_doc = resolve_nested_struct_doc(field, structs_doc)
            with field_cols[2]:
                st.text_input(
                    f"{field_name} (struct_list) 的元素结构体类型",
                    value=nested_struct_label(nested_doc),
                    disabled=True,
                    key=f"{field_key}_struct_list_fixed",
                    label_visibility="collapsed",
                )
                initial_items = field_initial if isinstance(field_initial, list) else []
                count = list_count_controls(field_key, default_count=len(initial_items) if initial_items else (1 if depth == 0 else 0))
            st.markdown(
                '<div class="qx-nested-note">列表项按下方展开区逐项编辑。</div>',
                unsafe_allow_html=True,
            )
            items: list[dict[str, Any]] = []
            for index in range(count):
                if nested_doc:
                    with st.expander(f"{field_name} #{index + 1}", expanded=index == 0):
                        items.append(
                            render_struct_value_editor(
                                nested_doc,
                                structs_doc,
                                f"{field_key}_item_{index}",
                                depth=depth + 1,
                                ancestor_structs=current_ancestors,
                                initial_value=initial_items[index] if index < len(initial_items) else {},
                            )
                        )
                else:
                    st.error(f"{field_name} 的结构定义里没有可解析的元素结构体类型。")
                    items.append({})
            value[field_name] = items
            continue
        with field_cols[2]:
            value[field_name] = render_scalar_field_input(field, field_key, compact=True, initial_value=field_initial)
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
        suffix = Path(uploaded.name).suffix.lower()
        try:
            with st.spinner("正在解析结构体，首次解析后会缓存结果..."):
                result = parse_structs_upload_cached(uploaded.name, uploaded.getvalue(), STRUCT_PARSER_CACHE_VERSION)
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
    st.caption("上传结构体 JSON、结构体定义 GIA 或地图 GIL 后，按字段可视化编辑一个结构体值，并导出为 P2Gia 同格式的数据结构 JSON。")

    structs_doc: dict[str, Any] | None = None
    initial_data_json: dict[str, Any] | None = None
    initial_data_token = "empty"
    structs_upload = st.file_uploader(
        "上传结构体格式 structs.json、数据结构.gia 或 地图.gil",
        type=["json", "gia", "gil"],
        key="visual_structs_source",
    )
    if structs_upload:
        try:
            suffix = Path(structs_upload.name).suffix.lower()
            with st.spinner("正在解析结构体，首次解析后会缓存结果..."):
                structs_doc = parse_structs_upload_cached(structs_upload.name, structs_upload.getvalue(), STRUCT_PARSER_CACHE_VERSION)
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

    data_upload = st.file_uploader(
        "上传导出变量 JSON（当 GIA 顺序不可信时必填，也可作为初始数据）",
        type=["json"],
        key="visual_struct_value_source",
    )
    if data_upload:
        try:
            raw_data = data_upload.getvalue()
            initial_data_json = json.loads(decode_text_bytes(raw_data))
            if not isinstance(initial_data_json, dict) or not (initial_data_json.get("structId") or is_keyed_export_json(initial_data_json)):
                raise ValueError("数据 JSON 必须是 P2Gia 同格式对象，或包含 key 字段的导出变量 JSON。")
            initial_data_token = hashlib.sha1(raw_data).hexdigest()[:12]
            identity = initial_data_json.get("structId") or initial_data_json.get("name") or "unknown"
            st.success(f"已读取初始数据：{identity}")
        except Exception as exc:
            st.error(f"数据结构 JSON 解析失败：{exc}")
            initial_data_json = None
            initial_data_token = "invalid"

    struct_names = [
        str(item.get("name") or item.get("id"))
        for item in structs_doc.get("structs", [])
        if item.get("name") or item.get("id")
    ]
    default_struct_index = 0
    if initial_data_json:
        initial_struct_id = str(initial_data_json.get("structId") or "")
        initial_struct_name = str(initial_data_json.get("name") or "")
        for index, item in enumerate(structs_doc.get("structs", [])):
            if str(item.get("id")) == initial_struct_id or str(item.get("name")) == initial_struct_name:
                default_struct_index = index
                break
    selected_struct = st.selectbox(
        "选择要编辑的结构体",
        struct_names,
        index=min(default_struct_index, max(len(struct_names) - 1, 0)),
        key=f"visual_struct_name_{initial_data_token}",
    )
    selected_struct_doc = find_struct_doc(structs_doc, selected_struct)
    if not selected_struct_doc:
        st.error("未找到选中的结构体。")
        return

    if initial_data_json:
        try:
            initial_data_json = normalize_export_data_json(initial_data_json, structs_doc, selected_struct_doc)
        except Exception as exc:
            st.error(f"导出变量 JSON 无法用于当前结构体：{exc}")
            return

    order_problems = collect_unverified_order_structs(selected_struct_doc, structs_doc, initial_data_json)
    if order_problems:
        if initial_data_json is None:
            st.warning("当前 GIA 没有提取到完整可信的变量实际顺序，不能直接编辑或导出。")
            st.info("请在上方上传“导出变量”得到的数据结构 JSON，用它逐位校验字段顺序。校验不通过时不会自动重排。")
        else:
            st.error("导出变量 JSON 不能证明当前字段顺序正确，已停止编辑，避免错位写入。")
        for problem in order_problems[:8]:
            st.write(f"- {problem}")
        if len(order_problems) > 8:
            st.write(f"- 还有 {len(order_problems) - 8} 个顺序问题未显示。")
        return
    if initial_data_json is not None and structs_doc.get("source_format") == "gia":
        st.success("字段顺序已通过导出变量 JSON 逐位校验。")

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
    try:
        initial_value = (
            data_json_to_struct_value(selected_struct_doc, structs_doc, initial_data_json)
            if initial_data_json and str(initial_data_json.get("structId")) == str(selected_struct_doc.get("id"))
            else {}
        )
    except Exception as exc:
        st.error(f"初始数据 JSON 与当前结构体顺序不一致：{exc}")
        return
    value = render_struct_value_editor(
        selected_struct_doc,
        structs_doc,
        f"visual_struct_editor_{selected_struct_doc.get('id')}_{initial_data_token}",
        initial_value=initial_value,
    )
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
    story_input_mode = st.radio(
        "story.txt 输入方式",
        ["上传文件", "直接输入"],
        horizontal=True,
        key="story_gil_export_input_mode",
    )
    with st.form("story_to_gil"):
        input_gil_upload = st.file_uploader("关卡 .gil", type=["gil"], key="story_gil_export_gil")
        story_upload = None
        story_text_input = ""
        if story_input_mode == "上传文件":
            story_upload = st.file_uploader("story_board 导出的 story.txt", type=["txt"], key="story_gil_export_txt")
        else:
            story_text_input = st.text_area(
                "story.txt 内容",
                value="",
                height=260,
                placeholder="每行格式：status|文本1;文本2|next1;next2",
                key="story_gil_export_text_input",
            )
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
        if not input_gil_upload:
            st.error("需要上传关卡 .gil。")
            return
        if story_input_mode == "上传文件":
            if not story_upload:
                st.error("需要上传 story.txt。")
                return
            story_text = read_text_upload(story_upload)
        else:
            story_text = story_text_input.strip()
            if not story_text:
                st.error("需要输入 story.txt 内容。")
                return
        if not any(line.strip() for line in story_text.splitlines()):
            st.error("story.txt 内容不能为空。")
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
                    story_text,
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


def render_tool_page_header(page: str) -> None:
    descriptions = {
        "导入变量": "从结构体定义生成可导入的结构体数据 JSON。",
        "导出元件": "把剧情文本、结构体和 components JSON 写入地图 GIL。",
        "镜头 GIA 生成": "生成滑动变焦镜头组 GIA。",
    }
    st.markdown(
        f"""
        <div class="qx-page-hero">
          <div class="qx-page-kicker">Miliastra Wonderland Tooling</div>
          <div class="qx-page-title">{page}</div>
          <div class="qx-shell-title">{descriptions.get(page, "千星工具箱")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title="千星工具箱", layout="wide")

    st.sidebar.title("千星工具箱")
    st.sidebar.caption("GIL / GIA workflow")
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
        st.markdown(APP_PAGE_CSS, unsafe_allow_html=True)
        render_tool_page_header(page)
        page_import_variables()
    elif page == "导出元件":
        st.markdown(APP_PAGE_CSS, unsafe_allow_html=True)
        render_tool_page_header(page)
        page_export_component()
    elif page == "镜头 GIA 生成":
        st.markdown(APP_PAGE_CSS, unsafe_allow_html=True)
        render_tool_page_header(page)
        page_camera_generator()


if __name__ == "__main__":
    main()
