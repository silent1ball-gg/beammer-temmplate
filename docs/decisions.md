# Decisions

## Decision: appendix does not create its own title page

The weekly-report renderer uses `\\appendix` without `\\section{附录}`. In the academic Beamer design, the latter created an extra content-free title page, while the former preserves appendix numbering and makes every appendix page correspond to actual content. Validated by the end-to-end PDF review on 2026-07-19.

## Long-Term Maintainable Technical Route

**路线：LaTeX Beamer 文档类 + XeLaTeX 编译器 + latexmk 构建，样式与内容分离（`.sty` + `.tex`）。**

选择理由：
- LaTeX Beamer 是学术界和工业界制作演示文稿的事实标准，生态成熟，社区活跃，不会过时。
- XeLaTeX 原生支持 Unicode 和系统字体，比 pdfLaTeX 的中文方案（CJK 宏包）简单可靠；比 LuaLaTeX 编译更快，生态兼容性更好。
- latexmk 是 TeX Live 自带的自动化构建工具，自动处理多次编译（解决交叉引用、目录生成等），无需手写 Makefile。
- `.sty` 样式分离让用户专注内容，模板维护者可以独立升级样式而不影响用户内容。

这条路线从单文件 MVP 到多模板、多主题的完整产品都能支撑，无需推倒重来。

## Initial Choices

| 选择项 | 决定 | 备选方案与说明 |
|--------|------|---------------|
| TeX 编译器 | **XeLaTeX** | LuaLaTeX 更现代但编译略慢；pdfLaTeX 中文支持繁琐。XeLaTeX 是当前中文 LaTeX 的最佳平衡点。 |
| 构建工具 | **latexmk** | Makefile 跨平台差；`arara` 需额外安装。latexmk 随 TeX Live 分发，零额外依赖。 |
| Beamer 主题基础 | **metropolis** | 简洁现代风格，学术/技术场景通用。备选：Madrid（传统）、CambridgeUS。如用户偏好其他，可在 `.sty` 中一行切换。 |
| 中文字体 | **系统苹方 (PingFang)** | macOS 自带，无需额外安装，渲染质量好。若需跨平台，可配置为思源字体 (Noto Serif/Sans CJK)。 |
| 英文主字体 | **Fira Sans** | 搭配 metropolis 主题的原生字体，现代无衬线风格，适合演示文稿。 |
| 参考文献引擎 | **biber + biblatex** | 比传统 BibTeX 更灵活，原生支持 Unicode，与 XeLaTeX 配合更好。 |
| 屏幕比例 | **16:9 (`aspectratio=169`)** | 现代显示器和投影仪的默认比例。在 `.sty` 中配置，用户可改为 4:3。 |

## Open Questions

- 用户是否有特定的 LaTeX 发行版偏好？MacTeX 是 macOS 的默认选择，但需确认是否已安装。
- 是否需要英文模板同步提供？MVP 先支持中文，英文内容在同样式下自然可用。
- 是否需要暗色背景主题？MVP 先做亮色（白底）主题，后续可作为主题变体。
- 用户的目标使用场景是学术答辩、技术分享还是通用演示？影响示例内容的方向。
学术答辩

## Constraints

- **平台约束**：macOS 优先。Windows/Linux 用户需自行调整字体路径，但 `.sty` 和 `.tex` 核心逻辑跨平台兼容。
- **时间约束**：MVP 应在一个会话内完成基础骨架搭建。
- **依赖约束**：零运行时依赖（PDF 查看器除外）。编译依赖仅限于 TeX Live/MacTeX 标准安装。
- **分发约束**：项目以 Git 仓库形式分发，不发布到 CTAN。

## Known Limitations (MVP)

