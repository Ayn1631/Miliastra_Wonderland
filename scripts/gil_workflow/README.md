# GIL 工作流脚本

本目录把当前 `.gil` 逆向结果整理为一个可执行工作流：

1. 从一个地图/工程 `.gil` 中提取已有结构体。
2. 按 JSON 规格创建多个新元件。
3. 为每个新元件写入自定义变量。
4. 默认只追加 `root.f4` 元件定义和 `root.f8` 元件索引/缓存，不修改 `root.f5` 场景实体和 `root.f10` 结构体/节点定义。

## 文件

| 文件 | 作用 |
| --- | --- |
| `gil_common.py` | `.gil` 容器、Protobuf 读写、id 扫描、模板定位和基础编码工具。 |
| `export_gil_structs.py` | 通用入口：传入存档 `.gil`，导出所有结构体结构 JSON。 |
| `extract_structs.py` | 从 `root.f10` 提取结构体 schema，输出结构体名称、id 和字段列表。 |
| `build_gil_components.py` | 通用入口：传入地图 `.gil`、元件变量 JSON，输出处理后的 `.gil`。 |
| `build_chapter_components_spec.py` | 把章节目录下的 `report_*.json` 转成“每章一个元件、每小节一个 Story 变量”的工作流规格。 |
| `build_lutasiyi_chapters_gil.py` | 塔露斯伊专用零参数脚本，一次性生成章节元件版 `.gil`。 |
| `create_components.py` | 按规格追加新元件，并根据 `Template.gil` 的变量模板生成变量。 |
| `run_workflow.py` | 串联入口：先提取结构体，再创建元件。 |
| `components.example.json` | 通用元件变量 JSON 示例。 |
| `components.story.example.json` | 依赖 `Story/StoryNode` 结构体的剧情变量示例，适用于塔露斯伊这类地图。 |
| `COMPONENTS_JSON_GUIDE.md` | `components.example.json` 的详细编写指南，包含所有字段、类型和完整示例。 |
| `example.workflow.json` | 示例规格文件。 |

## 使用方式

### 通用：导出结构体 JSON

```powershell
python .\scripts\gil_workflow\export_gil_structs.py `
  .\scripts\resources\gil_inputs\塔露斯伊.gil `
  .\scripts\resources\gil_inputs\塔露斯伊.structs.json
```

输出 JSON 包含：

| 字段 | 说明 |
| --- | --- |
| `structs[]` | 结构体列表。 |
| `structs[].id` | 结构体 id。 |
| `structs[].name` | 结构体名称。 |
| `structs[].fields[]` | 字段列表，包含字段名、类型名和 type_code。 |
| `structs_by_name` | 名称到 id 的映射，便于生成变量时用 `"struct": "Story"` 引用。 |
| `structs_by_id` | id 到完整结构体定义的映射。 |

### 通用：按 JSON 创建元件和局部变量

详细 JSON 写法见 [COMPONENTS_JSON_GUIDE.md](COMPONENTS_JSON_GUIDE.md)。

```powershell
python .\scripts\gil_workflow\build_gil_components.py `
  .\scripts\resources\gil_inputs\塔露斯伊.gil `
  .\scripts\gil_workflow\components.example.json `
  .\scripts\resources\gil_outputs\塔露斯伊_自定义元件.gil `
  --overwrite
```

如果要生成 `Story` 结构体变量，使用：

```powershell
python .\scripts\gil_workflow\build_gil_components.py `
  .\scripts\resources\gil_inputs\塔露斯伊.gil `
  .\scripts\gil_workflow\components.story.example.json `
  .\scripts\resources\gil_outputs\塔露斯伊_Story示例.gil `
  --overwrite
```

注意：结构体变量的 `"struct"` 必须是当前输入 `.gil` 里真实存在的结构体名称。比如 `塔露斯伊.gil` 有 `Story`、`StoryNode`，但没有 `test`。

这个入口会自动：

1. 从输入 `.gil` 导出结构体 JSON。
2. 将 `components.example.json` 转换为内部 workflow spec。
3. 基于 `Template.gil` 里的变量模板创建元件变量。
4. 输出处理后的 `.gil`、`.summary.json`、`.structs.json` 和 `.workflow.json`。

元件变量 JSON 可以是：

