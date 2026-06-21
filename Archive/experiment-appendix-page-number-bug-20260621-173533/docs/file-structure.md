# File Structure

## Proposed Tree

```text
appendix-page-number-bug/
├── docs/
│   ├── goal.md                  # 实验目标与成功标准
│   ├── mvp-flow.md              # 隔离测试 → 根因 → 修复方案
│   ├── file-structure.md        # 本文档
│   └── decisions.md             # 技术决策与排除方案
├── Archive/
├── latexmkrc                    # XeLaTeX 编译配置
├── test-minimal.tex             # 最小复现测试（metropolis + footline + appendix）
├── test-no-section.tex          # 隔离测试：去掉 \section 命令
├── test-plain-footline.tex      # 隔离测试：最简 footline（无条件判断）
├── test-no-metropolis.tex       # 隔离测试：替换为 Madrid 主题
├── test-diagnostic.tex          # 诊断测试：footline 中输出 \typeout
└── test-metropolis-fix.tex      # 修复验证测试（待完成）
```

## Path Responsibilities

- `test-minimal.tex`：最小可复现测试。metropolis + 2 正文帧 + `\appendix` + `\section{Appendix}` + 2 附录帧。确认附录 footline 不渲染。
- `test-no-section.tex`：去掉 `\section{Appendix}`，证明 `\AtBeginSection` 不是元凶。
- `test-plain-footline.tex`：使用无条件的简单 footline，证明 `\ifbeamer@inappendix` 不是元凶。
- `test-no-metropolis.tex`：Madrid 主题替代 metropolis，附录 footline 正常 → **锁定 metropolis 为元凶**。
- `test-diagnostic.tex`：在 footline 中添加 `\typeout` 诊断，确认附录帧完全不触发 footline。
- `test-metropolis-fix.tex`：待完成的修复验证测试。
