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
