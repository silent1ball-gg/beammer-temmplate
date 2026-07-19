# File Structure

## Proposed Tree

> ✅ 以下为项目当前实际文件树（与 MVP 计划一致）。

```text
beamer-template/
├── README.md                  # 项目入口：依赖、编译、自定义、FAQ
├── main.tex                   # 主模板文件，用户在此填写演示内容
├── beamer-style.sty           # 样式配置：主题、CJK字体、颜色、页脚、参考文献
├── refs.bib                   # BibTeX 参考文献示例文件
├── latexmkrc                  # latexmk 编译配置（xelatex 引擎）
├── .gitignore                 # Git 忽略规则（编译产物 + .DS_Store）
├── img/                       # 图片资源目录（用户自行添加图片）
├── docs/
│   ├── goal.md                # 目标与范围定义
│   ├── mvp-flow.md            # MVP 里程碑计划
│   ├── file-structure.md      # 本文档（文件结构说明）
│   └── decisions.md           # 技术决策与已知限制
├── Archive/                   # 历史归档（旧版本文档、被替换方案）
└── experiments/               # 实验性功能隔离工作区
```

## Path Responsibilities

- `README.md`：项目入口文档。覆盖依赖安装（MacTeX）、编译命令（`latexmk`）、自定义方法（内容、样式、图片、参考文献）、常见问题。
- `main.tex`：用户操作的主文件。17 帧学术答辩模板，包含标题页（含导师/答辩委员会）、目录、研究背景、相关工作、研究方法（架构 + 技术选型表）、实验结果（含图表帧）、总结与展望、致谢、参考文献。各 Section 均附注释标注可修改点。
- `beamer-style.sty`：所有外观配置集中在此。包括：
  - `\usetheme{metropolis}` — Beamer 主题
  - `xeCJK` + PingFang SC — 中文字体配置
  - `biblatex` (biber, numeric) — 参考文献引擎
  - `booktabs` — 专业表格
  - 自定义颜色主题（学术蓝 #005A9C）
  - 自定义页脚页码模板
  - 图表编号、参考文献样式、目录格式
- `refs.bib`：BibTeX 格式的参考文献示例条目（article + book），供 `\cite` 和 `\printbibliography` 使用。
- `latexmkrc`：latexmk 配置文件。指定 `pdf_mode=5` (xelatex)、自定义清理扩展名列表。
- `.gitignore`：忽略 LaTeX 编译产物（`.aux`、`.log`、`.out`、`*.pdf` 等）和 `.DS_Store`。
- `img/`：用户存放图片的目录。模板中使用 `mwe` 包的 `example-image` 作为占位图，用户替换为实际图片。
- `docs/goal.md`：项目目标、用户分析、MVP 定义、假设、非目标、目标用户、成功标准。
- `docs/mvp-flow.md`：四大里程碑从项目基础到验证收尾的完整步骤。
- `docs/file-structure.md`：本文档。
- `docs/decisions.md`：技术路线、初始选择（编译器、主题、字体、参考文献引擎）、开放问题、约束、已知限制。
- `Archive/`：历史归档目录，存放被替换的旧版本文档和设计方案。
- `experiments/`：实验性功能隔离工作区，每个实验有独立的 `docs/` 和 `Archive/`。

<!-- feature:build-dir:start -->
## Feature Structure Update: build-dir

### Current Structure Impact

- `latexmkrc`：新增 1 行配置（`$aux_dir`）。
- `.gitignore`：从逐个文件忽略简化为 `build/` 目录忽略。
- `README.md`：文件结构图中增加 `build/` 目录说明。
- 无需新建任何源代码文件。

### Proposed Changes

```text
beamer-template/
...
├── build/                    ← NEW: 所有编译中间产物（.aux, .log, .toc, ...）
├── latexmkrc                 ← MODIFIED: 新增 $aux_dir = 'build';
├── .gitignore                ← MODIFIED: 简化为忽略 build/ + *.pdf
...
```

