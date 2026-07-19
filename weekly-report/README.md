# 数据驱动的每周工作汇报

每周只编辑 `report.yaml`，并把图片放入 `img/`；`main.tex` 和 `generated/` 都不需要手改。

## 快速使用

```bash
cd weekly-report
make check   # 只校验 YAML
make report  # 校验 → 生成 TeX → 编译 weekly-report.pdf
```

Python 依赖为 PyYAML。若本机尚未安装：

```bash
python3 -m pip install -r requirements.txt
```

## 唯一输入

`report.yaml` 包含四部分：

- `week`：封面信息、本周结论、已确认事项、不确定性和讨论请求。
- `work_items`：1--5 个工作项，其中最多两个设置为 `focus: true`。
- `next_week`：1--4 个带有交付物和成功证据的下周行动。
- `appendix`：可选的补充材料页。

完整字段解释见 [weekly-input.md](weekly-input.md)。普通文本会自动转义 `%`、`_`、`&`、`#` 等 LaTeX 特殊字符，因此不要在 YAML 文本字段中写 LaTeX 命令。

## 插入图片

先把 PNG、JPG、JPEG 或 PDF 放入 `img/`，再在工作项的 `evidence` 中引用：

```yaml
evidence:
  summary: "准确率提升 2.1 个百分点。"
  image: "img/ablation-result.pdf"
  caption: "消融实验结果"
```

封面 Logo 使用：

```yaml
week:
  logo: "img/logo.png"
```

渲染器会拒绝绝对路径、`../`、不存在的文件和 `img/` 之外的路径。

## 工作类型适配器

| `type` | 重点页侧重 |
|---|---|
| `experiment` | 假设、设置、实验动作、结果证据 |
| `engineering` | 工程目标、实现变更、验证证据 |
| `reading` | 研究问题、核心观点、迁移依据 |
| `writing` | 论点、写作产出、文稿与反馈 |
| `coordination` | 决议、执行、结果与依赖 |

所有类型都保留共同字段：目标、变化、证据、状态、影响、阻碍/请求和下一步。

## 页面生成规则

- 所有工作项进入概览页。
- `focus: true` 的工作项各生成一页重点进展，最多两页。
- 存在阻碍或请求的工作项自动进入“问题与讨论”。
- `next_week` 自动生成下周计划。
- `appendix` 中每一项生成一页附录，使用 A-1、A-2 等页码。

## 其他命令

```bash
make render  # 只生成 generated/*.tex
make test    # 运行渲染器测试
make clean   # 清理 LaTeX 中间文件
```

切换视觉设计时只需修改稳定外壳 `main.tex` 中的 `design=academic`，可选 `classic` 或 `midnight`；这不是每周内容的一部分。
