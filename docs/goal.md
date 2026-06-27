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

<!-- feature:build-dir:start -->
## Feature: build-dir

### User Request

将 latexmk 编译产物归纳到独立 build/ 目录，保持项目根目录整洁

### Purpose Analysis

- 当前 MVP 每次编译会产生 10+ 个中间文件（`.aux`、`.log`、`.out`、`.toc`、`.nav`、`.snm`、`.bbl`、`.bcf`、`.blg`、`.fls`、`.xdv` 等），散落在项目根目录，干扰文件浏览和版本管理。
- 目标用户：使用本模板的学术答辩者，他们需要在干净的目录中快速定位 `main.tex` 和 `main.pdf`，而不是在一堆编译产物中翻找。
- 核心任务改进：编译后根目录只保留源文件和最终 PDF，所有中间产物自动归入 `build/`。
- 属于产品而非实验：这是 LaTeX 项目的标准工程实践（类似 `cmake-build-debug/` 或 `node_modules/`），直接纳入主项目。

### Minimum Feature Scope

- 配置 `latexmkrc`，将 `.aux`、`.log`、`.toc` 等中间文件输出到 `build/` 目录。
- PDF 保留在项目根目录，方便直接打开。
- 更新 `.gitignore`，简化为一键忽略 `build/`。
- 用户编译命令不变，仍为 `latexmk`。

### Non-Goals

- 不将 PDF 移入 `build/`（PDF 是最终产物，应在根目录方便访问）。
- 不提供多套输出目录方案（如按章节分目录）。
- 不改变 `latexmk -c` / `latexmk -C` 的清理行为。

### Success Criteria

- [x] `latexmk` 编译后，根目录无 `.aux`、`.log`、`.out`、`.toc` 等中间文件。✅
- [x] 所有中间文件生成在 `build/` 目录下。✅ 13 个文件归拢于 `build/`
- [x] `main.pdf` 仍然生成在根目录。✅
- [x] 原有 17 页模板编译结果不变。✅ 0 错误，0 overfull 警告
<!-- feature:build-dir:end -->

<!-- feature:groupmeeting-preset:start -->
## Feature: groupmeeting-preset

### User Request

中文模板提供组会汇报预设场景，让用户可以快速选择组会汇报的幻灯片结构

### Purpose Analysis

- **用户真实目标**：除了学位论文答辩，用户还需要频繁参加课题组会，每次汇报本周工作进展。当前模板只有「学术答辩」一种幻灯片结构，用户每次组会前需要手动删除/修改答辩模板中的章节（研究背景、相关工作、技术选型表等），重复劳动且容易遗漏，产出的幻灯片结构也不自然。
- **目标用户**：需要每周/双周进行组会汇报的研究生、博士生、科研人员。与答辩模板是同一个用户群体，但面对完全不同的使用场景（日常高频汇报 vs 一次性正式答辩）。
- **核心任务改进**：从「拿到答辩模板 → 删改内容 → 适配组会结构」缩短为「直接选用组会模板 → 填写本周内容」。
- **属于产品而非实验**：组会汇报是学术用户最高频的演示场景之一（远高于答辩），与现有答辩模板互补，应直接纳入主项目作为正式预设场景。「答辩」「组会汇报」「技术分享」三种预设场景在 MVP 规划中已预先列入 Later 清单。

### Minimum Feature Scope

- 新增一个 `main-groupmeeting.tex` 文件，提供组会汇报的幻灯片结构。
- 复用现有 `beamer-style.sty` 样式文件，不修改样式，保持视觉一致性。
- 组会汇报预设结构：标题页（含导师/课题组）→ 本周工作概览 → 详细进展（1-2 帧）→ 遇到的问题与讨论 → 下周计划 → 致谢 & Q&A。
- 更新 README，说明两种预设场景（答辩 vs 组会）的差异、文件对应关系和选择建议。
- 注释风格与 `main.tex` 一致，标注用户可修改点。

### Non-Goals

- 不提供模板选择器/自动切换机制（用户手动选择 `.tex` 文件即可，符合 LaTeX 用户习惯）。
- 不修改现有 `main.tex`（学术答辩模板）的结构和内容。
- 不修改 `beamer-style.sty`（样式对两种场景完全通用）。
- 不提供「技术分享」等其他预设场景（此 feature 只做组会汇报，其余留在 Later）。
- 不提供 Markdown → Beamer 的转换工具。
- 不提炼共同结构宏集（等场景数量 ≥ 4 时再考虑）。

### Success Criteria

- [x] `main-groupmeeting.tex` 开箱可编译，`latexmk` 一次通过，生成无错误的 PDF。✅ 12 页，0 错误
- [x] 中文渲染正常（PingFang SC），无乱码，字体回退合理。✅
- [x] 覆盖组会汇报核心幻灯片类型：标题页、问题背景、本周概览、详细进展、结果展示、问题讨论、下周计划、致谢、附录。✅
- [x] README 更新，明确说明两种预设场景的差异和选择方式。✅
- [x] 现有 `main.tex`（学术答辩模板）回归编译不受影响（仍为 19 页 PDF，0 错误）。✅
<!-- feature:groupmeeting-preset:end -->

