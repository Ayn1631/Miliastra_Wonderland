# GIA Component Import Scripts

本目录存放元件变量导入和多章节合并脚本。

| 文件 | 作用 |
| --- | --- |
| `import_component_variables.py` | 将一个章节目录中的 `report_*.json` 导入到单个元件 `.gia`。 |
| `build_multi_chapter_gia.py` | 以模板 `.gia` 为格式基准，按章节目录生成“一个章节一个元件”的合并 `.gia`。 |
| `README.md` | 当前导入脚本目录说明。 |

依赖：

| 路径 | 作用 |
| --- | --- |
| `scripts/gia_component_variables/parse_component_variables.py` | 提供 Protobuf 解析、变量定位和 CSV 输出能力。 |

示例：

```powershell
python .\scripts\gia_component_import\build_multi_chapter_gia.py `
  --template .\scripts\resources\gia_templates\1and2.gia `
  --chapters .\scripts\resources\story_reports\lutasiyi_chapters `
  --output .\scripts\resources\gia_outputs\路塔斯忆_五章合并_1and2格式.gia `
  --summary .\scripts\resources\gia_outputs\路塔斯忆_五章合并_1and2格式.summary.json
```