### Path Responsibilities

- `build/`：latexmk 生成的编译中间产物目录。由 `latexmkrc` 中的 `$aux_dir` 配置自动创建和管理。git 已忽略。
- `latexmkrc`：新增 `$aux_dir = 'build';`，将中间文件重定向至此目录，PDF 保留在根目录。
- `.gitignore`：简化规则，只需忽略 `build/` 和 `*.pdf`，不再逐个列举 `.aux`、`.log` 等扩展名。
<!-- feature:build-dir:end -->

<!-- feature:groupmeeting-preset:start -->
## Feature Structure Update: groupmeeting-preset

### Current Structure Impact

- 不修改现有文件：`main.tex`、`beamer-style.sty`、`latexmkrc`、`refs.bib` 均保持不变。
- 不影响现有构建流程和样式系统。
- `README.md` 需要更新，增加组会模板说明。
- `main-groupmeeting.pdf` 需要加入 `.gitignore`（如尚未被 `*.pdf` 规则覆盖）。

### Proposed Changes

```text
beamer-template/
├── main.tex                   ← 不变：学术答辩预设场景
├── main-groupmeeting.tex      ← NEW：组会汇报预设场景
├── beamer-style.sty           ← 不变：两种场景共用样式
├── refs.bib                   ← 不变：参考文献库（共用）
├── README.md                  ← MODIFIED：新增预设场景说明
...
```

### Path Responsibilities

- `main-groupmeeting.tex`：组会汇报预设场景的主文件。与 `main.tex` 完全对等的关系——两个独立的内容模板，共享同一个 `beamer-style.sty` 样式。提供组会专用幻灯片结构：标题页（含 Logo + 导师/课题组信息）→ 问题背景 → 本周工作概览 → 详细进展（数据预处理 + 基线实验）→ 结果展示（图表 + 分析表格）→ 问题讨论（alertblock/exampleblock）→ 下周计划 → 致谢 & Q&A → 附录。文件内附详细的 LaTeX 注释，标注用户可修改的元数据和内容区域。
- `README.md`：新增「预设场景」小节，用对比表格展示两种模板的适用场景、幻灯片结构差异、选择建议。更新文件说明表增加 `main-groupmeeting.tex` 条目。
<!-- feature:groupmeeting-preset:end -->

<!-- feature:appendix-pages:start -->
## Feature Structure Update: appendix-pages

### Current Structure Impact

- 修改 `beamer-style.sty`：footline 模板从 `\inserttotalframenumber` 改为 `\insertmainframenumber` + `\ifnum` 附录判断（约 6 行改动）。
- 修改 `main.tex`：`\end{document}` 前新增 `\appendix` + 示例帧（约 20 行）。
- 修改 `main-groupmeeting.tex`：`\end{document}` 前新增 `\appendix` + 示例帧（约 20 行）。
- `README.md` 更新：特性列表、自定义指南、FAQ。
- 不修改 `latexmkrc`、`refs.bib`、`.gitignore`。

### Proposed Changes

```text
beamer-template/
├── main.tex                   ← MODIFIED: 新增 \appendix + 附录帧
├── main-groupmeeting.tex      ← MODIFIED: 新增 \appendix + 附录帧
├── beamer-style.sty           ← MODIFIED: footline 页码逻辑（\insertmainframenumber + \ifnum）
├── README.md                  ← MODIFIED: 说明附录功能
...
```

### Path Responsibilities

- `beamer-style.sty` 修改：footline 模板用 `\ifnum\insertframenumber>\insertmainframenumber` 判断附录区域，正文显示 "X/Y"，附录显示 "A-Z"。
- `main.tex` 新增：`\appendix` + 一个示例附录帧，位于参考文献之后、`\end{document}` 之前。
- `main-groupmeeting.tex` 新增：`\appendix` + 一个示例附录帧，位于致谢之后、`\end{document}` 之前。原注释的参考文献帧保留在附录帧之后。
- `README.md`：特性列表新增附录条目；自定义指南新增「使用附录」小节；FAQ 新增附录页码问答。
<!-- feature:appendix-pages:end -->