<!-- feature:appendix-pages:start -->
## Feature: appendix-pages

### User Request

给两份模版都加入一页附录，利用 Beamer 的 \appendix 命令让备用幻灯片不计入进度条总页数

### Purpose Analysis

- **用户真实目标**：答辩或组会讨论环节，评委/导师常追问细节，这些内容不适合放在正式汇报中（会拖长时间、分散重点），但需要能快速调出展示。附录（backup slides）正是 Beamer 的标准解决方案——`\appendix` 后页码自动切换为 A-1, A-2, ...，用户按需跳转。
- **目标用户**：与 MVP 相同——需要答辩或组会汇报的研究生/科研人员。附录是学术答辩事实上的标配组件。
- **属于产品而非实验**：使用 Beamer 内置 `\appendix` + `\insertmainframenumber` 判断，不引入新工具、新宏包。

### Minimum Feature Scope

- 修改 `beamer-style.sty` 的 footline 模板，正文显示 "X/Y"，附录自动切换为 "A-Z"。
- 在 `main.tex` 参考文献后添加 `\appendix` + 一个示例附录帧。
- 在 `main-groupmeeting.tex` 致谢后添加 `\appendix` + 一个示例附录帧。
- 更新 README，说明附录功能。
- 回归验证两个模板正文部分编译结果不变。

### Non-Goals

- 不添加真实附录内容（仅提供示例占位帧，用户自行填充）。
- 不引入 `appendixnumberbeamer` 等额外宏包。
- 不改变现有正文帧的顺序和编号。

### Success Criteria

- [x] `main.tex` 编译通过，19 页（正文 17+1 标题帧 A-1+1 内容帧 A-2），0 新错误。✅
- [x] `main-groupmeeting.tex` 编译通过，12 页（正文 10+1 标题帧 A-1+1 内容帧 A-2），0 新错误。✅
- [x] 正文页码显示 "X/Y"，附录页码显示 "A-Z"（pgfkey 中性化 + `\ifbeamer@inappendix`）。✅
- [x] 两份模板回归编译零 overfull 警告。✅
<!-- feature:appendix-pages:end -->

<!-- feature:cover-logo:start -->
## Feature: cover-logo

### User Request

在封面右上角添加机构/课题组 Logo

### Purpose Analysis

- **用户真实目标**：学术答辩和组会汇报通常需要展示学校、学院或课题组的标识，这是学术演示的标配元素。
- **属于产品而非实验**：使用 Beamer 内置 tikz（已默认加载）的 overlay 定位，零额外依赖。

### Minimum Feature Scope

- 在 `main.tex` 和 `main-groupmeeting.tex` 的标题帧中通过 tikz overlay 定位 Logo。
- Logo 位置：封面右上角，通过 `xshift`/`yshift` 灵活调整。
- Logo 文件：`img/logo.png`（用户自行替换）。

### Non-Goals

- 不在非封面帧显示 Logo（仅封面）。
- 不修改 `beamer-style.sty`。

### Success Criteria

- [x] `main.tex` 封面 Logo 渲染正常，编译 0 错误。✅
- [x] `main-groupmeeting.tex` 封面 Logo 渲染正常，编译 0 错误。✅
<!-- feature:cover-logo:end -->

<!-- feature:groupmeeting-enhance:start -->
## Feature: groupmeeting-enhance

### User Request

组会模板增加「问题背景」和「结果展示」帧

### Purpose Analysis

- **用户真实目标**：
  1. 组会听众（导师、同门）可能不熟悉每个人的课题细节，需要在汇报开头提供问题背景。
  2. 每周工作的核心产出（实验结果、图表、数据对比）需要专门的展示区域，而非混在进展详情中一笔带过。
- **属于产品而非实验**：直接扩展现有模板的幻灯片结构，不引入新依赖。

### Minimum Feature Scope

- 新增「问题背景」帧（Section 2）：研究课题、核心问题、应用场景、当前瓶颈、本文思路。
- 新增「结果展示」帧：图表占位 + caption 说明。
- 新增「结果分析」帧：booktabs 三线表性能对比 + 文字分析。

### Non-Goals

- 不修改 `beamer-style.sty`。
- 不影响 `main.tex`。

### Success Criteria

- [x] `main-groupmeeting.tex` 编译通过，12 页，0 新错误。✅
- [x] 新增 3 帧均含示例内容 + 替换说明注释。✅
- [x] `main.tex` 回归编译不受影响（19 页）。✅
<!-- feature:groupmeeting-enhance:end -->
