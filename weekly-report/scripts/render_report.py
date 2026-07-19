#!/usr/bin/env python3
"""Validate a weekly-report YAML file and render Beamer fragments."""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


ALLOWED_TYPES = {
    "experiment": {
        "label": "实验",
        "left": "假设、设置与行动",
        "change": "本周实验",
        "evidence": "结果证据",
    },
    "engineering": {
        "label": "代码与工程",
        "left": "工程目标与实现",
        "change": "本周变更",
        "evidence": "验证证据",
    },
    "reading": {
        "label": "文献阅读",
        "left": "研究问题与核心观点",
        "change": "本周阅读",
        "evidence": "迁移依据",
    },
    "writing": {
        "label": "写作",
        "left": "论点、产出与修订",
        "change": "本周产出",
        "evidence": "文稿与反馈",
    },
    "coordination": {
        "label": "协作与事务",
        "left": "决议、执行与依赖",
        "change": "本周推进",
        "evidence": "结果证据",
    },
}

STATUS = {
    "green": ("绿", "green!50!black"),
    "yellow": ("黄", "orange!85!black"),
    "red": ("红", "red!80!black"),
}

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".pdf"}

LATEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


class ReportValidationError(ValueError):
    """Raised when report.yaml does not satisfy the public data interface."""


def latex_escape(value: str) -> str:
    """Escape plain user text so it cannot alter the generated LaTeX."""

    return "".join(LATEX_ESCAPES.get(char, char) for char in value)