<!-- feature:cover-logo:start -->
## Feature Structure Update: cover-logo

### Current Structure Impact

- 修改 `main.tex`：标题帧 `\begin{frame}` 后新增 tikz logo 代码块（6 行）。
- 修改 `main-groupmeeting.tex`：同上。
- 不修改 `beamer-style.sty`、`latexmkrc`、`refs.bib`。

### Proposed Changes

```text
beamer-template/
├── main.tex                   ← MODIFIED: 标题帧新增右上角 Logo
├── main-groupmeeting.tex      ← MODIFIED: 标题帧新增右上角 Logo
├── img/logo.png               ← NEW: 用户提供的 Logo 文件
...
```

### Path Responsibilities

- `main.tex` / `main-groupmeeting.tex`：标题帧内通过 `tikz` 的 `remember picture, overlay` 将 `img/logo.png` 定位在封面右上角。用户修改 `xshift`/`yshift` 调整位置，修改 `height` 调整大小。
- `img/logo.png`：用户自行放置的 Logo 图片文件。
<!-- feature:cover-logo:end -->

<!-- feature:groupmeeting-enhance:start -->
## Feature Structure Update: groupmeeting-enhance

### Current Structure Impact

- 修改 `main-groupmeeting.tex`：新增 3 帧（问题背景 + 结果展示 + 结果分析），约 50 行。更新全部 section 编号注释。
- 不修改其他文件。

### Proposed Changes

```text
beamer-template/
├── main-groupmeeting.tex      ← MODIFIED: 新增 问题背景、结果展示、结果分析 帧
...
```

### Path Responsibilities

- `main-groupmeeting.tex` 新增帧：
  - **问题背景**（Section 2）：研究课题、核心问题、应用场景、当前瓶颈、本文思路。帮助听众快速理解研究上下文。
  - **结果展示**（Section 5）：图表占位帧（`example-image` + caption），替换为实际实验结果图。
  - **结果分析**（Section 5）：性能对比表格（`booktabs` 三线表），含基线模型与改进方案对比示例。
- 组会幻灯片结构更新为 10 个 section：标题页 → 问题背景 → 本周概览 → 进展详情 → 结果展示 → 文献阅读（可选）→ 问题讨论 → 下周计划 → 致谢 → 附录。
<!-- feature:groupmeeting-enhance:end -->

<!-- feature:multi-design-interface:start -->
## Feature Structure Update: multi-design-interface

```text
beamer-template/
├── beamer-style.sty            ← 公共视觉接口与跨设计能力
├── beamer-design-academic.sty  ← 默认学术蓝档案
├── beamer-design-classic.sty   ← 正式经典档案
└── beamer-design-midnight.sty  ← 深色技术档案
```

- `beamer-style.sty`：解析 `design=<name>`，载入档案，并提供各设计共用的字体、引用和页码行为。
- `beamer-design-*.sty`：每个档案只实现主题和视觉 token；不得包含用户内容或编译流程逻辑。
- `main.tex`、`main-groupmeeting.tex`：显式选择 `design=academic`，用户可替换为其他已提供的设计名。
- `tests/design-smoke.tex`：用同一组标题、中文、block、附录内容回归验证每个设计档案。
<!-- feature:multi-design-interface:end -->

<!-- feature:weekly-report-workflow:start -->
## Feature Structure Update: weekly-report-workflow

### Current Structure Impact

- 不修改视觉接口：`beamer-style.sty` 和 `beamer-design-*.sty` 保持不变。
- 新增一份 Markdown 输入接口和一份独立的 Beamer 内容模板；`main-groupmeeting.tex` 继续作为带完整示例的组会预设。
- `README.md` 更新为三个内容入口：答辩、组会示例、可复用周报工作流。

