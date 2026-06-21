# MVP Flow

## Milestone 1: Project Foundation ✅

- [x] 创建最小测试文件 `test-minimal.tex`（metropolis + 自定义 footline + `\appendix`）。
- [x] 确认 bug 可复现：正文帧 footline 正常，附录帧 footline 消失。
- [x] Verification：诊断 `\typeout` 确认附录帧不触发 footline 模板。

## Milestone 2: Core Data or Domain Model ✅

关键隔离实验，逐一排除嫌疑：

| 测试文件 | 条件 | 附录 footline 是否渲染 |
|----------|------|----------------------|
| `test-minimal.tex` | metropolis + `\ifbeamer@inappendix` footline | ❌ 不渲染 |
| `test-no-section.tex` | 去掉 `\section{附录}` | ❌ 不渲染（排除 `\AtBeginSection` 嫌疑） |
| `test-plain-footline.tex` | 最简 footline（仅显示帧号，不用条件判断） | ❌ 不渲染（排除 `\ifbeamer@inappendix` 嫌疑） |
| `test-no-metropolis.tex` | 换成 Madrid 主题 | ✅ 正常渲染 |

**结论：元凶是 metropolis 主题。**

## Milestone 3: Main User Workflow ✅

在 `beamerouterthememetropolis.sty` 第 123-130 行找到根因：

```latex
\AtBeginDocument{%
  \apptocmd{\appendix}{%
    \pgfkeys{%
      /metropolis/outer/.cd,
      numbering=none,       % ← 帧号设为空模板
      progressbar=none}     % ← footline 重新激活 [plain] 变体
    }{}{}
}
```

**过程：**

1. **正文部分**：`progressbar=none` 是 metropolis 默认值 → footline = `[plain]` 变体。`[plain]` 变体内部调用 `\usebeamertemplate*{frame numbering}` 来渲染页码。在正文中 `numbering=counter`，帧号正常显示。

2. **用户自定义 footline**：我们的 `beamer-style.sty` 用 `\setbeamertemplate{footline}{...}` 设置了**默认** footline 模板。在正文中这覆盖了 `[plain]` 变体，正常显示。

3. **进入 `\appendix`**：metropolis 的钩子执行：
   - `numbering=none` → `frame numbering` 模板变为空
   - `progressbar=none` → `\setbeamertemplate{footline}[plain]` **重新激活 `[plain]` 变体，覆盖了用户的自定义 footline！**
   - 结果：`[plain]` footline 调用已被设为空的 `frame numbering` → **无页码**

**关键发现**：无论用户设置什么 footline，metropolis 都会在附录中用 `[plain]` 变体覆盖掉。

## Milestone 4: Verification and Demo

### 已测试的方案

| 方案 | 方法 | 结果 |
|------|------|------|
| 覆盖 `frame numbering` `none` 模板 | `\expandafter\def\csname beamer@@tmpop@frame numbering@none\endcsname{...}` | ❌ 诊断显示 footline 仍只调用 1 次 |
| 覆盖 `footline` `plain` 内部宏 | `\expandafter\def\csname beamer@@tmpop@footline@plain\endcsname{...}` | ❌ 诊断显示 footline 仍只调用 1 次 |
| `\apptocmd{\appendix}` 重新设置 footline | `\AtBeginDocument{\apptocmd{\appendix}{\setbeamertemplate{footline}{...}}}` | 待验证 |

### ✅ 最终方案：pgfkey 中性化

`\apptocmd{\appendix}` 方案（Milestone 4 中尝试）仍然失败——附录帧 footline 不渲染。原因是 Beamer 模板系统内部机制导致 `\setbeamertemplate{footline}{...}` 在附录中无法正确覆盖 `[plain]` 变体。

**有效方案**：直接清空 metropolis 用于破坏 footline 的两个 pgfkey handler：

```latex
\pgfkeys{
  /metropolis/outer/numbering/none/.code={},
  /metropolis/outer/progressbar/none/.code={},
}
```

当 metropolis 的 `\apptocmd{\appendix}` 触发 `\pgfkeys{numbering=none, progressbar=none}` 时，这些 key 变成空操作——不会清空帧号，不会重置 footline。用户的自定义 footline 在整个文档中保持激活。

然后设置自定义 footline（正文 `X/Y`，附录 `A-Z`）：

```latex
\setbeamertemplate{footline}{%
  \hfill%
  \usebeamercolor[fg]{page number in head/foot}%
  \usebeamerfont{page number in head/foot}%
  \ifbeamer@inappendix
    A-\insertframenumberinappendix
  \else
    \insertframenumber\,/\,\insertmainframenumber
  \fi
  \hspace{1.5em}\vspace{4pt}%
}
```

### Verification ✅

- [x] `main.tex`：19 页，0 overfull，正文 `X/12`，附录 `A-1, A-2`
- [x] `main-groupmeeting.tex`：9 页，0 overfull，正文 `X/7`，附录 `A-1`
- [x] 诊断 `\typeout` 确认 33 次 footline 调用，附录帧 `inapp=Y, off=1`
- [x] 正文帧 footline 不受影响

## Later

- 考虑向 metropolis 上游提 PR：附录中不应强制 `numbering=none`。
- `progressbar=none` 中性化也影响了 `headline` 和 `frametitle` 的 `[plain]` 设置。当前无可见副作用，但如果有问题，可以重定义 `.code` 仅跳过 `\setbeamertemplate{footline}[plain]`。