def _mapping(value: Any, path: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{path} 必须是映射对象")
        return {}
    return value


def _list(value: Any, path: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{path} 必须是列表")
        return []
    return value


def _text(
    mapping: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
    *,
    required: bool = True,
    max_length: int = 220,
) -> str:
    value = mapping.get(key, "")
    field = f"{path}.{key}"
    if not isinstance(value, str):
        errors.append(f"{field} 必须是字符串；日期和数字也请加引号")
        return ""
    value = value.strip()
    if required and not value:
        errors.append(f"{field} 不能为空")
    if len(value) > max_length:
        errors.append(f"{field} 过长（{len(value)} > {max_length}）")
    return value


def validate_image_path(value: str, field: str, root: Path, errors: list[str]) -> str:
    """Accept only existing PNG/JPEG/PDF files lexically and physically in img/."""

    if not value:
        return ""
    if not isinstance(value, str):
        errors.append(f"{field} 必须是字符串路径")
        return ""

    normalized = value.replace("\\", "/").strip()
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != "img":
        errors.append(f"{field} 必须是 img/ 下的相对路径")
        return normalized
    if path.suffix.lower() not in IMAGE_SUFFIXES:
        errors.append(f"{field} 仅支持 PNG、JPG、JPEG 或 PDF")
        return normalized

    image_root = (root / "img").resolve()
    disk_path = (root / Path(*path.parts)).resolve()
    try:
        disk_path.relative_to(image_root)
    except ValueError:
        errors.append(f"{field} 解析后越过了 img/ 目录")
        return normalized
    if not disk_path.is_file():
        errors.append(f"{field} 文件不存在：{normalized}")
    return path.as_posix()


def validate_report(data: Any, root: Path) -> dict[str, Any]:
    """Validate and return the original report mapping when it is safe to render."""

    errors: list[str] = []
    report = _mapping(data, "root", errors)
    if report.get("version") != 1:
        errors.append("version 必须为整数 1")

    week = _mapping(report.get("week"), "week", errors)
    for key, limit in (
        ("title", 60),
        ("subtitle", 80),
        ("author", 60),
        ("institute", 100),
        ("period", 60),
        ("date", 60),
        ("conclusion", 220),
        ("confirmed", 220),
        ("uncertainty", 220),
        ("request", 220),
    ):
        _text(week, key, "week", errors, max_length=limit)
    logo = week.get("logo", "")
    if logo:
        validate_image_path(logo, "week.logo", root, errors)

    work_items = _list(report.get("work_items"), "work_items", errors)
    if not 1 <= len(work_items) <= 5:
        errors.append("work_items 必须包含 1 到 5 项")

    focus_count = 0
    for index, raw_item in enumerate(work_items):
        path = f"work_items[{index}]"
        item = _mapping(raw_item, path, errors)
        _text(item, "title", path, errors, max_length=60)
        _text(item, "overview", path, errors, max_length=120)
        for key in ("objective", "change", "impact", "next_step"):
            _text(item, key, path, errors)
        _text(item, "blocker", path, errors, required=False, max_length=180)
        _text(item, "request", path, errors, required=False, max_length=180)

        item_type = item.get("type")
        if item_type not in ALLOWED_TYPES:
            errors.append(f"{path}.type 未知：{item_type!r}")
        status = item.get("status")
        if status not in STATUS:
            errors.append(f"{path}.status 必须是 green、yellow 或 red")
        focus = item.get("focus")
        if not isinstance(focus, bool):
            errors.append(f"{path}.focus 必须是 YAML 布尔值 true 或 false")
        elif focus:
            focus_count += 1

        evidence = _mapping(item.get("evidence"), f"{path}.evidence", errors)
        _text(evidence, "summary", f"{path}.evidence", errors)
        image = evidence.get("image", "")
        if image:
            validate_image_path(image, f"{path}.evidence.image", root, errors)
            _text(
                evidence,
                "caption",
                f"{path}.evidence",
                errors,
                required=False,
                max_length=100,
            )

    if focus_count > 2:
        errors.append(f"focus=true 的工作项最多 2 个，当前为 {focus_count} 个")

    next_week = _list(report.get("next_week"), "next_week", errors)
    if not 1 <= len(next_week) <= 4:
        errors.append("next_week 必须包含 1 到 4 项")
    for index, raw_plan in enumerate(next_week):
        path = f"next_week[{index}]"
        plan = _mapping(raw_plan, path, errors)
        for key in ("action", "deliverable", "evidence"):
            _text(plan, key, path, errors, max_length=180)
        _text(plan, "dependency", path, errors, required=False, max_length=120)

    appendix = _list(report.get("appendix", []), "appendix", errors)
    if len(appendix) > 5:
        errors.append("appendix 最多包含 5 项")
    for index, raw_slide in enumerate(appendix):
        path = f"appendix[{index}]"
        slide = _mapping(raw_slide, path, errors)
        _text(slide, "title", path, errors, max_length=80)
        bullets = _list(slide.get("bullets"), f"{path}.bullets", errors)
        if not 1 <= len(bullets) <= 6:
            errors.append(f"{path}.bullets 必须包含 1 到 6 项")
        for bullet_index, bullet in enumerate(bullets):
            if not isinstance(bullet, str) or not bullet.strip():
                errors.append(f"{path}.bullets[{bullet_index}] 必须是非空字符串")
            elif len(bullet.strip()) > 180:
                errors.append(f"{path}.bullets[{bullet_index}] 过长")
        image = slide.get("image", "")
        if image:
            validate_image_path(image, f"{path}.image", root, errors)
            _text(slide, "caption", path, errors, required=False, max_length=100)

    if errors:
        formatted = "\n".join(f"- {error}" for error in errors)
        raise ReportValidationError(f"report.yaml 校验失败：\n{formatted}")
    return report


def _tex(value: str) -> str:
    return latex_escape(value.strip())


def _fragment(value: str) -> str:
    """Render prose inside a semicolon-separated list without doubled punctuation."""

    return _tex(value).rstrip("。；;，, ")


def _image_tex(path: str, caption: str, *, height: str = "0.43\\textheight") -> str:
    caption_tex = _tex(caption) if caption else ""
    return (
        "\\begin{center}\n"
        f"  \\includegraphics[width=\\linewidth,height={height},keepaspectratio]"
        f"{{\\detokenize{{{path}}}}}\n"
        + (f"  \\par\\vspace{{0.3em}}{{\\scriptsize {caption_tex}}}\n" if caption_tex else "")
        + "\\end{center}\n"
    )


def render_preamble(report: dict[str, Any]) -> str:
    week = report["week"]
    subtitle = f"{_tex(week['subtitle'])}\\\\[0.2em]{_tex(week['period'])}"
    return (
        "% Generated from report.yaml. Do not edit.\n"
        f"\\title{{{_tex(week['title'])}}}\n"
        f"\\subtitle{{{subtitle}}}\n"
        f"\\author{{{_tex(week['author'])}}}\n"
        f"\\institute{{{_tex(week['institute'])}}}\n"
        f"\\date{{{_tex(week['date'])}}}\n"
    )


def render_title_frame(week: dict[str, Any]) -> str:
    logo = week.get("logo", "")
    background_open = ""
    background_close = ""
    if logo:
        background_open = (
            "{\n"
            "\\usebackgroundtemplate{%\n"
            "  \\begin{tikzpicture}[remember picture, overlay]\n"
            "    \\node[anchor=north east, xshift=-0.8cm, yshift=-0.65cm]\n"
            "      at (current page.north east)\n"
            f"      {{\\includegraphics[height=1.2cm]{{\\detokenize{{{logo}}}}}}};\n"
            "  \\end{tikzpicture}%\n"
            "}\n"
        )
        background_close = "}\n\n"
    return (
        background_open
        + "\\begin{frame}[shrink=12]\n"
        + "  \\titlepage\n"
        + "\\end{frame}\n\n"
        + background_close
    )


def render_conclusion_frame(week: dict[str, Any]) -> str:
    return (
        "\\begin{frame}{本周结论}\n"
        "  \\begin{block}{一句话判断}\n"
        f"    {_tex(week['conclusion'])}\n"
        "  \\end{block}\n"
        "  \\vspace{0.5em}\n"
        "  \\begin{itemize}\n"
        f"    \\item \\textbf{{已确认：}}{_tex(week['confirmed'])}\n"
        f"    \\item \\textbf{{仍不确定：}}{_tex(week['uncertainty'])}\n"
        f"    \\item \\textbf{{本次希望讨论：}}{_tex(week['request'])}\n"
        "  \\end{itemize}\n"
        "\\end{frame}\n\n"
    )


def status_tex(status: str) -> str:
    label, color = STATUS[status]
    return f"\\textcolor{{{color}}}{{\\textbf{{{label}}}}}"


def render_overview_frame(items: list[dict[str, Any]]) -> str:
    rows = "\n".join(
        f"      {_tex(item['title'])} & {_tex(item['overview'])} & {status_tex(item['status'])} \\\\"
        for item in items
    )
    focused = [item["title"] for item in items if item["focus"]]
    focus_text = "、".join(_tex(title) for title in focused) if focused else "本周无单独展开项"
    return (
        "\\begin{frame}[shrink=5]{本周工作概览}\n"
        "  \\renewcommand{\\arraystretch}{1.2}\n"
        "  \\begin{table}\n"
        "    \\centering\\small\n"
        "    \\begin{tabular}{p{0.23\\textwidth}p{0.49\\textwidth}p{0.10\\textwidth}}\n"
        "      \\toprule\n"
        "      \\textbf{工作项} & \\textbf{本周变化 / 证据} & \\textbf{状态} \\\\\n"
        "      \\midrule\n"
        f"{rows}\n"
        "      \\bottomrule\n"
        "    \\end{tabular}\n"
        "  \\end{table}\n"
        "  \\begin{block}{重点选择}\n"
        f"    {focus_text}\n"
        "  \\end{block}\n"
        "\\end{frame}\n\n"
    )


def render_focus_frame(item: dict[str, Any]) -> str:
    adapter = ALLOWED_TYPES[item["type"]]
    evidence = item["evidence"]
    title = f"{adapter['label']}：{_tex(item['title'])}"
    image = evidence.get("image", "")

    left_text = (
        f"  \\textbf{{{adapter['left']}}}\n"
        "  \\begin{itemize}\n"
        f"    \\item \\textbf{{目标：}}{_tex(item['objective'])}\n"
        f"    \\item \\textbf{{{adapter['change']}：}}{_tex(item['change'])}\n"
        f"    \\item \\textbf{{{adapter['evidence']}：}}{_tex(evidence['summary'])}\n"
        "  \\end{itemize}\n"
    )
    right_text = (
        "  \\textbf{结论与影响}\n"
        "  \\begin{itemize}\n"
        f"    \\item \\textbf{{状态：}}{status_tex(item['status'])}\n"
        f"    \\item \\textbf{{影响：}}{_tex(item['impact'])}\n"
        + (f"    \\item \\textbf{{阻碍：}}{_tex(item['blocker'])}\n" if item.get("blocker") else "")
        + (f"    \\item \\textbf{{请求：}}{_tex(item['request'])}\n" if item.get("request") else "")
        + f"    \\item \\textbf{{下一步：}}{_tex(item['next_step'])}\n"
        "  \\end{itemize}\n"
    )

    if image:
        left_column = _image_tex(image, evidence.get("caption", ""))
        right_column = left_text + right_text
        widths = ("0.43", "0.53")
    else:
        left_column = left_text
        right_column = right_text
        widths = ("0.48", "0.48")

    return (
        f"\\begin{{frame}}[shrink=5]{{{title}}}\n"
        "  \\begin{columns}[T]\n"
        f"    \\begin{{column}}{{{widths[0]}\\textwidth}}\n"
        + left_column
        + "    \\end{column}\n"
        f"    \\begin{{column}}{{{widths[1]}\\textwidth}}\n"
        + right_column
        + "    \\end{column}\n"
        "  \\end{columns}\n"
        "\\end{frame}\n\n"
    )


def render_discussion_frame(week: dict[str, Any], items: list[dict[str, Any]]) -> str:
    issues = [item for item in items if item.get("blocker") or item.get("request")]
    issue_lines = []
    for item in issues:
        detail_parts = []
        if item.get("blocker"):
            detail_parts.append(f"阻碍：{_fragment(item['blocker'])}")
        if item.get("request"):
            detail_parts.append(f"请求：{_fragment(item['request'])}")
        issue_lines.append(
            f"    \\item \\textbf{{{_tex(item['title'])}：}}" + "；".join(detail_parts)
        )

    body = (
        "\\begin{frame}[shrink=12]{问题与讨论}\n"
        "  \\begin{alertblock}{本次希望获得}\n"
        f"    {_tex(week['request'])}\n"
        "  \\end{alertblock}\n"
    )
    if issue_lines:
        body += "  \\begin{itemize}\n" + "\n".join(issue_lines) + "\n  \\end{itemize}\n"
    body += "\\end{frame}\n\n"
    return body


def render_plan_frame(plans: list[dict[str, Any]]) -> str:
    lines = []
    for plan in plans:
        dependency = plan.get("dependency", "")
        dependency_tex = f"；依赖：{_tex(dependency)}" if dependency else ""
        lines.append(
            "    \\item "
            f"\\textbf{{{_tex(plan['action'])}}}："
            f"交付 {_tex(plan['deliverable'])}；"
            f"成功证据为 {_tex(plan['evidence'])}{dependency_tex}。"
        )
    return (
        "\\begin{frame}[shrink=8]{下周计划}\n"
        "  \\begin{enumerate}\n"
        + "\n".join(lines)
        + "\n  \\end{enumerate}\n"
        "\\end{frame}\n\n"
    )


def render_appendix(slides: list[dict[str, Any]]) -> str:
    if not slides:
        return ""
    output = "\\appendix\n\n"
    for slide in slides:
        bullets = "\n".join(f"    \\item {_tex(bullet)}" for bullet in slide["bullets"])
        image = slide.get("image", "")
        if image:
            body = (
                "  \\begin{columns}[T]\n"
                "    \\begin{column}{0.50\\textwidth}\n"
                + "  " + _image_tex(image, slide.get("caption", ""), height="0.50\\textheight").replace("\n", "\n  ")
                + "    \\end{column}\n"
                "    \\begin{column}{0.46\\textwidth}\n"
                "      \\begin{itemize}\n"
                + bullets.replace("    ", "        ")
                + "\n      \\end{itemize}\n"
                "    \\end{column}\n"
                "  \\end{columns}\n"
            )
        else:
            body = "  \\begin{itemize}\n" + bullets + "\n  \\end{itemize}\n"
        output += (
            f"\\begin{{frame}}[shrink=5]{{{_tex(slide['title'])}}}\n"
            + body
            + "\\end{frame}\n\n"
        )
    return output


def render_content(report: dict[str, Any]) -> str:
    week = report["week"]
    items = report["work_items"]
    focused = [item for item in items if item["focus"]]
    content = "% Generated from report.yaml. Do not edit.\n\n"
    content += render_title_frame(week)
    content += render_conclusion_frame(week)
    content += render_overview_frame(items)
    for item in focused:
        content += render_focus_frame(item)
    content += render_discussion_frame(week, items)
    content += render_plan_frame(report["next_week"])
    content += (
        "\\begin{frame}[c]{}\n"
        "  \\centering\n"
        "  \\Huge 谢谢！\\\\[0.5em]\n"
        "  \\Large 欢迎讨论与建议\n"
        "\\end{frame}\n\n"
    )
    content += render_appendix(report.get("appendix", []))
    return content


def render_report(source: Path, output_dir: Path, *, check_only: bool = False) -> dict[str, Any]:
    root = source.parent.resolve()
    try:
        data = yaml.safe_load(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReportValidationError(f"找不到输入文件：{source}") from exc
    except yaml.YAMLError as exc:
        raise ReportValidationError(f"YAML 语法错误：{exc}") from exc

    report = validate_report(data, root)
    if not check_only:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "preamble.tex").write_text(render_preamble(report), encoding="utf-8")
        (output_dir / "content.tex").write_text(render_content(report), encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", default="report.yaml", help="YAML input file")
    parser.add_argument("--check", action="store_true", help="validate only; do not generate TeX")
    parser.add_argument("--output-dir", default="generated", help="generated TeX directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = Path(args.source).expanduser().resolve()
    output = Path(args.output_dir)
    if not output.is_absolute():
        output = source.parent / output
    try:
        report = render_report(source, output, check_only=args.check)
    except ReportValidationError as exc:
        print(exc)
        return 2

    focus_count = sum(1 for item in report["work_items"] if item["focus"])
    action = "校验通过" if args.check else "已生成 TeX"
    print(
        f"{action}：{len(report['work_items'])} 个工作项，"
        f"{focus_count} 个重点，{len(report.get('appendix', []))} 个附录项。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
