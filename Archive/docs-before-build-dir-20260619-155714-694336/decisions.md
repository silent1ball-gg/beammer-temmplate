# Decisions

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
- **单主题**：MVP 仅提供一套 metropolis 主题配色，多主题切换尚未实现。
- **无代码高亮**：暂未集成 `minted` 或 `listings` 宏包，代码展示需用户自行添加。
- **无暗色主题**：仅提供亮色（白底）版本，暗色背景待后续添加。