- **Fira Sans 未生效**：macOS 的 XeTeX 引擎无法通过字体族名找到 TeX Live 中的 Fira Sans 字体文件。metropolis 主题回退到默认的 Latin Modern Sans。视觉效果可接受，如需修复，需在 `beamer-style.sty` 中用 `Extension=.otf` + `UprightFont=*-Regular` 的文件名方式显式指定。
- **仅支持 XeLaTeX**：模板依赖 `xeCJK` 宏包处理中文，该宏包仅适用于 XeLaTeX。pdfLaTeX 需要 CJK 宏包方案（完全不同），LuaLaTeX 理论上可用但未经测试。
- **中文字体绑定 macOS**：默认使用 PingFang SC（苹方-简），其他平台需手动替换字体配置。
- **单主题配色**：仅提供一套学术蓝 metropolis 主题配色，多套颜色主题切换尚未实现。
- **预设场景有限**：当前提供「学术答辩」和「组会汇报」2 种预设场景，「技术分享」等场景待后续添加。
- **无代码高亮**：暂未集成 `minted` 或 `listings` 宏包，代码展示需用户自行添加。
- **无暗色主题**：仅提供亮色（白底）版本，暗色背景待后续添加。

<!-- feature:build-dir:start -->
## Feature Decision: build-dir

### Long-Term Route Fit

- latexmk 是构建工具，内置 `$aux_dir` 支持，无需引入新工具。该功能是 latexmk 原生能力的合理运用，与当前技术路线完全一致。

### Chosen Approach

- **`$aux_dir = 'build'`**（非 `$out_dir`）：仅重定向中间文件，PDF 保留在根目录方便用户直接打开。
- 备选方案 `$out_dir = 'build'` 会将 PDF 也放入 `build/`，增加用户访问路径，不采用。

### Compatibility and Migration

- **向后兼容**：用户编译命令 `latexmk`、`latexmk -c`、`latexmk -C` 行为不变。
- **`.gitignore` 简化**：删除逐个中间文件扩展名列表，统一为 `build/`。旧用户如切换到此版本，需清理一次已有中间文件。
- **无数据迁移**：不涉及任何 `.tex` 或 `.sty` 源码修改。

### Open Questions

- 无。`$aux_dir` 是 latexmk 的标准功能，XeLaTeX 通过 `-aux-directory` 原生支持。

### Constraints

- **XeLaTeX 版本**：`-aux-directory` 选项在较新版本 XeTeX 中支持良好（TeX Live 2020+）。当前环境 TeX Live 2026 无问题。
<!-- feature:build-dir:end -->

<!-- feature:groupmeeting-preset:start -->
## Feature Decision: groupmeeting-preset

### Long-Term Route Fit

- 当前技术路线核心是**样式与内容分离**（`.sty` + `.tex`）。本 feature 在「内容层」新增一个 `.tex` 文件，样式层（`beamer-style.sty`）完全复用，不改变也不依赖样式的任何修改。
- 未来可能发展出更多预设场景（技术分享、论文汇报、学术报告等），扩展模式清晰：每个场景一个 `.tex` 内容文件 + 一个共用 `.sty` 样式文件。这条模式从 1 个场景到 N 个场景都无需推倒重来。
- 不在此 feature 中引入宏集抽象或条件编译：当前仅 2 个场景，过度抽象（如提取 `beamer-base.tex` 或 `\newcommand` 宏集）会增加维护成本和用户理解难度。等场景数量 ≥ 4 且代码重复明显时再考虑提炼。

### Chosen Approach

- **方案：独立的 `main-groupmeeting.tex` 文件**，直接 `\usepackage{beamer-style}`，与 `main.tex` 平级且对等。
- **备选方案 A**：参数化单文件（通过 `\input{scenario-config.tex}` 切换幻灯片结构）→ 过度工程，用户需要在多个文件间跳转才能理解模板逻辑，且 LaTeX 社区不习惯这种「配置文件」模式。
- **备选方案 B**：将共同结构（documentclass、usepackage、元数据模式）提取为 `beamer-base.tex`，两种场景各自 `\input{beamer-base}` → 虽然符合 DRY 原则，但当前两个文件的共同部分不到 30 行，提取带来的间接性代价大于重复代码的维护成本。
- **备选方案 C**：通过 `\mode<presentation>` 或 `\ifdefined` 条件编译在同一文件中切换场景 → 用户需要修改非直观的 LaTeX 命令，学习成本高，不符合模板「开箱即用」的目标。
- **选择依据**：保持简单、直白。每个预设场景一个独立、自包含的 `.tex` 文件，用户复制后即可开始编辑。这是 LaTeX 模板领域的主流做法（如各大高校学位论文模板库：`main-master.tex`、`main-phd.tex` 各自独立）。独立文件还有额外好处：用户可以同时拥有两份不同的演示文稿（同一项目中），互不干扰。

