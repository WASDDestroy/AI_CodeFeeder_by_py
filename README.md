
***

# 🚀 AI\_CodeFeeder

> **Stop Copy-Pasting. Start Coding.**
>
> 拒绝繁琐的复制粘贴，让 AI 更懂你的代码架构。

## 📖 简介 

**众所周知，大多数 AI（如 DeepSeek,豆包,ChatGPT, Claude, Gemini）不允许直接上传代码文件夹。**

劳累了一天的人们，往往还要不厌其烦地打开一个个文件，复制、粘贴，或者被迫使用 IDE 内置的昂贵或不够聪明的 AI 插件。这种方式不仅效率低下，而且丢失了项目原本的文件结构上下文，导致 AI 的回答往往不够准确。

**AI\_CodeFeeder** 因此诞生。👍🤓

它是一个基于 Python 的轻量级工具，能够**一键扫描**你的工程目录，智能过滤掉无关文件（如 `build`, `.git`, `node_modules` 以及 STM32/Unity 的垃圾文件），生成一份包含**完整目录树**和**所有源码内容**的 Markdown 文件。

你只需把这个文件“喂”给 AI，它就能立刻理解你的整个项目。


## 🛠️ 快速开始

### 1. 环境要求

* Python 3.x (已安装即可)

### 2. 使用方法

1. 下载 `AI_CodeFeeder.py` 到任意位置。

2. 运行脚本：

   Bash

   ```
   python AI_CodeFeeder.py
   ```

3. **操作步骤**：

   * **选择目录**：脚本会弹出一个窗口，选择你想要分析的**项目根目录**。

   * **确认扫描**：终端会显示即将包含的文件列表，按 **Enter (回车)** 确认。

   * **保存文件**：选择输出 `.md` 文件的保存位置（默认名为 `目录名_Codes.md`）。

### 3. 投喂 AI

打开生成的 `.md` 文件，全选复制，发送给 AI (ChatGPT / Claude / NotebookLM / DeepSeek 等)，并附上你的问题：

> "这是我的项目代码和结构，请帮我分析..."

## ⚙️ 配置说明

你可以直接打开 `AI_CodeFeeder.py` 修改顶部的配置区域，以适应不同项目：

### 1. 包含的文件类型

修改 `ALLOWED_EXTENSIONS` 集合：

Python

```
ALLOWED_EXTENSIONS = {
    '.py', '.java', '.cpp', '.c', '.h', '.js', '.ts', 
    '.cs', '.shader', '.md', '.txt' 
    # ... 添加你需要的文件后缀
}
```

### 2. 忽略的目录

修改 `IGNORE_DIRS` 集合。代码已默认内置了以下屏蔽规则：

* **通用**：`.git`, `.vscode`, `node_modules`, `venv`

* **编译产物**：`build`, `dist`, `bin`, `obj`, `cmake-build-*`

* **STM32/嵌入式**：`Drivers` (巨大的库文件), `Middlewares`, `MDK-ARM`

* **Unity**：`Library`, `Temp`, `Logs`

### 3. 忽略特定前缀文件 (CubeMX 专用)

修改 `IGNORE_PREFIXES`。这对于保持上下文简洁非常重要，它屏蔽了大量自动生成的冗余代码：

Python

```
IGNORE_PREFIXES = {
    'stm32f4xx_it',       # 忽略中断处理存根
    'system_stm32f4xx',   # 忽略系统初始化
    'stm32f4xx_hal_conf', # 忽略HAL配置
    # ...
}
```

## 📝 输出示例 

生成的 Markdown 文件内容如下所示：

Markdown

````
# Project Directory Structure

```text
MyProject/
    Core/
        Src/
            main.c
    PID/
        speed_pid.c
````

***

## File: Core/Src/main.c

C

```
#include "main.h"
// ... 代码内容 ...
```

***

## File: PID/speed\_pid.c

C

```
// ... 代码内容 ...
```



## 👨‍💻 版本与作者

**AI_CodeFeeder V1.0.5**
Coded by **ChaoPhone**

---
*Happy Coding!*