```json
{
  "components": [
    {
      "name": "DemoComponent",
      "variables": [
        {"name": "title", "type": "str", "value": "文本"},
        {"name": "count", "type": "int", "value": 1},
        {
          "name": "profile",
          "type": "struct",
          "struct": "Story",
          "value": {
            "Story_List": []
          }
        }
      ]
    }
  ]
}
```

也可以直接传组件数组：

```json
[
  {
    "name": "DemoComponent",
    "variables": [
      {"name": "title", "type": "str", "value": "文本"}
    ]
  }
]
```

### 旧 workflow 入口

先复制一份规格 JSON，把 `input_gil` 改成你的地图文件：

```powershell
Copy-Item .\scripts\gil_workflow\example.workflow.json .\my_map.workflow.json
```

然后运行完整工作流：

```powershell
python .\scripts\gil_workflow\run_workflow.py .\my_map.workflow.json
```

也可以分步运行。

塔露斯伊章节元件专用脚本：

```powershell
python .\scripts\gil_workflow\build_lutasiyi_chapters_gil.py
```

该脚本不需要参数，固定读取：

| 项 | 路径 |
| --- | --- |
| 输入 GIL | `scripts/resources/gil_inputs/塔露斯伊.gil` |
| 变量模板 | `scripts/resources/gil_templates/Template.gil` |
| 章节目录 | `scripts/resources/story_reports/lutasiyi_chapters` |
| 输出 GIL | `scripts/resources/gil_outputs/塔露斯伊_章节元件.gil` |

提取结构体：

```powershell
python .\scripts\gil_workflow\extract_structs.py `
  .\地图.gil `
  --output .\地图.structs.json
```

生成元件：

```powershell
python .\scripts\gil_workflow\create_components.py .\my_map.workflow.json
```

章节 report 批量生成规格：

```powershell
python .\scripts\gil_workflow\build_chapter_components_spec.py `
  --chapters-root .\scripts\resources\story_reports\lutasiyi_chapters `
  --input-gil .\scripts\resources\gil_inputs\塔露斯伊.gil `
  --template-gil .\scripts\resources\gil_templates\Template.gil `
  --structs-json .\scripts\resources\gil_inputs\塔露斯伊.structs.json `
  --output-gil .\scripts\resources\gil_outputs\塔露斯伊_章节元件.gil `
  --spec-output .\scripts\resources\gil_outputs\塔露斯伊_chapters.workflow.json `
  --overwrite
```

## 规格字段

| 字段 | 说明 |
| --- | --- |
| `input_gil` | 输入地图/工程 `.gil`。 |
| `template_gil` | 变量模板供体，默认建议使用 `scripts/resources/gil_templates/Template.gil`。 |
| `template_component` | 模板元件名，当前为 `Template`。 |
| `structs_json` | 结构体提取结果；`run_workflow.py` 会自动生成。 |
| `output_gil` | 输出 `.gil`。 |
| `overwrite` | 是否覆盖已有输出文件。 |
| `components[]` | 要创建的新元件列表。 |
| `components[].variables[]` | 单个元件的变量列表。 |

变量示例：

```json
{
  "name": "title",
  "type": "str",
  "value": "文本"
}
```

结构体变量示例：

```json
{
  "name": "profile",
  "type": "struct",
  "struct": "test",
  "value": {
    "str": "结构体字段值",
    "int": 1,
    "bool": true
  }
}
```

字典变量示例：

```json
{
  "name": "settings",
  "type": "dict",
  "key_type": "str",
  "value_type": "int",
  "entries": [
    {"key": "hp", "value": 100}
  ]
}
```

## 当前边界

| 类型/能力 | 当前状态 |
| --- | --- |
| `str/int/float/bool` | 支持自定义值。 |
| `str_list/int_list/float_list/bool_list/camp_list` | 支持自定义列表。 |
| `struct` | 支持引用已提取结构体，并按字段名写值。 |
| `struct_list` | 支持基础列表编码，建议先小样本验证。 |
| `dict` | 已实现实验性编码，必须在编辑器里验证。 |
| `object/vector/GUID/configurationID/componentID` 非默认值 | 语义尚未完全确认，脚本会保留模板默认值并输出 warning。 |
| 新建独立结构体 | 暂未默认启用；要生成新结构体时需要扩展 `root.f10`。 |
| 场景实体实例 | 暂不生成；默认不改 `root.f5`。 |