### Compatibility and Migration

- **向后兼容**：不修改 `main.tex`、`beamer-style.sty`、`latexmkrc`、`refs.bib`，现有用户完全不受影响。
- **无迁移成本**：现有用户无需任何操作即可 `git pull` 升级。组会模板作为新增文件出现，不会产生合并冲突。
- **latexmk 编译方式**：`latexmk` 默认查找并编译 `main.tex`。编译组会模板需使用 `latexmk -jobname=main-groupmeeting main-groupmeeting.tex`，避免 PDF 被命名为 `main.pdf` 而覆盖。README 中将说明两种编译方式。VS Code LaTeX Workshop 用户打开 `main-groupmeeting.tex` 后保存即可自动编译，无需特殊配置。
- **`.gitignore`**：现有 `*.pdf` 规则已忽略所有 PDF 文件，无需修改。

### Open Questions

- **是否需要单独的 `refs-groupmeeting.bib`？** → MVP 不需要。组会汇报通常文献引用量少，可直接共用 `refs.bib`。如用户需要独立文献库，可自行创建并在 `main-groupmeeting.tex` 中的 `\addbibresource` 修改引用路径。
- **是否需要提供「空白模板」版本？** → 当前不提供。两种预设场景本身即接近空白（用户替换内容即可），再提供空白版本意义不大。如用户反馈有需求，后续在 Later 中加入 `main-blank.tex`。

### Constraints

- **平台约束**：不变（macOS 优先，中文字体绑定 PingFang SC）。
- **编译约束**：需要用户使用 `-jobname` 参数或通过 LaTeX Workshop 默认行为编译非 `main.tex` 文件。已在 README 中说明。
- **依赖约束**：零新增宏包依赖，复用现有 `beamer-style.sty` 的全部依赖。
- **质量约束**：组会模板的注释密度和详细程度需与 `main.tex` 保持一致（每帧都有注释，元数据区有说明），不应成为「二等公民」。
<!-- feature:groupmeeting-preset:end -->

<!-- feature:appendix-pages:start -->
## Feature Decision: appendix-pages

### Long-Term Route Fit

- `\appendix` 是 Beamer 内核命令，`\insertmainframenumber` 是 Beamer 内置计数器，不引入新宏包、新工具，与现有 XeLaTeX + Beamer (metropolis) + latexmk 路线完全一致。

### Chosen Approach

**三层设计**：

1. **pgfkey 中性化**（`beamer-style.sty`）：清空 metropolis 的两个 pgfkey handler：
   ```latex
   \pgfkeys{
     /metropolis/outer/numbering/none/.code={},
     /metropolis/outer/progressbar/none/.code={},
   }
   ```
   metropolis 在 `\appendix` 时通过 `\apptocmd{\appendix}` 触发 `\pgfkeys{numbering=none, progressbar=none}`——原本会清空帧号并重置 footline 为 `[plain]` 变体。清空 handler 后，这些操作变成空操作，用户 footline 不受影响。

2. **页码切换**（footline 模板）：使用 Beamer 内置的 `\ifbeamer@inappendix` + `\insertframenumberinappendix`（而非手动 `\ifnum` 判断）。
   - 正文：`\insertframenumber / \insertmainframenumber` → "X / Y"
   - 附录：`A-\insertframenumberinappendix` → "A-1, A-2, ..."

