# Dust Front RTS Demo 汉化工具

对编译好的 Unity IL2CPP 游戏 **Dust Front RTS Demo** 进行中文本地化。

## 使用方法

```bash
cd localization-tool
uv sync

# 生成补丁
uv run python run.py patch

# 应用补丁（关闭游戏后执行）
uv run python run.py apply

# 恢复原版
uv run python run.py restore

# 查看文件状态
uv run python run.py status
```

应用补丁后启动游戏，在语言下拉菜单中选择 **Chinese** 即可。

## 文件说明

| 文件 | 说明 |
|------|------|
| `run.py` | 主入口：patch / apply / restore / status |
| `translate.py` | 翻译数据：679 条中英文对照 |

## 工作原理

游戏的 `Localizator` 类从 CSV header 动态读取语言名。在原始 `Keys,Russian,English` 格式中添加 `Chinese` 列，游戏自动识别并允许选择。

## 注意事项

- 游戏更新后重新运行 `uv run python run.py patch && uv run python run.py apply`
- 修改翻译：编辑 `translate.py` 中的 `TRANSLATIONS` 字典
- 保留 `resources.assets.bak` 以便恢复
