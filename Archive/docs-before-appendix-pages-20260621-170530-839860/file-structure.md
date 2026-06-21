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

- `main-groupmeeting.tex`：组会汇报预设场景的主文件。与 `main.tex` 完全对等的关系——两个独立的内容模板，共享同一个 `beamer-style.sty` 样式。提供组会专用幻灯片结构：标题页（含导师/课题组信息）、本周工作概览、详细进展、问题讨论（alertblock/exampleblock）、下周计划、致谢 & Q&A。文件内附详细的 LaTeX 注释，标注用户可修改的元数据和内容区域。
- `README.md`：新增「预设场景」小节，用对比表格展示两种模板的适用场景、幻灯片结构差异、选择建议。更新文件说明表增加 `main-groupmeeting.tex` 条目。
<!-- feature:groupmeeting-preset:end -->