3. **保留 `\section{附录}`**：生成标题帧作为附录入口（页码 A-1），后续内容帧为 A-2, A-3...。

**探索过的方案及排除原因**：
- `\apptocmd{\appendix}` 重新设置 footline → ❌ 附录帧 footline 仍不渲染（Beamer 模板系统内部机制）
- 覆盖 `\beamer@@tmpop@footline@plain` 内部宏 → ❌ 只渲染 1 次
- 覆盖 `\beamer@@tmpop@frame numbering@none` 内部宏 → ❌ 只渲染 1 次
- `\ifnum\insertframenumber>\insertmainframenumber` → ❌ 比较逻辑在边缘情况不可靠
- `appendixnumberbeamer` 宏包 → ❌ 需新增依赖，且不带 "A-" 前缀

详见 `experiments/appendix-page-number-bug/docs/`。

### Compatibility and Migration

- **向后兼容**：pgfkey 中性化 + footline 模板仅影响外观，不修改 `.tex` 内容文件。正文帧页码保持 "X/Y" 不变。
- **无迁移成本**：用户 `git pull` 后即可使用，编译命令不变。

### Open Questions

- **附录是否需要独立的页码样式（如 "A-1, A-2"）？** → ✅ 已实现。通过 `\ifbeamer@inappendix` 自动切换。
- **是否需要「谢谢」页与附录之间的分隔页？** → 不添加。居中「谢谢！」帧 + `\section{附录}` 标题帧已形成自然视觉分隔。

### Constraints

- **依赖约束**：零新增依赖。`\ifbeamer@inappendix`、`\insertframenumberinappendix`、`\pgfkeys` 均为 Beamer/pgf 内核。
- **质量约束**：两个模板的附录帧注释密度与现有帧保持一致。
<!-- feature:appendix-pages:end -->

<!-- feature:multi-design-interface:start -->
## Feature Decision: multi-design-interface

### Chosen Interface

内容模板通过一项稳定声明选择视觉实现：

```latex
\usepackage[design=academic]{beamer-style}
```

`beamer-style.sty` 是公共接口层，保留 XeLaTeX 检查、CJK 字体、`biblatex`、表格、附录页码和公共 Beamer 模板。每个 `beamer-design-<name>.sty` 档案只负责：基础 Beamer 主题、调色板、标题和 block 的视觉处理。

| 设计 | 基础主题 | 用途 |
|------|----------|------|
| `academic` | metropolis | 原有的默认学术蓝风格 |
| `classic` | Madrid | 更传统的正式/机构汇报 |
| `midnight` | metropolis | 深色高对比技术分享 |

### Preserved Invariants

- 同一份 `main.tex` 或 `main-groupmeeting.tex` 内容可在所有设计下编译。
- 字体、参考文献、附录页码、图片路径、`latexmk` 命令和 16:9 比例不因设计而改变。
- 设计档案不承载内容结构，也不改变用户数据（标题、作者、frame 内容）。

### Boundary

接口只保证上述公共能力和常见 Beamer 内容环境的兼容。某一设计专属的导航、色彩或布局细节不应被内容模板依赖；需要新增设计专属组件时，应先判断它是否应提升为公共接口。
<!-- feature:multi-design-interface:end -->

<!-- feature:weekly-report-workflow:start -->
## Feature Decision: weekly-report-workflow

### Long-Term Route Fit

- 继续采用「Markdown 记录接口 + 独立 `.tex` 内容模板 + 共用 `.sty` 样式接口」的本地、纯文本路线；它与现有 XeLaTeX + Beamer + latexmk 技术栈一致，并让内容演进不影响视觉层。
- 不引入 Markdown 转换器或数据库：周报的核心难点是筛选与叙事判断，而不是格式转换；先保留可读、可手工调整的输入与输出。

### Chosen Approach

