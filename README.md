# Beamer 学术答辩演示文稿模板

基于 **XeLaTeX + Beamer (metropolis) + PingFang SC** 的中文学术答辩模板，
适用于学位论文答辩、技术分享、学术报告等场景。

## 特性

- ✅ 开箱即用，`latexmk` 一键编译
- ✅ 样式与内容分离（`.sty` + `.tex`）
- ✅ 中文完美支持（PingFang SC / 苹方-简）
- ✅ 学术答辩预设结构（标题 → 目录 → 背景 → 方法 → 结果 → 总结 → 参考文献）
- ✅ 5 种常用 slide 类型：标题页、目录、正文、图表、参考文献
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

## 快速开始

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

## 自定义指南

### 修改内容

编辑 `main.tex`：

```latex
% --- 元数据 ---
\title{你的论文题目}
\subtitle{硕士研究生学位论文答辩}
\author{你的姓名}
\institute{你的学校 / 学院}
\date{2026 年 6 月 20 日}
```

在 `\begin{document} ... \end{document}` 之间按 Section 组织幻灯片内容。

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

## 文件说明

| 文件 | 作用 |
|------|------|
| `main.tex` | 主文件，填写演示内容（元数据 + 各 Section 幻灯片） |
| `beamer-style.sty` | 样式配置（主题、颜色、字体、页脚、参考文献设置） |
| `refs.bib` | BibTeX 参考文献数据库 |
| `latexmkrc` | latexmk 编译配置（xelatex 引擎 + `build/` 中间产物目录） |
| `build/` | 编译中间产物目录（自动生成，已 git-ignore） |
| `img/` | 图片资源目录 |
| `main.pdf` | 编译生成的 PDF 输出（`.gitignore` 已忽略） |

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
**A:** 编辑 `main.tex` 第一行，将 `aspectratio=169` 改为 `aspectratio=43`。

### Q: 如何禁用参考文献？
**A:** 如果不需要参考文献，可删除 `main.tex` 最后的 `\section*{参考文献}` 帧，并在 `beamer-style.sty` 中注释掉 `\usepackage[...]{biblatex}` 相关行。

## 项目结构

```text
beamer-template/
├── README.md              ← 你正在看
├── main.tex               ← 主文件，编辑内容
├── beamer-style.sty       ← 样式文件，编辑外观
├── refs.bib               ← 参考文献
├── latexmkrc              ← 编译配置
├── .gitignore
├── build/                 ← 编译中间产物（自动生成）
├── img/                   ← 图片资源
├── docs/                  ← 项目规划文档
├── Archive/               ← 历史归档
└── experiments/           ← 实验性功能
```

## 许可

MIT License — 自由使用、修改和分发。
