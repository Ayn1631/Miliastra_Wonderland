# GIA Component Variable Scripts

本目录存放元件变量解析脚本。

| 文件 | 作用 |
| --- | --- |
| `parse_component_variables.py` | 解析元件变量摘要，输出变量名、类型、Story 引用、StoryNode 内容等。 |
| `dump_gia_full.py` | 导出完整 Protobuf 树，保留未知字段和 `raw_hex`，用于逆向分析不支持的字段。 |
| `analyze_template_variables.py` | 通用提取 `Template.gia` 变量类型映射、值字段和字典 key/value 类型。 |
| `README.md` | 当前变量解析脚本目录说明。 |

示例：

```powershell
python .\scripts\gia_component_variables\parse_component_variables.py .\scripts\resources\gia_templates\1and2.gia --component 第一章 --json .\scripts\resources\gia_outputs\1and2.第一章.variables.json
python .\scripts\gia_component_variables\dump_gia_full.py .\scripts\resources\gia_templates\1and2.gia --output .\scripts\resources\gia_outputs\1and2.full.json
```
