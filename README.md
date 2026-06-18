# Dust Front RTS Demo 汉化工具

对编译好的 Unity IL2CPP 游戏 **Dust Front RTS Demo** 进行中文本地化。

## 安装

将本仓库克隆到游戏根目录：

```bash
cd "你的Steam库路径/steamapps/common/Dust Front RTS Demo"
git clone https://github.com/zgh2000/dust-front-rts-chinese.git
cd dust-front-rts-chinese
uv sync
```

目录结构：
```
Dust Front RTS Demo/
├── Dust Front RTS_Data/    ← 游戏数据
├── dust-front-rts-chinese/  ← 本仓库
│   ├── run.py
│   ├── translate.py
│   └── ...
└── Dust Front RTS.exe
```

## 使用方法

```bash
uv run python run.py patch    # 生成补丁
uv run python run.py apply    # 应用补丁（关闭游戏后执行）
uv run python run.py restore  # 恢复原版
uv run python run.py status   # 查看文件状态
```

应用补丁后启动游戏，在语言下拉菜单中选择 **Chinese** 即可。

## 翻译范围

共翻译 **679 条**文本，覆盖：

- **系统 UI**：主菜单、设置、按钮
- **资源系统**：材料、补给、零件、能量
- **单位**：叛军和变种人全部单位名称和描述
- **建筑**：全部建筑名称和描述
- **武器数据**：火力、装甲、速度等属性
- **任务系统**：任务目标、天气事件、增援
- **战斗统计**：结算画面所有统计项
- **学说/升级**：全部学说和升级项
- **能力/支援**：战术能力和支援技能
- **操作说明**：控制键位和提示
- **教程文本**：界面教程、基础教程、高级教程

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
