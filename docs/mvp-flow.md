# MVP Flow

## Milestone 1: Project Foundation ✅

- [x] 确认技术路线：LaTeX Beamer + XeLaTeX + latexmk。
- [x] 确认本地环境：TeX Live 2026，`xelatex` 3.14、`latexmk` 4.88、`biber` 2.21 均已可用。
- [x] 创建项目文件结构（`.gitignore`、`latexmkrc`、`main.tex`、`beamer-style.sty`、`refs.bib`、`img/`），编写 README 骨架。
- [x] 验证通过：`latexmk` 成功编译 hello-world Beamer 文档（7 页 PDF），中文暂缺但框架可运行。

## Milestone 2: Core Data or Domain Model — Style Configuration ✅

- [x] 编写 `beamer-style.sty`：metropolis 主题 + PingFang SC (CJK) + 学术蓝配色 (#005A9C) + 页码页脚。
- [x] `main.tex` 通过 `\usepackage{beamer-style}` 引用样式。
- [x] 验证通过：中英文混排正常，0 个中文字符缺失，颜色和字体符合预期。仅有的警告：metropolis 未找到 Fira Sans（回退 Latin Modern Sans，非致命）。

## Milestone 3: Main User Workflow — Content Template & Examples ✅

- [x] 编写示例幻灯片内容，覆盖 5+ 种常用 slide 类型：
  1. 标题页（含导师/答辩委员会信息）
  2. 目录页（自动生成 `\tableofcontents`）
  3. 正文内容页（itemize、enumerate、description、columns、block/alertblock/exampleblock、table）
  4. 图表页（`figure` + `\includegraphics{example-image}` + `\caption`）
  5. 参考文献页（`\printbibliography`，biber 后端）
  6. 致谢页
- [x] 添加详细 LaTeX 注释，标注用户可修改部分。
- [x] 验证通过：17 页 PDF 编译成功，排版整洁，所有 slide 类型正常显示。

## Milestone 4: Verification and Demo ✅

- [x] 从零模拟用户流程：`latexmk -C` 清理 → 删除 PDF → `latexmk` 重新编译 → 成功生成 17 页 PDF。
- [x] PDF 质量检查：0 overfull 警告、0 中文字符缺失、页码正确（帧号/总帧数格式）。
- [x] README 完善：依赖安装 (MacTeX)、编译命令 (latexmk)、自定义指南（内容、样式、图片、参考文献）、常见问题（字体替换、平台兼容、比例切换）。
- [x] 已知限制已文档化：Fira Sans 回退、仅支持 XeLaTeX、中文字体绑定 macOS、单主题、无代码高亮。
- [x] 文档验证通过（`validate_mvp_docs.py`）。

## Later

- 支持多套颜色主题切换（light/dark/accent color 变体）。
- 添加 Beamer 高级特性：渐显列表、代码高亮（minted/lstlisting）、定理环境。
- 提供 Overleaf 兼容版（单文件 `.tex`，去掉 `.sty` 外部依赖）。
- CI 自动编译 + GitHub Release 发布 PDF。
- 中文模板提供「答辩」「学术报告」「技术分享」三种预设场景。
- 支持 4:3 屏幕比例备选。
- 修复 Fira Sans 字体问题（通过 `Extension=.otf` 方式加载 TeX 字体文件）。

<!-- feature:build-dir:start -->
## Feature Flow: build-dir

### Milestone 1: Current State and Route Fit ✅

- 当前 `latexmkrc` 仅有 `$pdf_mode = 5` 和清理配置，所有编译产物写入根目录。
- 长期技术路线是 latexmk 管理构建流程 → 本功能天然使用 latexmk 内置的 `$aux_dir` 能力，不引入新工具。
- 验证通过：升级前根目录确有 10+ 个中间文件。

### Milestone 2: Domain or Interface Change ✅

- 在 `latexmkrc` 中添加 `$aux_dir = 'build';` 一行。
- 在 `.gitignore` 中删除逐个中间文件列表，替换为 `build/` 目录忽略。
- 用户接口不变：编译命令 `latexmk`、清理命令 `latexmk -c` / `latexmk -C` 保持不变。
- 验证通过。

### Milestone 3: End-to-End Feature Workflow ✅

- 修改 `latexmkrc` 和 `.gitignore`。
- 执行 `latexmk` 编译。
- 验证通过：
  - 根目录下仅剩源文件 + `main.pdf`，零中间文件泄露。
  - `build/` 目录生成，包含 13 个中间文件。
  - `main.pdf` 内容不变（17 页，121KB）。

### Milestone 4: Regression Check and Demo ✅

- 全量清理后从零编译：`latexmk -C && rm -f main.pdf && latexmk` → 17 页 PDF 无误。
- `README.md` 文件结构说明已更新，标注 `build/` 为编译产物目录。
- 无新增已知限制。

### Later

- （已完成）`.gitignore` 中 `build/` 规则已生效。
<!-- feature:build-dir:end -->

<!-- feature:groupmeeting-preset:start -->
## Feature Flow: groupmeeting-preset

### Milestone 1: Current State and Route Fit ✅

- [x] 当前 MVP 已完成：`main.tex`（学术答辩模板，17 页）、`beamer-style.sty`（metropolis + PingFang SC + 学术蓝配色）、`latexmkrc`（xelatex + build/ 隔离）、`refs.bib` 均稳定可用。
- [x] 技术路线确认：XeLaTeX + Beamer (metropolis) + PingFang SC + latexmk，样式与内容分离（`.sty` + `.tex`）。
- [x] 本 feature 不引入新工具、新宏包、新样式，仅新增一个内容模板文件。完全符合并延续现有技术路线。
- [x] Verification：`latexmk -C && latexmk` 实际编译 `main.tex`，结果 — 17 页 PDF，0 错误，0 Overfull 警告。已知警告（Fira Sans 回退 × 2、Frame shrunk × 2、fontspec、rerun）与基线一致。回归基线已建立。

### Milestone 2: Slide Structure Design ✅

- [x] 设计组会汇报的幻灯片结构（共 6 帧，约 10-12 页 PDF），与学术答辩模板的差异对比如下：

| # | 学术答辩 (main.tex) | 组会汇报 (main-groupmeeting.tex) |
|---|-------------------|--------------------------------|
| 1 | 标题页 + 答辩委员会 | 标题页 + 导师/课题组 |
| 2 | 目录 (`\tableofcontents`) | 本周工作概览（itemize 摘要，2-3 项） |
| 3 | 研究背景 | 工作进展详情 I — 具体展开，可含 block/图表 |
| 4 | 相关工作 | 工作进展详情 II — 第二项工作或补充细节 |
| 5 | 模板架构设计 | **遇到的问题与讨论** — alertblock 突出障碍 |
| 6 | 技术选型表 | **下周工作计划** — enumerate 清晰列出 |
| 7 | 编译性能测试 | **致谢 & Q&A** — 大号居中文字 |
| 8 | 实验结果可视化 | — |
| 9 | 主要贡献 | — |
| 10 | 未来工作 | — |
| 11 | 致谢 | — |
| 12 | 参考文献 | — |

- [x] 组会模板特点：
  - **无 `\section` 目录结构**：组会内容短，不需要 `\tableofcontents`，直接 itemize 罗列工作项
  - **无参考文献页**：日常组会通常不列出正式引用（除非汇报文献阅读）
  - **突出问题讨论**：用 `alertblock` 高亮遇到的困难，引导导师和同门给出建议
  - **强调下周计划**：组会的核心产出之一是明确下一步做什么
  - **可含文献阅读帧**（可选）：用 block/exampleblock 展示读过的论文要点

- [x] 确认 `beamer-style.sty` 引用路径正确：`\usepackage{beamer-style}`（与 `main.tex` 一致，同目录）。
- [x] 确认元数据区格式与 `main.tex` 一致（`\title`、`\author`、`\institute`、`\date`），注释风格统一。
- [x] Verification：结构设计覆盖组会核心场景，帧数精简（6-7 帧 vs 答辩的 12 帧），结构文档化。

### Milestone 3: End-to-End Feature Workflow ✅

- [x] 编写 `main-groupmeeting.tex` 完整内容（183 行），包含 7 帧幻灯片 + 2 个可选帧（文献阅读、参考文献）：
  1. 标题页（`[shrink]` + 导师信息）
  2. 本周工作概览（itemize + block 总体进度）
  3. 工作进展详情 — 数据预处理（enumerate + exampleblock）
  4. 工作进展详情 — 基线模型实验（columns 双栏 + itemize）
  5. 遇到的问题与讨论（2 个 alertblock，突出问题）
  6. 下周工作计划（enumerate + 子 itemize + block 目标）
  7. 致谢 & Q&A（居中大号文字）
  
  可选帧（已注释，按需取消注释）：
  - 文献阅读笔记（双 block 对比两篇论文）
  - 参考文献页（`\printbibliography`）
- [x] 全部帧附带详细 LaTeX 注释，标注用户可修改点，风格与 `main.tex` 一致。
- [x] 编译成功：
  ```bash
  latexmk -jobname=main-groupmeeting main-groupmeeting.tex
  ```
- [x] Verification：
  - 7 页 PDF，68,009 字节 ✅
  - 0 错误，0 Overfull 警告 ✅
  - 中文字符无缺失（PingFang SC 正常渲染）✅
  - 所有 slide 类型正常显示（标题页、概览、详情 ×2、问题讨论、下周计划、致谢）✅

### Milestone 4: Regression Check and Demo ✅

- [x] 回归验证 `main.tex`：删除 PDF → `latexmk` 重新编译 → 17 页 PDF，123,522 字节。0 错误，0 Overfull 警告。与基线完全一致。
- [x] 从零编译两个模板，均一次通过：
  - `main.tex` → 17 页 ✅
  - `main-groupmeeting.tex` → 7 页 ✅
- [x] README 更新：
  - 新增「预设场景」小节，对比表格展示两种模板的适用场景、文件对应、典型结构
  - 快速开始区分答辩和组会两种编译命令
  - 自定义指南补充组会模板的元数据修改说明
  - 文件说明表增加 `main-groupmeeting.tex` 条目
  - 项目结构树增加 `main-groupmeeting.tex`
  - FAQ 新增：模板选择建议、组会模板编译方法
- [x] `.gitignore` 检查：`*.pdf` 规则已覆盖 `main-groupmeeting.pdf`，无需修改。
- [x] 已知限制更新：`decisions.md` 中「单主题」→「单主题配色」，新增「预设场景有限（当前 2 种）」。
- [x] 文档验证：`validate_mvp_docs.py` 通过。

### Later

- 提供「技术分享」预设场景（`main-techshare.tex`）
- 提供简洁的 Makefile 或 `select-template.sh`，交互式选择预设场景
- 当场景数量 ≥ 4 时，将共同结构提炼为 `beamer-common.tex` 或 `\newcommand` 宏集
- 考虑在 `latexmkrc` 中添加 `@default_files` 多文件支持
<!-- feature:groupmeeting-preset:end -->

<!-- feature:appendix-pages:start -->
## Feature Flow: appendix-pages

### Milestone 1: Current State and Route Fit ✅

- [x] 当前 MVP 状态：`main.tex`（学术答辩，17 页）、`main-groupmeeting.tex`（组会汇报，7 页），两份模板均无附录机制。
- [x] 技术路线确认：XeLaTeX + Beamer (metropolis) + PingFang SC + latexmk。`\appendix` 是 Beamer 内置命令，`\insertmainframenumber` 是 Beamer 内置计数器，零新依赖。
- [x] 用户决策：用户确认附录需要独立页码样式（A-1, A-2），通过修改 footline 模板中的判断条件实现。
- [x] Verification：编译两个模板确认基线 — `main.tex` 17 页，`main-groupmeeting.tex` 7 页，均 0 错误 0 overfull。

### Milestone 2: Domain or Interface Change ✅

- [x] 变更范围：三个文件 — `beamer-style.sty`（pgfkey 中性化 + footline 模板）、`main.tex`（`\appendix` + `\section{附录}` + 示例帧）、`main-groupmeeting.tex`（同上）。
- [x] 页码方案：`\ifbeamer@inappendix` + `\insertframenumberinappendix`（Beamer 内置机制），正文 "X/Y"，附录 "A-Z"。
- [x] metropolis 对抗：pgfkey 中性化（清空 `numbering=none` 和 `progressbar=none` 的 `.code`），阻止 metropolis 在 `\appendix` 时覆盖用户 footline。
- [x] 保留 `\section{附录}`：生成标题帧作为附录入口，页码显示 A-1。
- [x] Verification：总计约 30 行改动，零新宏包。实验验证过程见 `experiments/appendix-page-number-bug/docs/`。

### Milestone 3: End-to-End Feature Workflow ✅

- [x] 修改 `beamer-style.sty`：pgfkey 中性化 + `\ifbeamer@inappendix` footline。
- [x] 修改 `main.tex`：参考文献后插入 `\appendix` + `\section{附录}` + 示例帧。
- [x] 修改 `main-groupmeeting.tex`：致谢后插入 `\appendix` + `\section{附录}` + 示例帧。
- [x] 编译验证：`main.tex` → 19 页（正文 17 + 1 标题帧 A-1 + 1 内容帧 A-2），0 错误。
- [x] `main-groupmeeting.tex` → 9 页（正文 7 + 1 标题帧 A-1 + 1 内容帧 A-2），0 错误。
- [x] 诊断 `\typeout` 确认：33 次 footline 调用，附录帧 `inappendix=YES, offset=1`。

### Milestone 4: Regression Check and Demo ✅

- [x] 全量清理从零编译两个模板通过。
- [x] `main.tex` → 19 页，正文页码 X/12，附录 A-1、A-2。✅
- [x] `main-groupmeeting.tex` → 9 页，正文页码 X/7，附录 A-1、A-2。✅
- [x] 更新 README：特性列表、自定义指南新增附录小节、FAQ。
- [x] `validate_mvp_docs.py` 通过。

### Later

- 提供预设的附录帧模板（数据表附录、代码附录、推导附录等）。
<!-- feature:appendix-pages:end -->

<!-- feature:multi-design-interface:start -->
## Feature Flow: multi-design-interface

### Interface Workflow ✅

1. 内容模板在 `\usepackage` 中声明 `design=<name>`。
2. `beamer-style.sty` 校验设计名并装载对应的 `beamer-design-<name>.sty`。
3. 设计档案设置基础主题和视觉参数；公共接口层再统一加载字体、引用、表格和页码逻辑。
4. 同一内容在不同档案下重建为相应外观。

### Validation Plan

- 默认 academic：回归编译两份内容模板。
- classic、midnight：运行 `tests/design-smoke.tex`，验证主题、中文、block、附录页码能共同工作。
- 检查未知设计名是否给出明确的可选值提示。
<!-- feature:multi-design-interface:end -->

<!-- feature:weekly-report-workflow:start -->
## Feature Flow: weekly-report-workflow

### Milestone 1: Current State and Route Fit

- 已确认：项目已有 `main-groupmeeting.tex`、共用 `beamer-style.sty`、三种视觉设计和 `latexmk` 构建路径。
- 该功能只增加内容层与使用文档；周度输入作为人类可编辑的 Markdown 接口，不引入解析器或自动化依赖。
- Verification: 当前规划文档已归档到 `Archive/docs-before-weekly-report-workflow-*`，并在根文档中记录本功能范围。

### Milestone 2: Domain or Interface Change

- 定义工作项的稳定接口：目标、变化、证据、状态、影响、阻碍/请求、下一步。
- 将工作项按实验、工程、阅读、写作、协作五类适配为重点页；共享的汇报操作保持不变：筛选重点 → 给出证据 → 明确结论 → 请求决策。
- Verification: 输入清单和 Beamer 模板使用同一组字段，且正文骨架不依赖某一具体工作类型。

### Milestone 3: End-to-End Feature Workflow

- 新增独立的 `weekly-report/` 目录，其中的 `weekly-input.md` 用于日常记录和汇报前筛选。
- 在该目录中新增 `main.tex` 与本地 `latexmkrc`；前者提供面向周报的独立可编译内容模板，后者复用项目根目录的构建配置。
- 更新 README 和文件结构文档，说明从输入清单到 PDF 的流程与编译命令。
- Verification: `latexmk -jobname=weekly-report main.tex` 已成功生成 10 页 PDF；检查结果为 0 个 overfull 和 0 个未定义控制序列，页面包含概览、两项重点工作、讨论、下周计划和附录。

### Milestone 4: Regression Check and Demo

- 从 `weekly-report/` 编译 `main.tex`，检查错误和 overfull 警告。
- 回归编译 `main.tex` 与 `main-groupmeeting.tex`，确认公共样式和现有预设未受影响。
- 验证四项抽象检查：输入字段是否足以支持页面选择、是否能仅由字段完成周报、结构是否在无结果周保持稳定、下周是否能回查上周承诺。

**验证结果：**

- `weekly-report/main.tex`、根目录 `main.tex` 与 `main-groupmeeting.tex` 均已由 latexmk 成功编译。
- 周报 PDF 已渲染检查封面、概览、重点进展、讨论与附录页面；页码显示正文 `X / 8`、附录 `A-1`。
- 输入清单的七字段足以确定页面内容；只有 1 个重点时可删除第二重点帧；无结果周仍可用“仍不确定 / 阻碍与请求”表达；下周计划显式要求可检查证据。

### Later

- 可选地增加脚本，将一份结构化 YAML/Markdown 输入生成 LaTeX 草稿。
- 提供用于实验、代码、论文阅读的附录卡片宏。
- 增加按周创建、归档和清理历史报告的命令行辅助工具。
<!-- feature:weekly-report-workflow:end -->

<!-- feature:weekly-report-framework:start -->
## Feature Flow: weekly-report-framework

### Milestone 1: Current State and Route Fit

- 已确认现有 `weekly-report/` 仍要求用户把 `weekly-input.md` 的内容手工同步到 `main.tex`；根目录的 `latexmk`、视觉接口与周报独立目录均已稳定可用。
- 选择本地 Python + YAML：YAML 适合高频编辑、PyYAML 已在本机可用，生成的 TeX 继续交给 XeLaTeX/latexmk，不引入第二套排版系统。
- Verification: 当前四份根文档已归档到 `Archive/docs-before-weekly-report-framework-*`，本功能的接口和边界已记录。

### Milestone 2: Domain or Interface Change

- 定义 `report.yaml` 接口：`week`、`work_items`、`next_week`、`appendix`；每个工作项共享目标、变化、证据、状态、影响、阻碍/请求和下一步，另以 `type` 指定适配器。
- 定义输入安全边界：普通文本自动 LaTeX 转义；图片必须位于 `img/`、使用 PNG/JPG/JPEG/PDF 且真实存在；重点项最多两个。
- Verification: 用示例 YAML 覆盖实验、工程、阅读、写作和协作类型，并确保渲染器只依赖该接口。

### Milestone 3: End-to-End Feature Workflow

- 新增 `scripts/render_report.py`，负责加载、校验、转义和生成 TeX 片段；不直接改写 `main.tex`。
- 将 `main.tex` 收敛为稳定外壳，并用 `\input` 加载生成的元信息与页面内容。
- 增加 `Makefile`、`requirements.txt` 和目录级 `.gitignore`，使 `make check`、`make report` 与生成物管理可重复。
- 更新 `README.md`、`weekly-input.md` 与示例 `report.yaml`，将手工流程切换为数据驱动流程。
- Verification: 从 YAML 生成 TeX、编译 PDF、检查文本转义与图片校验失败路径。

### Milestone 4: Regression Check and Demo

- 验证 `make check` 与 `make report`；检查生成的 `.tex` 中的重点页类型、图片路径与页码。
- 使用带 `%`、`_`、`&` 的文本和带图片的样例验证转义和图片插入；用非法图片路径验证错误信息。
- 回归编译根目录 `main.tex`、`main-groupmeeting.tex`，确认 `bibresource` 接口与视觉档案的默认行为未改变。

**验证结果：**

- `make check` 通过：5 个工作项、2 个重点、1 个附录项。
- `make test` 通过 7 项测试，覆盖特殊字符转义、五种适配器、缺失字段、重点数量、未知类型、目录逃逸、不存在图片与合法图片渲染。
- `make report` 成功生成 10 页 `weekly-report.pdf`；日志中 0 个 overfull、0 个未定义控制序列。
- PDF 已渲染检查封面 Logo、概览表、图片型重点页、讨论页和附录页；正文页码为 `X / 8`，附录为 `A-1`。
- 根目录 `main.tex` 与 `main-groupmeeting.tex` 均由 latexmk 成功回归编译。

### Later

- 从外部任务系统、Git 提交或文献笔记预填 YAML 草稿。
- 提供图表数据到 PDF/SVG 的自动制图适配器。
- 增加历史周报索引和跨周进度对比。
<!-- feature:weekly-report-framework:end -->