- 在独立的 `weekly-report/` 目录中新增 `weekly-input.md` 作为任务相关接口，固定每项工作的七个字段：目标、变化、证据、状态、影响、阻碍/请求、下一步。
- 在该目录中新增 `main.tex` 作为重建层：封面/结论 → 概览 → 1--2 个重点 → 问题讨论 → 下周计划 → Q\&A → 附录。
- `beamer-style.sty` 增加可选的 `bibresource` 参数，因此独立周报目录能显式复用根目录的 `refs.bib`，而不复制或隐式查找文献库。
- 保留 `main-groupmeeting.tex` 的丰富示例；它适合学习和改写，周报模板则优先保证高频、低摩擦的重复使用。

### Compatibility and Migration

- 零迁移成本：现有 `main.tex`、`main-groupmeeting.tex`、视觉设计档案和编译命令均不改变。
- 新模板在 `weekly-report/` 中使用 `latexmk -jobname=weekly-report main.tex`，避免覆盖根目录的 PDF，也不会将周报源文件与根目录模板混放。
- 用户可复制整个 `weekly-report/` 目录或其中的 `main.tex`、`weekly-input.md` 留存；如果将其移出项目，需相应调整指向父目录样式和文献库的相对路径。

### Open Questions

- 无阻塞问题。后续如用户要求自动生成，再决定是否将输入清单升级为受约束的 YAML 格式。

### Constraints

- 一份周报默认面向 8--15 分钟汇报，正文宜控制在 7--9 页；细节放在附录。
- 输入清单仅保证决策相关信息被保留，不试图保留工作过程的全部细节。
- 本功能沿用项目的 XeLaTeX、中文字体和本地编译环境限制。
<!-- feature:weekly-report-workflow:end -->

<!-- feature:weekly-report-framework:start -->
## Feature Decision: weekly-report-framework

### Long-Term Route Fit

- 保持 XeLaTeX + Beamer + latexmk 的长期排版路线；仅在内容层加入一个小型、可审查的 Python 编译步骤。YAML 是源数据，TeX 是可再生的呈现中间产物。
- 不采用通用 Markdown→LaTeX 转换器或复杂模板引擎：周报的字段和布局是受限、稳定的，专用渲染器更容易验证、转义和维护。

### Chosen Approach

- 使用 Python 3 + PyYAML 的 `safe_load` 读取 `report.yaml`，将输入校验与渲染逻辑放在一个零网络、单文件脚本中。
- 渲染器按 `type` 使用五种适配器（experiment、engineering、reading、writing、coordination），但每种都重建为相同的“目标 → 变化/证据 → 影响 → 下一步”叙事接口。
- `main.tex` 通过 `\input{generated/preamble.tex}` 和 `\input{generated/content.tex}` 加载生成内容；`Makefile` 固定生成与编译顺序。

### Compatibility and Migration

- 既有 `weekly-input.md` 保留为字段说明，现有手工 `main.tex` 内容由新的稳定外壳替代；用户在升级后将当周内容填写进 `report.yaml`。
- `make report` 输出仍为 `weekly-report.pdf`，沿用本目录 `latexmkrc` 和父目录样式/参考文献路径；根目录命令与模板不变。
- 生成目录忽略 `*.tex`，避免用户意外提交或手改可再生产物。
- 渲染器只写入 `generated/preamble.tex` 与 `generated/content.tex`；测试使用 Python 标准库 `unittest`，不增加新的测试依赖。

### Open Questions

- 无阻塞问题。当前决定不支持 YAML 中的原始 LaTeX；若未来确有公式或复杂表格需求，再审慎增加显式、受限的富文本字段。

### Constraints

- 文本字段一律自动转义；这意味着 YAML 不能直接书写 LaTeX 命令。
- 图片路径必须相对 `weekly-report/` 并位于 `img/` 中；支持 png、jpg、jpeg、pdf。
- 重点工作项限制为 0--2 个，概览工作项限制为 1--5 个，以保护 8--15 分钟汇报的页面密度。
<!-- feature:weekly-report-framework:end -->
