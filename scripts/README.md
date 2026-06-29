# Scripts

本目录集中存放可执行脚本，按用途拆分为子目录。

| 路径 | 作用 |
| --- | --- |
| `gia_camera/` | 镜头类 `.gia` 文件的解析与滑动变焦预设生成。 |
| `gia_component_variables/` | 元件变量类 `.gia` 文件的变量摘要解析与完整 Protobuf 树导出。 |
| `gia_component_import/` | 把章节 JSON 导入元件变量，并基于模板合并生成多章节 `.gia`。 |
| `gil_generation/` | `.gil` 工程存档生成脚本。 |
| `gil_workflow/` | 从地图 `.gil` 提取结构体，并按规格创建多个新元件和变量的工作流脚本。 |
| `resources/` | 脚本默认使用的模板、输入、输出和剧情数据资源。 |
| `Story/` | 故事制作工具集 |
| `streamlit_app.py` | 简约 Streamlit 前端，整合剧情编排、元件导出、镜头 GIA 生成等功能。 |
| `README.md` | 当前脚本总目录说明。 |
