# Goal

## User Request

排查并修复附录帧不显示页码的 bug：`\appendix` 后的帧 footline 中页码消失。

## Purpose Analysis

- **真实目标**：无论使用自定义 footline 还是 metropolis 默认 footline，附录帧都应显示页码（A-1, A-2, ...），不能因为进入附录区域就变成空白 footline。
- **影响用户**：使用本 Beamer 模板进行答辩/组会汇报的用户，需要在问答环节跳转到附录帧时看到正确的页码。
- **核心价值**：修复一个阻断性 bug——附录帧完全没有页码，用户在问答时无法定位。

## MVP Definition

最小目标：找到根因 → 验证 → 提供可工作的修复（应用于 `beamer-style.sty`）。

## Assumptions

- 问题出现在 metropolis 主题 + 自定义 footline 的组合场景中。
- 问题不在 CJK 字体、参考文献等无关组件。

## Non-Goals

- 不在此实验中修改正式代码（最终修复在实验验证后再合并到 `beamer-style.sty`）。
- 不重新设计整个页码系统。

## Target User

使用本模板的 Beamer 用户。

## Success Criteria

- [x] 定位根因（哪个主题/宏包/钩子导致 footline 消失）。✅
- [x] 在最小可复现测试文件中复现 bug。✅
- [x] 提出修复方案并在测试文件中验证通过。✅ pgfkey 中性化
- [x] 将修复应用到 `beamer-style.sty` 并通过回归编译。✅ 19 页 / 9 页，0 overfull
