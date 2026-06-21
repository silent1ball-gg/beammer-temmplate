# Beamer 学术答辩演示文稿模板

基于 **XeLaTeX + Beamer (metropolis) + PingFang SC** 的中文学术答辩模板，
适用于学位论文答辩、技术分享、学术报告等场景。

## 特性

- ✅ 开箱即用，`latexmk` 一键编译
- ✅ 样式与内容分离（`.sty` + `.tex`）
- ✅ 中文完美支持（PingFang SC / 苹方-简）
- ✅ **两种预设场景**：学术答辩 + 组会汇报，按需选用
- ✅ 6+ 种常用 slide 类型：标题页、目录、正文、图表、问题讨论、参考文献
- ✅ **附录备份幻灯片**：正文后附录帧，页码自动切换为 A-1, A-2, ...
- ✅ 16:9 宽屏比例，适配现代投影仪
- ✅ biber + biblatex 参考文献管理

## 环境依赖

| 组件 | 说明 | 安装方式 |
|------|------|----------|
| TeX Live / MacTeX | LaTeX 发行版 | `brew install mactex` (macOS) |
| XeLaTeX | 编译引擎 | 随 TeX Live 安装 |
| latexmk | 自动化构建 | 随 TeX Live 安装 |
| biber | 参考文献引擎 | 随 TeX Live 安装 |

> **⚠️ 仅支持 XeLaTeX 编译。** pdfLaTeX 和 LuaLaTeX 未经测试，可能无法正确处理中文。

## 预设场景

本项目提供 **两种预设场景**，根据你的实际需求选择对应的模板文件：

| 场景 | 模板文件 | 适用场合 | 典型结构 |
|------|----------|----------|----------|
| **学术答辩** | `main.tex` | 学位论文答辩、开题报告、中期检查 | 标题 → 目录 → 研究背景 → 相关工作 → 研究方法 → 实验结果 → 总结展望 → 致谢 → 参考文献 |
| **组会汇报** | `main-groupmeeting.tex` | 每周/双周课题组进展汇报 | 标题 → 本周概览 → 进展详情 → 问题讨论 → 下周计划 → 致谢 |

> 💡 **选择建议**：正式答辩用 `main.tex`（约 12-17 页），日常组会用 `main-groupmeeting.tex`（约 7 页）。两个模板共享同一个 `beamer-style.sty` 样式文件，视觉风格完全一致。

## 快速开始

### 学术答辩模板

```bash
cd beamer-template

# 编译 PDF
latexmk

# 查看生成的 main.pdf
open main.pdf
```

### 组会汇报模板

```bash
cd beamer-template

# 编译 PDF（注意：使用 -jobname 指定输出文件名）
latexmk -jobname=main-groupmeeting main-groupmeeting.tex

# 查看生成的 main-groupmeeting.pdf
open main-groupmeeting.pdf
```

```bash
# 1. 克隆或复制本项目
# 2. 进入项目目录
cd beamer-template

# 3. 编译 PDF（首次编译会自动运行 biber 处理参考文献）
latexmk

# 4. 查看生成的 main.pdf
open main.pdf
```

### 常用命令

```bash
# 清理编译产物（保留 PDF）
latexmk -c

# 完全清理（包括 PDF）
latexmk -C

# 强制重新编译
latexmk -g
```

### VS Code 编译

项目已包含 `.vscode/settings.json`，安装 **LaTeX Workshop** 扩展后即可开箱即用：

```bash
# 1. 安装 VS Code 扩展（二选一）
code --install-extensions James-Yu.latex-workshop    # 命令行安装
# 或在 VS Code 扩展市场搜索 "LaTeX Workshop"

# 2. 用 VS Code 打开项目
code beamer-template

# 3. 打开 main.tex，保存即自动编译
# 4. 右侧分屏自动打开 PDF 预览
```

| 快捷键 | 功能 |
|--------|------|
| `Cmd+Alt+B` | 手动编译 |
| `Cmd+Alt+V` | 打开 PDF 预览 |
| `Cmd+Alt+C` | 清理辅助文件 |
| 双击 PDF 中的文本 | 跳转到源码对应位置（Synctex） |

> **提示**：保存文件时会自动触发编译（`onSave`）。如需关闭，修改 `.vscode/settings.json` 中 `latex-workshop.latex.autoBuild.run` 为 `"never"`。

## 自定义指南

### 修改内容

编辑对应的模板文件（`main.tex` 或 `main-groupmeeting.tex`）：

**学术答辩模板** (`main.tex`)：

```latex
% --- 元数据 ---
\title{你的论文题目}
\subtitle{硕士研究生学位论文答辩}
\author{你的姓名}
\institute{你的学校 / 学院}
\date{2026 年 6 月 20 日}
```

在 `\begin{document} ... \end{document}` 之间按 Section 组织幻灯片内容。

**组会汇报模板** (`main-groupmeeting.tex`)：

```latex
% --- 元数据 ---
\title{本周研究进展汇报}
\subtitle{课题组组会}
\author{你的姓名}
\institute{你的学校 ~ 学院 ~ 课题组}
\date{2026 年 6 月 20 日}
```

组会模板无 Section 结构，直接按帧（frame）填写：本周概览 → 进展详情 → 问题讨论 → 下周计划。文献阅读帧和参考文献帧默认注释，按需取消注释。

### 修改样式

编辑 `beamer-style.sty`：

