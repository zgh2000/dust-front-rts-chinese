# Dust Front RTS Demo 汉化工具

对编译好的 Unity IL2CPP 游戏 **Dust Front RTS Demo** 进行中文本地化。

## 使用方法

```bash
cd dust-front-rts-chinese
uv sync

uv run python run.py patch    # 生成补丁
uv run python run.py apply    # 应用补丁（关闭游戏后执行）
uv run python run.py restore  # 恢复原版
uv run python run.py status   # 查看文件状态
```

应用补丁后启动游戏，在语言下拉菜单中选择 **Chinese** 即可。

## 翻译范围

共翻译 **679 条**文本，覆盖以下内容：

### 主本地化（path_id=163，616 条）

| 分类 | 内容 | 示例 |
|------|------|------|
| 系统 UI | 主菜单、设置、按钮 | 开始、退出、设置、返回 |
| 资源系统 | 材料、补给、零件、能量 | 材料、补给、零件、网络功率 |
| 单位名称 | 叛军和变种人全部单位 | 步枪兵、铁甲舰、无畏舰、巨人 |
| 建筑名称 | 全部建筑 | 兵营、加工厂、发电站、碉堡 |
| 单位/建筑描述 | 每个单位和建筑的详细说明 | 属性、用途、特殊能力 |
| 武器数据 | 火力、装甲、速度等属性 | 主要武器、纯净伤害、移动速度 |
| 任务系统 | 任务目标、天气事件、增援 | 增援部队正在途中、消灭残余 |
| 战斗统计 | 结算画面所有统计项 | 战斗统计、时间、伤亡 |
| 学说/升级 | 全部学说和升级项 | 突击学说、重型炮塔、穿甲弹 |
| 能力/支援 | 战术能力和支援技能 | 火炮引导、扫描、烟幕 |
| 操作说明 | 控制键位和提示 | 快捷键列表、右键取消 |
| 阵营选择 | 派系名称和描述 | 叛军、变种人 |

### 教程/演示文本（path_id=165，63 条）

| 分类 | 内容 |
|------|------|
| 开场/结束画面 | 欢迎语、感谢语、愿望单提示 |
| 界面教程 | 资源面板、小地图、编组系统 |
| 基础教程 | 建造、生产、选择、控制 |
| 高级教程 | 移动攻击、集火、占领建筑、能力 |
| 成就系统 | 达成条件描述 |

### 未翻译内容

| 内容 | 原因 |
|------|------|
| 开发者署名 | "A game by RtsDimon (Dmitry). Music by Edlise." |
| 游戏标题 | "DUST FRONT RTS" 为 Logo 图片 |
| 版本号 | "VERSION: D29-6" |
| Shader/调试文本 | 技术文本，玩家不可见 |

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
