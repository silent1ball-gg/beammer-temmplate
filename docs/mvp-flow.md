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
