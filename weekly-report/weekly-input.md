# `report.yaml` 字段指南

`report.yaml` 是每周汇报的唯一内容源。本文件只解释字段，不参与生成。

## 顶层结构

```yaml
version: 1
week: {}
work_items: []
next_week: []
appendix: []
```

## `week`

| 字段 | 必填 | 含义 |
|---|---|---|
| `title` | 是 | 封面标题 |
| `subtitle` | 是 | 组会或报告场景 |
| `author` | 是 | 汇报人 |
| `institute` | 是 | 学校、学院或课题组 |
| `period` | 是 | 本周起止日期 |
| `date` | 是 | 汇报日期；请加引号 |
| `conclusion` | 是 | 不超过两句的本周总判断 |
| `confirmed` | 是 | 已被证据支持的事项 |
| `uncertainty` | 是 | 仍未解决的问题 |
| `request` | 是 | 希望在本次汇报中获得的决策或帮助；没有则写“无” |
| `logo` | 否 | `img/` 中的封面 Logo |

## `work_items`

每项工作使用同一个任务接口：

```yaml
- title: "工作项名称"
  type: experiment
  focus: true
  status: green
  overview: "概览页中的一句话。"
  objective: "要消除什么不确定性，或交付什么？"
  change: "本周实际完成、发现或调整了什么？"
  evidence:
    summary: "关键指标、产物或可复现结果。"
    image: "img/result.png"       # 可选
    caption: "结果图说明"         # 可选
  impact: "证据对研究路线、方案或时间表意味着什么？"
  blocker: "阻碍；没有则留空字符串。"
  request: "希望获得的具体帮助；没有则留空字符串。"
  next_step: "下一个最小可验证动作。"
```

枚举值：

- `type`：`experiment`、`engineering`、`reading`、`writing`、`coordination`。
- `status`：`green`（可继续）、`yellow`（有风险）、`red`（受阻）。
- `focus`：YAML 布尔值 `true` 或 `false`；最多两个 `true`。

## `next_week`

```yaml
- action: "要执行的动作"
  deliverable: "到下次组会前的最小交付"
  evidence: "如何判断它确实完成"
  dependency: "依赖的决策、资源或反馈；可为空"
```

## `appendix`

```yaml
- title: "补充实验"
  bullets:
    - "补充说明一"
    - "补充说明二"
  image: "img/extra-result.pdf"  # 可选
  caption: "补充结果"            # 可选
```

## 填写约束

- 工作项必须为 1--5 个；重点项最多 2 个。
- 下周计划必须为 1--4 个；附录最多 5 页。
- 图片仅支持 PNG、JPG、JPEG、PDF，且必须真实存在于 `img/`。
- 日期、百分比和看似数字的文本建议始终加引号，避免 YAML 自动改变类型。
- 文本字段不接受原始 LaTeX；`%`、`_`、`&` 等会自动转义。
