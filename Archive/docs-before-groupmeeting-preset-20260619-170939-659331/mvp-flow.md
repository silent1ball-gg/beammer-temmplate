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
