# components JSON 编写指南

本文档说明 `components.example.json` 的完整写法。目标是：任何人拿到一个地图 `.gil` 和导出的结构体 JSON 后，都能写出用于创建元件和局部变量的 JSON。

## 最小使用流程

写一个 `components.json`，最后生成新存档：

```powershell
python .\scripts\gil_workflow\build_gil_components.py `
  .\scripts\resources\gil_inputs\塔露斯伊.gil `
  .\scripts\gil_workflow\components.example.json `
  .\scripts\resources\gil_outputs\塔露斯伊_自定义元件.gil `
  --overwrite
```

## JSON 顶层格式

推荐写法是一个对象，包含 `components` 数组：

```json
{
  "components": [
    {
      "name": "DemoComponent",
      "variables": []
    }
  ]
}
```

也可以直接写组件数组：

```json
[
  {
    "name": "DemoComponent",
    "variables": []
  }
]
```

推荐使用对象写法，因为以后可以在顶层追加 `id_policy`。

## 顶层字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `components` | array | 是 | 要创建的元件列表。每个数组项创建一个元件。 |
| `id_policy` | object | 否 | id 分配起点。一般不用写，脚本默认会给安全区间。 |

### `id_policy`

只有你明确知道当前地图 id 区间时才需要写。

```json
{
  "id_policy": {
    "component_definition_start": 1077940000,
    "component_index_start": 1077950000,
    "value_ref_start": 1075000000
  },
  "components": []
}
```

| 字段 | 说明 |
| --- | --- |
| `component_definition_start` | 新元件定义 id 起点，写入 `root.f4`。 |
| `component_index_start` | 新元件索引/缓存 id 起点，写入 `root.f8`。 |
| `value_ref_start` | 结构体值、复杂值内部对象引用 id 起点。 |

脚本会扫描输入 `.gil` 里已有整数 id，并避开已使用 id。

## 元件对象格式

