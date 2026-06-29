# GIA Camera Scripts

本目录存放镜头类 `.gia` 文件相关脚本。

| 文件 | 作用 |
| --- | --- |
| `parse_gia.py` | 解析已知镜头类 `.gia` 容器、header/footer、Protobuf 字段和镜头参数摘要。 |
| `generate_zoom_gia.py` | 根据步数、距离范围和视场角范围生成滑动变焦镜头组 `.gia`。 |
| `README.md` | 当前镜头脚本目录说明。 |

示例：

```powershell
python .\scripts\gia_camera\parse_gia.py .\镜头.gia
python .\scripts\gia_camera\generate_zoom_gia.py --output .\滑动变焦_16.gia
```
