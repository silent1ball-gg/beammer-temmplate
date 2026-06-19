# Goal

## User Request

我想做一个 latex 做的 beamer —— 构建一个可复用的 LaTeX Beamer 演示文稿模板。

## Purpose Analysis

- 真正的目标：拥有一套开箱即用的 Beamer 模板，每次做演示文稿时不需要从零配置主题、颜色、字体、页眉页脚，只需填充内容即可生成专业美观的 PDF。
- 核心用户：需要频繁制作学术/技术演示文稿的研究者、工程师或学生。
- 核心任务（job-to-be-done）：用最少的配置工作，快速产出一份排版精美、风格统一的 Beamer PDF 幻灯片。
- 最小核心价值：**一个可编译的 `.tex` 文件，包含合理的 Beamer 默认配置（主题、配色、字体、页码），用户只需 `latexmk` 一下就能得到一份像样的 PDF。**
- 与锦上添花功能的区分：多套主题切换、复杂布局组件、CI 自动构建等属于后续增强功能。

## MVP Definition

采用一条可长期维护的技术路线，构建能服务用户核心目的的最小能力：

1. 一个主模板文件 `main.tex`，用户复制后修改内容即可使用。
2. 一个样式配置文件 `beamer-style.sty`，集中管理主题、颜色、字体等外观设置。
3. 一份示例内容，展示标题页、目录、正文页、图表页、引用页等常见 slides 类型。
4. 一个 `latexmk` 构建配置，一键编译出 PDF。
5. 一份简明 README，说明依赖安装和编译方法。

## Assumptions

- 用户使用 macOS 平台，已安装或愿意安装 TeX Live (MacTeX)。
- 用户偏好中文支持（xelatex/lualatex 编译引擎）。
- 用户需要的是学术/技术风格的简洁模板，非花哨的营销风格。
- 采用 latexmk 作为构建工具（TeX Live 自带）。
- 默认输出面向 16:9 屏幕比例。

## Non-Goals

- 不提供多套主题切换机制（MVP 只提供一套精心调整的默认主题）。
- 不集成 CI/CD 自动构建 PDF。
- 不提供 Overleaf 在线编辑支持（本地编译优先）。
- 不制作花哨的动画/过渡效果。
- 不提供 Markdown → Beamer 的转换工具链。

## Target User

需要频繁制作学术报告、技术分享、论文答辩等演示文稿的中文用户，熟悉 LaTeX 基本操作，希望有一份专业模板减少重复配置工作。

## Success Criteria

- [x] `main.tex` 开箱可编译，`latexmk` 一次通过，生成无错误的 PDF。✅ 17 页，0 错误，0 overfull 警告
- [x] 模板包含标题页、目录页、正文内容页、图表页、引用页至少 5 种 slide 示例。✅ 覆盖全部 5 种 + 致谢页
- [x] 中文渲染正常，无乱码，字体回退合理。✅ 0 中文字符缺失，PingFang SC + Latin Modern Sans
- [x] README 覆盖：依赖安装、编译命令、自定义方法。✅ 包含快速开始、自定义指南、FAQ
- [x] 代码结构清晰，样式与内容分离（`.sty` + `.tex`）。✅ beamer-style.sty + main.tex 完全分离