- **切换主题**：修改 `\usetheme{metropolis}` 为 `Madrid`、`CambridgeUS` 等
- **更改配色**：修改 `\definecolor{AccentBlue}{HTML}{005A9C}` 中的色值
- **更换字体**：修改 `\setCJKsansfont{PingFang SC}` 为其他字体名
- **调整页脚**：修改 `\setbeamertemplate{footline}{...}`

### 添加图片

将图片放入 `img/` 目录，在 slide 中引用：

```latex
\includegraphics[width=0.6\textwidth]{img/your-image.png}
```

### 添加参考文献

编辑 `refs.bib`，添加 BibTeX 条目：

```bibtex
@article{key2024,
  author  = {作者名},
  title   = {文章标题},
  journal = {期刊名},
  year    = {2024},
}
```

在正文中引用：`\cite{key2024}`

### 使用附录

两个模板均在正文末尾预留了 **附录（Appendix）** 区域，适合放置备份材料供答辩或讨论环节按需展示：

- **自动页码切换**：正文显示 `X / Y` 格式，进入附录后自动切换为 `A-1, A-2, ...`。无需手动配置。
- **添加更多附录帧**：在 `\appendix` 之后按需插入 `\begin{frame}...\end{frame}` 即可，页码自动递增。
- **位置**：学术答辩模板中附录在参考文献之后，组会模板中附录在致谢之后。

## 文件说明

| 文件 | 作用 |
|------|------|
| `main.tex` | 学术答辩模板，填写演示内容（元数据 + 各 Section 幻灯片） |
| `main-groupmeeting.tex` | **组会汇报模板**，填写本周进展（概览 → 详情 → 问题 → 计划） |
| `beamer-style.sty` | 样式配置（主题、颜色、字体、页脚、参考文献设置），两种场景共享 |
| `refs.bib` | BibTeX 参考文献数据库 |
| `latexmkrc` | latexmk 编译配置（xelatex 引擎 + `build/` 中间产物目录） |
| `build/` | 编译中间产物目录（自动生成，已 git-ignore） |
| `img/` | 图片资源目录 |
| `main.pdf` / `main-groupmeeting.pdf` | 编译生成的 PDF 输出（`.gitignore` 已忽略） |

## 常见问题

### Q: 编译报错 "The font PingFang SC cannot be found"
**A:** 本模板默认使用 macOS 系统字体苹方-简（PingFang SC）。如果你使用其他平台，请编辑 `beamer-style.sty`，将字体替换为可用的中文字体：

```latex
\setCJKsansfont{Noto Sans CJK SC}    % Linux
\setCJKsansfont{SimSun}              % Windows (宋体)
\setCJKsansfont{Microsoft YaHei}     % Windows (微软雅黑)
```

### Q: 编译后英文用的不是 Fira Sans 字体
**A:** 这是一个已知限制（见 [decisions.md](docs/decisions.md)）。macOS 的 XeTeX 无法通过字体名找到 TeX Live 中的 Fira Sans，会自动回退到 Latin Modern Sans。如需修复，可在 `beamer-style.sty` 中用文件路径方式显式指定 Fira 字体。

### Q: 如何更改屏幕比例为 4:3？
**A:** 编辑对应 `.tex` 文件第一行，将 `aspectratio=169` 改为 `aspectratio=43`。

### Q: 学术答辩和组会汇报应该选哪个模板？
**A:** 
- **学术答辩** (`main.tex`)：适用于学位论文答辩、开题报告、中期检查等正式场合，结构完整（12-17 页），包含研究背景、相关工作、方法、实验结果、参考文献等章节。
- **组会汇报** (`main-groupmeeting.tex`)：适用于每周/双周课题组进展汇报，结构精简（约 7 页），聚焦本周工作、遇到的问题和下周计划。
- 两个模板共享同一个样式文件，视觉风格一致。选择对应场景的模板后，修改元数据和内容即可。

### Q: 如何编译组会汇报模板？
**A:** 使用 `latexmk -jobname=main-groupmeeting main-groupmeeting.tex` 命令。`-jobname` 参数确保 PDF 输出为 `main-groupmeeting.pdf` 而非 `main.pdf`，避免覆盖答辩模板的输出。如果使用 VS Code + LaTeX Workshop，打开 `main-groupmeeting.tex` 后保存即可自动编译。

### Q: 如何禁用参考文献？
**A:** 如果不需要参考文献，可删除 `main.tex` 最后的 `\section*{参考文献}` 帧，并在 `beamer-style.sty` 中注释掉 `\usepackage[...]{biblatex}` 相关行。

### Q: 附录页码如何工作？如何删除或添加附录帧？
**A:** 附录页码由 `beamer-style.sty` 的 footline 自动处理：当帧号超过正文帧数时，页码从 `X/Y` 切换为 `A-Z`。删除附录：直接删除 `.tex` 文件中 `\appendix` 到 `\end{document}` 之间的内容。添加更多附录帧：在 `\appendix` 后继续添加 `\begin{frame}...\end{frame}` 即可，页码自动递增。

## 项目结构

```text
beamer-template/
├── README.md                  ← 你正在看
├── main.tex                   ← 学术答辩模板
├── main-groupmeeting.tex      ← 组会汇报模板
├── beamer-style.sty           ← 样式文件，编辑外观
├── refs.bib                   ← 参考文献
├── latexmkrc                  ← 编译配置
├── .gitignore
├── .vscode/                   ← VS Code + LaTeX Workshop 配置
├── build/                     ← 编译中间产物（自动生成）
├── img/                       ← 图片资源
├── docs/                      ← 项目规划文档
├── Archive/                   ← 历史归档
└── experiments/               ← 实验性功能
```

## 许可

MIT License — 自由使用、修改和分发。
