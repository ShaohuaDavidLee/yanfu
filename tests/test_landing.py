from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "landing" / "index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.ids = set()
        self.headings = []
        self._heading = None
        self._heading_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a":
            self.links.append(attrs)
        if tag == "img":
            self.images.append(attrs)
        if tag in {"h1", "h2", "h3"}:
            self._heading = tag
            self._heading_text = []

    def handle_data(self, data):
        if self._heading:
            self._heading_text.append(data)

    def handle_endtag(self, tag):
        if tag == self._heading:
            self.headings.append((tag, "".join(self._heading_text).strip()))
            self._heading = None


class LandingPageContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.parser = PageParser()
        cls.parser.feed(cls.html)

    def test_core_pitch_and_boundaries_are_present(self):
        self.assertIn("严复 Skill", self.html)
        self.assertIn("你的产品故事翻译官", self.html)
        self.assertIn("开发者视角", self.html)
        self.assertIn("用户 5 秒能懂", self.html)
        self.assertIn("不改产品定位", self.html)

    def test_required_sections_exist(self):
        for section_id in (
            "principles",
            "cases",
            "download",
            "family",
        ):
            self.assertIn(section_id, self.parser.ids)

    def test_translation_cases_replace_ipod_method_section(self):
        cases = self.html[self.html.index('id="cases"'):self.html.index('id="principles"')]
        self.assertIn("翻译案例", self.html)
        self.assertNotIn("原文 / 译文", self.html)
        self.assertNotIn("MusicBox", self.html)
        self.assertNotIn("1000 首歌", self.html)
        self.assertNotIn("便携式数字音乐播放器", self.html)
        self.assertNotIn("writing-mode:vertical-rl", self.html)
        self.assertNotIn("<img", cases)
        self.assertNotIn("<button", cases)
        self.assertNotIn("原文", cases)
        self.assertNotIn("译文", cases)
        self.assertNotIn("{{", cases)
        self.assertLess(self.html.index('id="cases"'), self.html.index('id="principles"'))

    def test_family_links_are_real_and_safe(self):
        expected = {
            "https://b.caojuege.com/",
            "https://simaqian.caojuege.com/",
            "https://www.caojuege.com/",
            "https://www.caojuege.com/davidli",
        }
        external = {
            link.get("href")
            for link in self.parser.links
            if link.get("href", "").startswith("https://")
        }
        self.assertTrue(expected.issubset(external))
        for link in self.parser.links:
            if link.get("href") in expected:
                self.assertEqual(link.get("target"), "_blank")
                self.assertIn("noopener", link.get("rel", ""))

    def test_images_have_alt_text_and_local_sources(self):
        self.assertGreaterEqual(len(self.parser.images), 3)
        for image in self.parser.images:
            self.assertIn("alt", image)
            self.assertFalse(image.get("src", "").startswith("data:"))

    def test_download_section_is_prompt_entry_not_fake_file(self):
        self.assertIn("粘贴落地页链接", self.html)
        self.assertIn("上传产品截图", self.html)
        self.assertIn("复制提示词", self.html)
        self.assertIn("https://github.com/ShaohuaDavidLee/yanfu", self.html)
        self.assertIn("截图无法进入剪贴板文本", self.html)
        self.assertIn("请手动把截图附加给你的 agent", self.html)
        self.assertIn("不要重新设计", self.html)
        self.assertIn("忠于原 Landing Page 的设计风格", self.html)
        self.assertNotIn('download="', self.html)

    def test_single_h1(self):
        self.assertEqual(
            1,
            sum(1 for tag, _ in self.parser.headings if tag == "h1"),
        )


if __name__ == "__main__":
    unittest.main()
