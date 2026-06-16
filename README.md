# Dust Front RTS Demo 汉化工具

对编译好的 Unity IL2CPP 游戏 **Dust Front RTS Demo** 进行中文本地化。

## 功能

- 提取游戏本地化 CSV 文件（616+ 条主文本 + 63 条教程/演示文本）
- 将英文替换为中文翻译
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

1. 关闭游戏
2. 将 `resources.assets` 重命名为 `resources.assets.orig`
3. 将 `resources.assets.patched` 重命名为 `resources.assets`
4. 启动游戏，选择 **English** 语言即可看到中文

### 4. 恢复原版

1. 删除 `resources.assets`
2. 将 `resources.assets.bak` 重命名为 `resources.assets`

## 文件说明

| 文件 | 说明 |
|------|------|
| `patch_assets.py` | 主补丁脚本：读取翻译CSV，写回资产文件 |
| `translate.py` | 翻译数据：包含所有中英文对照 |
| `output/textasset_164_cn.csv` | 主本地化翻译后的CSV |
| `output/textasset_165_cn.csv` | 教程/演示翻译后的CSV |
| `output/textasset_164.csv` | 原始主本地化CSV |
| `output/textasset_165.csv` | 原始教程/演示CSV |

## 工作原理

游戏的本地化系统（`Localizator` 类）通过以下方式工作：

1. 从 `resources.assets` 加载 TextAsset CSV 文件
2. CSV 格式：`Keys,Russian,English`
3. 根据 `currentLanguage` 设置（`RUSSIAN` 或 `ENGLISH`）选择对应列
4. 通过 `Dictionary[语言名][key]` 查找翻译

汉化方案：将 English 列替换为中文，用户在游戏中选择 English 即可显示中文。

## 注意事项

- 游戏更新后可能需要重新应用补丁
- 建议保留 `resources.assets.bak` 以便恢复
- 如需修改翻译，编辑 `translate.py` 中的 `TRANSLATIONS` 字典，然后重新运行 `patch_assets.py`