```json
{
  "name": "DemoComponent",
  "variables": [
    {
      "name": "title",
      "type": "str",
      "value": "文本"
    }
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `name` | string | 是 | 元件名称。会写入 `root.f4` 和 `root.f8`。 |
| `variables` | array | 是 | 元件局部变量列表。顺序会按数组顺序写入。 |

变量名可以是中文、英文、数字字符串，例如 `"小节"`、`"title"`、`"1"`。

## 变量对象通用格式

```json
{
  "name": "变量名",
  "type": "str",
  "value": "变量值"
}
```

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `name` | string | 是 | 变量名。 |
| `type` | string | 通常必填 | 类型名，例如 `str`、`int`、`struct`。 |
| `type_code` | number | 否 | 类型码。一般用 `type` 即可；当类型名不方便表达时可直接写 type_code。 |
| `value` | any | 否 | 变量值。不同类型写法不同。 |

`type` 和 `type_code` 二选一即可。推荐使用 `type`，可读性更好。

## 支持的 type

| type | type_code | value 写法 | 当前支持状态 |
| --- | ---: | --- | --- |
| `str` | `6` | string | 支持 |
| `str_list` | `11` | string array | 支持 |
| `int` | `3` | integer | 支持 |
| `int_list` | `8` | integer array | 支持 |
| `float` | `5` | number | 支持 |
| `float_list` | `10` | number array | 支持 |
| `bool` | `4` | boolean | 支持 |
| `bool_list` | `9` | boolean array | 支持 |
| `camp` | `17` | integer | 支持 |
| `camp_list` | `24` | integer array | 支持 |
| `struct` | `25` | object | 支持 |
| `struct_list` | `26` | object array | 支持 |
| `dict` | `27` | `entries` array | 实验性支持 |
| `object` | `1` | `null` | 仅默认/空值稳妥 |
| `GUID` | `2` | `""` | 仅默认/空值稳妥 |
| `GUID_list` | `7` | `[]` | 仅默认/空值稳妥 |
| `vector` | `12` | `{}` | 仅默认/空值稳妥 |
| `vector_list` | `15` | `[]` | 仅默认/空值稳妥 |
| `configurationID` | `20` | `null` | 仅默认/空值稳妥 |
| `configurationID_list` | `22` | `[]` | 仅默认/空值稳妥 |
| `componentID` | `21` | `null` | 仅默认/空值稳妥 |
| `componentID_list` | `23` | `[]` | 仅默认/空值稳妥 |

说明：`object/vector/GUID/configurationID/componentID` 的非默认值语义尚未完全确认。你可以创建这些变量，但非空值可能被脚本保留为模板默认值，并在 summary 里产生 warning。

## 基础类型示例

### 字符串

```json
{
  "name": "title",
  "type": "str",
  "value": "示例元件"
}
```

### 字符串列表

```json
{
  "name": "小节",
  "type": "str_list",
  "value": ["1", "2", "3"]
}
```

### 整数

```json
{
  "name": "count",
  "type": "int",
  "value": 3
}
```

### 整数列表

```json
{
  "name": "next",
  "type": "int_list",
  "value": [10001, 10002]
}
```

### 浮点数

```json
{
  "name": "speed",
  "type": "float",
  "value": 1.5
}
```

### 浮点数列表

```json
{
  "name": "weights",
  "type": "float_list",
  "value": [0.25, 0.5, 1.0]
}
```

### 布尔值

```json
{
  "name": "enabled",
  "type": "bool",
  "value": true
}
```

### 布尔列表

```json
{
  "name": "flags",
  "type": "bool_list",
  "value": [true, false, true]
}
```

## 结构体变量

结构体变量使用 `type: "struct"`，并通过 `struct` 指定结构体名称。

```json
{
  "name": "story",
  "type": "struct",
  "struct": "Story",
  "value": {
    "Story_List": []
  }
}
```

`struct` 的值来自结构体导出 JSON 的 `structs_by_name`。例如 `塔露斯伊.structs.json` 里有：

```json
{
  "structs_by_name": {
    "StoryNode": 1077936129,
    "Story": 1077936130
  }
}
```

那么就可以写：

```json
{
  "type": "struct",
  "struct": "Story"
}
```

也可以直接写结构体 id：

```json
{
  "name": "story",
  "type": "struct",
  "struct_id": 1077936130,
  "value": {
    "Story_List": []
  }
}
```

推荐使用结构体名称，JSON 更容易读。

## 按结构体字段填 value

结构体的 `value` 是一个对象，字段名必须对应导出的结构体字段名。

例如导出的 `StoryNode` 是：

```json
{
  "name": "StoryNode",
  "fields": [
    {"name": "status", "type": "str"},
    {"name": "str", "type": "str_list"},
    {"name": "next", "type": "int_list"}
  ]
}
```

那么一个 `StoryNode` 的值应写为：

```json
{
  "status": "6",
  "str": ["一句文本"],
  "next": [3]
}
```

字段缺失时，脚本会按该类型的默认值写入。

## 结构体列表

结构体列表使用 `type: "struct_list"`，`value` 是对象数组。

```json
{
  "name": "nodes",
  "type": "struct_list",
  "struct": "StoryNode",
  "value": [
    {
      "status": "6",
      "str": ["第一句"],
      "next": [2]
    },
    {
      "status": "6",
      "str": ["第二句"],
      "next": [3]
    }
  ]
}
```

## 嵌套结构体：`__struct_types__`

有些结构体字段本身是 `struct_list`，只看字段 type_code 无法知道列表元素是哪种结构体。此时需要在父结构体的 `value` 中写 `__struct_types__`。

以 `Story` 为例：

```json
{
  "id": 1077936130,
  "name": "Story",
  "fields": [
    {
      "name": "Story_List",
      "type": "struct_list"
    }
  ]
}
```

`Story_List` 的元素实际是 `StoryNode`，所以要这样写：

```json
{
  "name": "1",
  "type": "struct",
  "struct": "Story",
  "value": {
    "__struct_types__": {
      "Story_List": "StoryNode"
    },
    "Story_List": [
      {
        "status": "6",
        "str": ["第一句文本"],
        "next": [2]
      },
      {
        "status": "6",
        "str": ["第二句文本"],
        "next": [3]
      }
    ]
  }
}
```

`__struct_types__` 不会成为游戏变量字段，它只是生成器用来判断嵌套结构体类型的提示。

## 字典变量

字典使用 `type: "dict"`。必须指定 key 和 value 的类型。

```json
{
  "name": "settings",
  "type": "dict",
  "key_type": "str",
  "value_type": "int",
  "entries": [
    {"key": "hp", "value": 100},
    {"key": "mp", "value": 50}
  ]
}
```

字段说明：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `key_type` | string | 是 | key 类型，例如 `str`、`int`。 |
| `value_type` | string | 是 | value 类型，例如 `int`、`str`、`float`。 |
| `entries` | array | 是 | 字典条目。 |
| `entries[].key` | any | 是 | key 值。 |
| `entries[].value` | any | 是 | value 值。 |

当前字典编码仍是实验性功能。生成后必须在编辑器里打开验证。

## 完整示例：普通元件

```json
{
  "components": [
    {
      "name": "DemoComponent",
      "variables": [
        {
          "name": "title",
          "type": "str",
          "value": "示例元件"
        },
        {
          "name": "sections",
          "type": "str_list",
          "value": ["1", "2", "3"]
        },
        {
          "name": "count",
          "type": "int",
          "value": 3
        },
        {
          "name": "enabled",
          "type": "bool",
          "value": true
        }
      ]
    }
  ]
}
```

## 完整示例：章节 Story 元件

```json
{
  "components": [
    {
      "name": "01_unknown_call",
      "variables": [
        {
          "name": "小节",
          "type": "str_list",
          "value": ["1", "2"]
        },
        {
          "name": "1",
          "type": "struct",
          "struct": "Story",
          "value": {
            "__struct_types__": {
              "Story_List": "StoryNode"
            },
            "Story_List": [
              {
                "status": "6",
                "str": ["【第一章：风中的未知来电】"],
                "next": [2]
              },
              {
                "status": "6",
                "str": ["风花节前夕的深夜。"],
                "next": [3]
              }
            ]
          }
        },
        {
          "name": "2",
          "type": "struct",
          "struct": "Story",
          "value": {
            "__struct_types__": {
              "Story_List": "StoryNode"
            },
            "Story_List": [
              {
                "status": "6",
                "str": ["第二小节第一句。"],
                "next": [2]
              }
            ]
          }
        }
      ]
    }
  ]
}
```

这个示例表达：

1. 创建一个元件 `01_unknown_call`。
2. 创建局部变量 `小节`，内容是 `["1", "2"]`。
3. 创建两个结构体变量，变量名分别为 `"1"` 和 `"2"`。
4. 每个结构体变量都是 `Story`。
5. `Story.Story_List` 是 `StoryNode` 列表。

## 常见错误

| 错误 | 原因 | 正确做法 |
| --- | --- | --- |
| `struct not found` | `struct` 名称不在导出的 `structs_by_name` 里。 | 先运行 `export_gil_structs.py`，按导出的结构体名填写。 |
| 结构体字段没生效 | `value` 里的字段名和结构体字段名不一致。 | 严格使用 `structs[].fields[].name`。 |
| `struct_list` 生成为空 | 没有告诉脚本列表元素是哪种结构体。 | 在父结构体 `value` 里加入 `__struct_types__`。 |
| 输出文件已存在 | 没有加 `--overwrite`。 | 重新运行时加 `--overwrite`，或换一个输出文件名。 |
| 编辑器打开后变量缺失 | 只改了手写 JSON，没有重新生成 `.gil`。 | 每次改 JSON 后都重新运行 `build_gil_components.py`。 |

### 例：`struct not found in extracted structs: test`

这个错误表示你的 JSON 写了：

```json
{
  "type": "struct",
  "struct": "test"
}
```

但当前输入 `.gil` 导出的结构体里没有名为 `test` 的结构体。

解决方法：

1. 运行 `export_gil_structs.py` 导出结构体。
2. 打开 `.structs.json`。
3. 查看 `structs_by_name` 里有哪些名称。
4. 把 `"struct"` 改成真实存在的名称。

例如 `塔露斯伊.gil` 里有：

```json
{
  "structs_by_name": {
    "StoryNode": 1077936129,
    "Story": 1077936130
  }
}
```

所以应该写：

```json
{
  "type": "struct",
  "struct": "Story"
}
```

## 生成后会得到哪些文件

执行：

```powershell
python .\scripts\gil_workflow\build_gil_components.py `
  .\地图.gil `
  .\components.json `
  .\地图_自定义元件.gil `
  --overwrite
```

会生成：

| 文件 | 说明 |
| --- | --- |
| `地图_自定义元件.gil` | 处理后的存档。 |
| `地图_自定义元件.summary.json` | 生成摘要，包含新增元件、变量、warning。 |
| `地图_自定义元件.structs.json` | 从输入地图导出的结构体结构。 |
| `地图_自定义元件.workflow.json` | 内部 workflow 规格，便于排查问题。 |

## 编写建议

1. 先用 `export_gil_structs.py` 导出结构体。
2. 复制结构体字段名，不要手打猜测。
3. 先生成一个元件、一个变量验证能打开，再批量生成。
4. `小节` 这类索引变量要和后续变量名顺序保持一致，例如 `["1", "2"]` 对应变量 `"1"`、`"2"`。
5. 复杂结构体列表一定写 `__struct_types__`。