### Proposed Changes

```text
beamer-template/
├── weekly-report/             ← NEW：与根目录模板隔离的周报工作区
│   ├── README.md               ← 周报工作流与编译说明
│   ├── weekly-input.md         ← 每周记录与汇报前筛选的输入清单
│   ├── main.tex                ← 可复制、可编译的周报内容模板
│   ├── latexmkrc               ← 复用根目录构建配置
│   └── img/                    ← 周报专用图片资源
├── beamer-style.sty            ← MODIFIED：支持指定共享文献库路径
└── docs/
    ├── goal.md                ← MODIFIED：功能目标与验收标准
    ├── mvp-flow.md            ← MODIFIED：实施和验证流程
    ├── file-structure.md      ← MODIFIED：本功能的路径边界
    └── decisions.md           ← MODIFIED：技术和兼容性决策
```

### Path Responsibilities

- `weekly-report/weekly-input.md`：用户每周复制的工作项收集表。它是周报的语义接口，而非程序必须解析的数据格式。
- `weekly-report/main.tex`：周报的呈现层。它只承载元数据和幻灯片内容，并通过父目录的 `beamer-style.sty` 选择既有设计。
- `weekly-report/latexmkrc`：加载父目录的构建配置，以便从周报目录直接编译、并将中间产物留在本目录的 `build/` 中。
- `weekly-report/README.md`：将输入清单、页面骨架、类型适配规则和 `latexmk` 命令连接为一条可执行工作流。
- `docs/*.md`：记录此功能的范围、技术边界与验证策略；归档前快照保留在 `Archive/`。
<!-- feature:weekly-report-workflow:end -->

<!-- feature:weekly-report-framework:start -->
## Feature Structure Update: weekly-report-framework

### Current Structure Impact

- `weekly-report/` 从“输入清单 + 每周手改 LaTeX”升级为数据驱动子系统；根目录模板、样式与设计档案不承载周报业务逻辑。
- `main.tex` 保留为稳定渲染外壳，`report.yaml` 成为每周唯一的手工内容输入；生成的 TeX 不提交、不手改。

### Proposed Changes

```text
weekly-report/
├── report.yaml                 ← NEW：每周唯一的结构化输入
├── main.tex                    ← MODIFIED：稳定 Beamer 外壳，加载 generated/ 内容
├── Makefile                    ← NEW：make check / make report
├── requirements.txt            ← NEW：渲染器的 PyYAML 依赖声明
├── weekly-input.md             ← MODIFIED：YAML 字段字典与填写指南
├── README.md                   ← MODIFIED：数据驱动周报的使用说明
├── scripts/
│   └── render_report.py        ← NEW：校验 YAML 并生成 TeX
├── tests/
│   └── test_render_report.py   ← NEW：接口、转义、适配器和失败路径测试
├── generated/
│   └── .gitignore              ← NEW：保留目录，忽略生成的 TeX
└── img/                        ← 周报图片；YAML 仅可引用此目录中的文件
```

### Path Responsibilities

- `report.yaml`：汇报内容的唯一事实源，包含字段值与图片引用；用户每周只编辑此文件和 `img/`。
- `scripts/render_report.py`：把受限数据接口重建为 `preamble.tex` 与 `content.tex`；负责校验和 LaTeX 特殊字符转义。
- `main.tex`：不含周度内容，只声明 Beamer 公共样式并加载 `generated/` 文件。
- `Makefile`：提供一条从数据到 PDF 的可重复命令；`generated/`：渲染产物，不应手改。
- `tests/test_render_report.py`：验证五种类型适配、文本转义、字段约束和图片路径边界。
- `weekly-input.md` / `README.md`：面向人的字段解释、类型适配规则与工作流说明。
<!-- feature:weekly-report-framework:end -->
