# Scripts Resources

本目录存放 `scripts/` 内脚本的默认输入、模板和输出位置。脚本内置默认路径必须指向本目录或 `scripts/` 内其他目录，避免依赖 `scripts/` 外部文件。

| 路径 | 作用 |
| --- | --- |
| `gil_templates/` | `.gil/.gia` 模板文件，例如 `Template.gil`、`Template.gia`。 |
| `gil_inputs/` | GIL 工作流默认输入和结构体 JSON，例如 `塔露斯伊.gil`、`塔露斯伊.structs.json`。 |
| `gil_outputs/` | GIL 工作流默认输出目录。 |
| `gia_templates/` | GIA 合并/导入示例模板。 |
| `gia_outputs/` | GIA 合并/导入示例输出目录。 |
| `story_sources/` | `P2Gia.py` 等脚本使用的源剧情文本。 |
| `story_reports/` | 由剧情文本拆分出的 `report_*.json` 章节数据。 |
