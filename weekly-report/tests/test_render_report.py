from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "render_report.py"
SPEC = importlib.util.spec_from_file_location("render_report", MODULE_PATH)
assert SPEC and SPEC.loader
render_report = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(render_report)


def make_report(item_type: str = "experiment") -> dict:
    return {
        "version": 1,
        "week": {
            "title": "周报",
            "subtitle": "组会",
            "author": "测试者",
            "institute": "测试课题组",
            "period": "2026-W29",
            "date": "2026-07-19",
            "conclusion": "核心结论",
            "confirmed": "已确认结果",
            "uncertainty": "待验证问题",
            "request": "需要一个决策",
        },
        "work_items": [
            {
                "title": "工作项",
                "type": item_type,
                "focus": True,
                "status": "green",
                "overview": "概览",
                "objective": "目标",
                "change": "变化",
                "evidence": {"summary": "证据 85% & macro_F1"},
                "impact": "影响",
                "blocker": "",
                "request": "",
                "next_step": "下一步",
            }
        ],
        "next_week": [
            {
                "action": "行动",
                "deliverable": "交付",
                "evidence": "可检查证据",
                "dependency": "无",
            }
        ],
        "appendix": [],
    }


class RenderReportTests(unittest.TestCase):
    def test_latex_escape_protects_plain_text(self) -> None:
        escaped = render_report.latex_escape(r"baseline_v2: 85% & $x#1$")
        self.assertEqual(
            escaped,
            r"baseline\_v2: 85\% \& \$x\#1\$",
        )

    def test_every_work_type_has_an_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for item_type, adapter in render_report.ALLOWED_TYPES.items():
                data = make_report(item_type)
                validated = render_report.validate_report(data, root)
                content = render_report.render_content(validated)
                self.assertIn(adapter["label"], content)
                self.assertIn("目标", content)
                self.assertIn("下一步", content)

    def test_rejects_more_than_two_focus_items(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_report()
            data["work_items"] = [
                copy.deepcopy(data["work_items"][0]) for _ in range(3)
            ]
            with self.assertRaisesRegex(render_report.ReportValidationError, "最多 2 个"):
                render_report.validate_report(data, root)

    def test_rejects_unknown_type(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_report("unknown")
            with self.assertRaisesRegex(render_report.ReportValidationError, "type 未知"):
                render_report.validate_report(data, root)

    def test_rejects_missing_required_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_report()
            del data["work_items"][0]["objective"]
            with self.assertRaisesRegex(render_report.ReportValidationError, "objective 不能为空"):
                render_report.validate_report(data, root)

    def test_rejects_missing_and_escaping_image_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_report()
            data["work_items"][0]["evidence"]["image"] = "../secret.png"
            with self.assertRaisesRegex(render_report.ReportValidationError, "img/ 下"):
                render_report.validate_report(data, root)

            data["work_items"][0]["evidence"]["image"] = "img/missing.png"
            with self.assertRaisesRegex(render_report.ReportValidationError, "文件不存在"):
                render_report.validate_report(data, root)

    def test_existing_image_is_rendered_with_detokenize(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "img").mkdir()
            (root / "img" / "result.png").write_bytes(b"fixture")
            data = make_report()
            data["work_items"][0]["evidence"].update(
                {"image": "img/result.png", "caption": "结果图"}
            )
            validated = render_report.validate_report(data, root)
            content = render_report.render_content(validated)
            self.assertIn(r"\detokenize{img/result.png}", content)

    def test_appendix_does_not_add_an_empty_section_page(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_report()
            data["appendix"] = [{"title": "补充说明", "bullets": ["一条证据"]}]
            validated = render_report.validate_report(data, root)
            appendix = render_report.render_appendix(validated["appendix"])
            self.assertIn(r"\appendix", appendix)
            self.assertNotIn(r"\section", appendix)


if __name__ == "__main__":
    unittest.main()
