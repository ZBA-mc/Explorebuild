# Explorebuild（双语版：中文 / English）

<details>

<summary>中文</summary>

# Explorebuild

一款基于 Python 实现的 Minecraft 风格沙盒游戏，支持 Faithful 64x 材质。

## 已实现功能：

- WASD 移动：流畅的第一人称世界漫游
- 第一人称视角：支持鼠标视角控制的沉浸式体验
- 随机地形生成：程序化生成地形，支持无限探索
- 多种方块类型：可收集、可放置的多种方块
- 空格跳跃：支持跑酷式空中跳跃
- 左键放置：在目标位置放置选中方块
- 右键破坏：通过交互移除方块
- 基于区块的地图系统：高效 4×4 区块（32×32 方块）渲染系统
- ESC 暂停菜单：通过暂停菜单访问设置或退出游戏
- 数字键选择方块：用数字键切换方块类型，手部模型显示当前方块

## 计划优化目标：

- 背包系统与物品栏界面
- 玩家与物体交互
- 生物 AI 与行为逻辑
- 增强地图生成与性能优化

## 搭建开发环境

### 安装方法

1. [下载 Python](https://www.python.org/ftp/python/3.13.12/python-3.13.12-amd64.exe)
2. 运行以下命令安装依赖库

```shell
python -m pip install pyglet perlin-noise numpy
```

   3.[下载全部资源文件](https://github.com/ZBA-mc/Explorebuild/archive/refs/heads/main.zip)，运行 main.py

</details>

<details>

<summary>English</summary>

# Explorebuild

A Minecraft-style sandbox game implemented in Python, featuring Faithful 64x texture support.

## Implemented Features:

- WASD Movement: Smooth first-person navigation across the world.
- First-Person Perspective: Immersive view with mouse look controls.
- Random Terrain Generation: Procedurally generated landscapes for endless exploration.
- Multiple Block Types: A variety of blocks to collect and place.
- Space Jump: Leap through the air for parkour-like movement.
- Left-Click Placement: Place selected blocks at target positions.
- Right-Click Destruction: Remove blocks by interacting with them.
- Chunk-Based Map System: Efficient 4×4 chunk (32×32 block) rendering system.
- ESC Pause Menu: Access settings or quit the game via a pause menu.
- Block Selection (Number Keys): Switch between block types with number keys, with hand visualization showing the active block.

## Planned Optimization Targets:

- Inventory system and backpack UI
- Player-object interactions
- Mob AI and behavior logic
- Enhanced map generation and performance tuning

## Set up the development environment

### How to install

1. [Download Python](https://www.python.org/ftp/python/3.13.12/python-3.13.12-amd64.exe)
2. Run the following command to install the support library

```
python -m pip install pyglet perlin-noise numpy
```

   3.[Download all the resources](https://github.com/ZBA-mc/Explorebuild/archive/refs/heads/main.zip) and run main.py

</details>
