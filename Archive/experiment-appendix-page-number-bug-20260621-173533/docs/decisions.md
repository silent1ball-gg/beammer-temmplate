# Decisions

## Long-Term Maintainable Technical Route

- 不引入新宏包，仅利用 Beamer 内置的 `\AtBeginDocument` + `\apptocmd` 机制。
- 修复与现有 XeLaTeX + Beamer (metropolis) + latexmk 路线完全兼容。

## Initial Choices

### 根因调查路线

采用**逐层隔离法**：
1. 最小测试文件 → 确认 bug 存在
2. 移除 `\section` → 排除 `\AtBeginSection` 嫌疑
3. 使用最简 footline → 排除 `\ifbeamer@inappendix` 嫌疑
4. 替换主题 → **确认 metropolis 为元凶**
5. 阅读 metropolis 源码 → **定位 `\apptocmd{\appendix}` 钩子**

### 修复策略

**推荐方案**：`\AtBeginDocument` + `\apptocmd{\appendix}` 重新设置 footline。

选择理由：
- 利用 `\AtBeginDocument` 执行顺序：我们的 `.sty` 后加载 → 我们的 `\AtBeginDocument` 后执行 → 我们的 `\apptocmd` 后追加 → 后执行 → 覆盖 metropolis 修改
- 零侵入：不修改 metropolis 源码，不引入新宏包
- 对正文无影响：`\appendix` 钩子仅在附录切换时触发

**已排除方案**：
- 覆盖 `frame numbering` 内部宏 → Beamer 模板系统内部行为不明确，覆盖不生效
- 覆盖 `footline` `plain` 内部宏 → 同上，覆盖不生效
- 直接 `\setbeamertemplate{footline}` → 被 metropolis 覆盖

### 最终选择

**pgfkey 中性化**：清空 `numbering=none` 和 `progressbar=none` 的 `.code` handler。

成功原因：
- metropolis 的 `\appendix` 钩子通过 pgfkey 机制修改 footline
- 清空 handler → 钩子变成空操作 → footline 不受影响
- 比 `\apptocmd` 方案简单直接，不依赖执行顺序

`\apptocmd` 方案失败原因（已排除）：
- Beamer 模板系统：`\setbeamertemplate{footline}[plain]` 的作用方式导致后续的 `\setbeamertemplate{footline}{...}` 无法在附录帧生效

## Open Questions

- 为什么 `\expandafter\def\csname beamer@@tmpop@footline@plain\endcsname` 只渲染 1 次？Beamer 模板系统的缓存机制待深入研究。
- 是否所有版本的 metropolis 都有此行为？（当前版本：TeX Live 2026）

## Constraints

- 平台约束：不变（macOS，XeLaTeX）。
- 依赖约束：零新增依赖。
