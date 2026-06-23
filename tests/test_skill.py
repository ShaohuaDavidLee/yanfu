from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "yanfu"
SKILL_MD = SKILL_DIR / "SKILL.md"
AGENT_YAML = SKILL_DIR / "agents" / "openai.yaml"
VALIDATOR = SKILL_DIR / "scripts" / "validate_delivery.py"


def read(path):
    return path.read_text(encoding="utf-8")


class YanfuSkillContract(unittest.TestCase):
    def test_skill_metadata_and_interface(self):
        text = read(SKILL_MD)
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        self.assertIn("name: yanfu", frontmatter)
        description = next(
            line.split(":", 1)[1].strip().strip('"')
            for line in frontmatter.splitlines()
            if line.startswith("description:")
        )
        self.assertTrue(description.startswith("用于"))
        self.assertIn("Landing Page", description)
        self.assertIn("产品截图", description)

        interface = read(AGENT_YAML)
        self.assertIn('display_name: "严复 Skill"', interface)
        self.assertIn("$yanfu", interface)
        self.assertIn("用 $yanfu", interface)

    def test_input_contract_and_incomplete_input_behavior(self):
        text = read(SKILL_MD)
        self.assertIn("公开可访问的 Landing Page URL", text)
        self.assertIn("1–5 张核心产品截图", text)
        self.assertIn("只有 URL", text)
        self.assertIn("只有截图", text)
        self.assertIn("不得自行注册或登录", text)

    def test_scope_boundaries_are_explicit(self):
        text = read(SKILL_MD)
        for rule in (
            "不得重新定位产品",
            "不得修改目标用户",
            "不得发明承诺",
            "不得进行竞品分析",
            "不得判断产品是否值得做",
            "不得大范围重做视觉识别",
        ):
            self.assertIn(rule, text)

    def test_workflow_requires_evidence_ledger(self):
        text = read(SKILL_MD)
        self.assertIn("翻译底稿", text)
        method = read(SKILL_DIR / "references" / "translation-method.md")
        for field in (
            "新页面表达",
            "原始依据",
            "处理方式",
            "置信度",
        ):
            self.assertIn(field, method)
        self.assertIn("功能", method)
        self.assertIn("用户动作", method)
        self.assertIn("用户结果", method)
        self.assertIn("可复述表达", method)

    def test_output_contract_and_references(self):
        text = read(SKILL_MD)
        self.assertIn("landing.html", text)
        self.assertIn("yanfu-notes.md", text)
        self.assertIn("references/evidence-and-browsing.md", text)
        self.assertIn("references/translation-method.md", text)
        self.assertIn("references/output-spec.md", text)

        output_spec = read(SKILL_DIR / "references" / "output-spec.md")
        for heading in ("## 信", "## 达", "## 雅", "## 待确认"):
            self.assertIn(heading, output_spec)

    def test_skill_contains_no_placeholders(self):
        combined = "\n".join(
            read(path)
            for path in SKILL_DIR.rglob("*")
            if path.is_file() and path.suffix in {".md", ".yaml", ".py"}
        )
        self.assertNotIn("TODO", combined)
        self.assertNotIn("TBD", combined)


class DeliveryValidatorContract(unittest.TestCase):
    def run_validator(self, output_dir):
        return subprocess.run(
            ["python3", str(VALIDATOR), str(output_dir)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_validator_accepts_complete_delivery(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            (output / "product.png").write_bytes(b"image")
            (output / "landing.html").write_text(
                """<!doctype html>
<html lang="zh-CN"><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Product</title></head>
<body><main><h1>用户能懂的一句话</h1>
<img src="product.png" alt="核心产品界面">
<a href="https://example.com/start">开始使用</a>
</main></body></html>""",
                encoding="utf-8",
            )
            (output / "yanfu-notes.md").write_text(
                """# 严复译注

## 信
保留原价值主张。

## 达
一句话 Pitch 与故事顺序。

## 雅
保留原设计元素。

## 待确认
无。
""",
                encoding="utf-8",
            )

            result = self.run_validator(output)

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("严复交付校验通过", result.stdout)

    def test_validator_rejects_missing_evidence_and_notes_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            (output / "landing.html").write_text(
                "<html><body><h1>Product</h1><img src='missing.png'></body></html>",
                encoding="utf-8",
            )
            (output / "yanfu-notes.md").write_text("# Notes\n", encoding="utf-8")

            result = self.run_validator(output)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("viewport", result.stdout)
            self.assertIn("缺少本地资源", result.stdout)
            self.assertIn("译注缺少章节", result.stdout)


if __name__ == "__main__":
    unittest.main()
