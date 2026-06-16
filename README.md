# Dust Front RTS Demo 汉化工具

对编译好的 Unity IL2CPP 游戏 **Dust Front RTS Demo** 进行中文本地化。

## 功能

- 提取游戏本地化 CSV 文件（616 条主文本 + 63 条教程/演示文本）
- 在 CSV 中添加 Chinese 列（保留原有俄语和英语）
- 生成汉化补丁文件（`resources.assets.patched`）
- 自动备份原始文件（`resources.assets.bak`）

## 使用方法

### 1. 安装依赖

```bash
cd localization-tool
uv sync
```

### 2. 生成汉化补丁

```bash
uv run python patch_assets.py
```

### 3. 应用补丁

```powershell
# 关闭游戏后执行
Remove-Item "Dust Front RTS_Data\resources.assets"
Rename-Item "Dust Front RTS_Data\resources.assets.patched" "resources.assets"
```

启动游戏，在语言下拉菜单中选择 **Chinese** 即可。

### 4. 恢复原版

```powershell
Remove-Item "Dust Front RTS_Data\resources.assets"
Rename-Item "Dust Front RTS_Data\resources.assets.bak" "resources.assets"
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `patch_assets.py` | 主补丁脚本：在 path_id=163 的 TextAsset 中添加 Chinese 列 |
| `translate.py` | 翻译数据：679 条中英文对照 |
| `output/textasset_163.csv` | 原始主本地化 CSV |
| `output/textasset_164_cn.csv` | 带 Chinese 列的主本地化 CSV |
| `output/textasset_165_cn.csv` | 带 Chinese 列的教程/演示 CSV |

## 工作原理

游戏的本地化系统（`Localizator` 类）工作方式：

1. 从 `resources.assets` 加载所有 TextAsset CSV
2. CSV 格式：`Keys,Russian,English[,Chinese]`
3. 从 header 行读取语言名，构建 `Dictionary[语言名][key] = 翻译文本`
4. 用户在设置中选择语言后，通过 `currentLanguage` 查找对应翻译

汉化方案：在原始 CSV 中添加 Chinese 列，游戏会自动识别并允许选择。

## 注意事项

- 游戏更新后需重新运行 `patch_assets.py` 并替换 `resources.assets`
- 修改翻译：编辑 `translate.py` 中的 `TRANSLATIONS` 字典，重新运行 `patch_assets.py`
- 保留 `resources.assets.bak` 以便随时恢复原版
