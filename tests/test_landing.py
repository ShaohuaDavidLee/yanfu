from html.parser import HTMLParser
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "landing" / "index.html"
DEMO_PAGE = ROOT / "landing" / "demo" / "index.html"
LETS_POD_EVENTS = ROOT / "landing" / "demo" / "letspod-events.json"
LANDING_ASSETS = ROOT / "landing" / "assets"


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
        self.assertIn("不重定位", self.html)
        self.assertIn("中文市场", self.html)
        self.assertIn("英文市场 Beta", self.html)

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
        self.assertNotIn("MusicBox", self.html)
        self.assertNotIn("1000 首歌", self.html)
        self.assertNotIn("便携式数字音乐播放器", self.html)
        self.assertNotIn("writing-mode:vertical-rl", self.html)
        self.assertIn("真实项目的表达前后对照", cases)
        for product in ("Let's Pod", "TransWeb", "草诀歌 AI Labs", "InkDao"):
            self.assertIn(f'{product} Before', cases)
            self.assertIn(f'{product} After', cases)
        for prefix in ("lp", "tw", "cjg", "ink"):
            self.assertIn(f"{prefix}ShowSrc", self.html)
            self.assertIn(f"{prefix}ShowTgt", self.html)
            self.assertIn(f"{prefix}View", self.html)
        self.assertEqual(cases.count("<article"), 4)
        self.assertEqual(cases.count(">Before</button>"), 4)
        self.assertEqual(cases.count(">After</button>"), 4)
        self.assertNotIn(">原文</button>", cases)
        self.assertNotIn(">译文</button>", cases)
        self.assertEqual(cases.count("中文市场 · 中→中"), 2)
        self.assertIn("英文市场 · 中→英", cases)
        self.assertIn("英文市场 · 英→英", cases)
        self.assertIn("A Chinese name you’ll never regret tattooing.", cases)
        self.assertNotIn("Get the Chinese name right", cases)
        self.assertNotIn("A Chinese name with meaning behind every character", cases)
        self.assertEqual(cases.count("<img"), 8)
        for name in (
            "letspod-source.jpg",
            "letspod-target.jpg",
            "transweb-source.jpg",
            "transweb-target.jpg",
            "caojuege-before.png",
            "caojuege-after.png",
            "inkdao-before.png",
            "inkdao-after.png",
        ):
            self.assertIn(f"assets/cases/{name}", cases)
            asset = LANDING_ASSETS / "cases" / name
            self.assertTrue(asset.is_file(), f"missing case asset: {name}")
            self.assertGreater(asset.stat().st_size, 1_000, f"empty case asset: {name}")
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
        self.assertIn("STEP 00", self.html)
        self.assertIn("这一版页面写给哪个市场", self.html)
        self.assertIn("粘贴落地页链接", self.html)
        self.assertIn("上传产品截图", self.html)
        self.assertIn("复制提示词", self.html)
        self.assertIn("下载严复任务包 ZIP", self.html)
        self.assertIn("只复制提示词", self.html)
        self.assertIn("yanfu-task-pack.zip", self.html)
        self.assertIn("prompt.md", self.html)
        self.assertIn("meta.json", self.html)
        self.assertIn("screenshots/", self.html)
        self.assertIn("https://github.com/ShaohuaDavidLee/yanfu", self.html)
        self.assertIn("截图无法进入剪贴板文本", self.html)
        self.assertIn("请手动把截图附加给你的 agent", self.html)
        self.assertIn("不要重新设计", self.html)
        self.assertIn("忠于原 Landing Page 的设计风格", self.html)

    def test_market_selector_precedes_url_and_supports_two_markets(self):
        download = self.html[self.html.index('id="download"'):self.html.index('id="family"')]
        self.assertLess(download.index("STEP 00"), download.index("STEP 01"))
        self.assertIn('data-market-options=""', download)
        self.assertIn('data-target-market="china"', download)
        self.assertIn('data-target-market="international-en"', download)
        self.assertIn('aria-label="选择目标市场"', download)
        self.assertIn("目标用户", download)
        self.assertIn('placeholder="例如：海外翻译和本地化专业从业者"', download)
        self.assertNotIn("主要写给谁", download)
        self.assertNotIn("第一次独立出海的中文开发者", download)
        self.assertIn("建议填写", download)
        self.assertIn("不填也可下载", download)

    def test_task_pack_v2_records_market_language_and_audience(self):
        for field in (
            "taskPackVersion: 2",
            "sourceLanguage: 'auto'",
            "targetMarket: 'china'",
            "targetLanguage: 'zh-CN'",
            "targetAudience: ''",
            "taskPackVersion: this.state.taskPackVersion",
            "sourceLanguage: this.state.sourceLanguage",
            "targetMarket: this.state.targetMarket",
            "targetLanguage: this.state.targetLanguage",
            "targetAudience: (this.state.targetAudience || '').trim()",
            "attribution: this.readAttribution()",
        ):
            self.assertIn(field, self.html)
        self.assertIn("targetMarket === 'international-en' ? 'en' : 'zh-CN'", self.html)

    def test_prompt_routes_all_four_language_paths_without_new_facts(self):
        prompt = self.html[self.html.index("  buildPrompt() {"):self.html.index("  buildMeta() {")]
        self.assertIn("先自动检测原页语言", prompt)
        for route in ("中→中", "英→中", "中→英", "英→英"):
            self.assertIn(route, prompt)
        self.assertIn("references/cross-market-adaptation.md", prompt)
        self.assertIn("不得引入任何新事实", prompt)
        self.assertIn("只在无法判断时再追问用户", prompt)

    def test_download_pack_is_generated_client_side(self):
        self.assertIn("downloadTaskPack", self.html)
        self.assertIn("createZip", self.html)
        self.assertIn("crc32", self.html)
        self.assertIn("application/zip", self.html)
        self.assertIn("URL.createObjectURL", self.html)

    def test_download_pack_requires_url_and_screenshot(self):
        self.assertIn("packError", self.html)
        self.assertIn("hasPackError", self.html)
        self.assertIn("请先粘贴落地页链接", self.html)
        self.assertIn("请上传 1–5 张核心产品截图", self.html)
        self.assertIn("再下载任务包", self.html)
        validation = self.html[
            self.html.index("  downloadTaskPack = async () => {"):
            self.html.index("    const files = [", self.html.index("  downloadTaskPack = async () => {"))
        ]
        self.assertNotIn("targetAudience", validation)
        self.assertNotIn("目标用户", validation)

    def test_market_selection_and_download_emit_local_events(self):
        self.assertIn("new CustomEvent(name, { detail })", self.html)
        self.assertIn("window.dataLayer.push({ event: name, ...detail })", self.html)
        self.assertIn("'yanfu:market-select'", self.html)
        self.assertIn("'yanfu:task-pack-download'", self.html)
        for field in ("utmSource", "utmMedium", "utmCampaign", "utmContent"):
            self.assertIn(field, self.html)

    def test_direct_hash_links_are_restored_after_runtime_hydration(self):
        self.assertIn("scrollToCurrentHash", self.html)
        self.assertIn("restoreHashAfterHydration", self.html)
        self.assertIn("waitForStableLayout", self.html)
        self.assertIn("pressed === 'true' || pressed === 'false'", self.html)
        self.assertIn("stableFrames >= 20", self.html)
        self.assertIn("behavior: 'instant'", self.html)
        self.assertIn("window.addEventListener('hashchange'", self.html)
        self.assertIn("window.addEventListener('load', restoreHashAfterHydration", self.html)

    def test_stable_brand_assets_and_share_metadata_are_present(self):
        self.assertIn('src="assets/yanfu-icon.png"', self.html)
        self.assertIn('src="assets/yanfu-portrait.png"', self.html)
        self.assertIn("mix-blend-mode:multiply", self.html)
        self.assertIn('<link rel="icon" type="image/png" href="assets/yanfu-icon.png">', self.html)
        self.assertIn('<meta property="og:title"', self.html)
        self.assertIn('<meta property="og:description"', self.html)
        self.assertIn('<meta property="og:url" content="https://yanfu.caojuege.com/">', self.html)
        self.assertIn('<meta property="og:image" content="https://yanfu.caojuege.com/assets/yanfu-share-card.png">', self.html)
        self.assertIn('<meta property="og:image:width" content="1200">', self.html)
        self.assertIn('<meta property="og:image:height" content="630">', self.html)
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', self.html)
        self.assertIn('<meta name="twitter:image" content="https://yanfu.caojuege.com/assets/yanfu-share-card.png">', self.html)
        self.assertIn('<link rel="canonical" href="https://yanfu.caojuege.com/">', self.html)

        for name in ("yanfu-icon.png", "yanfu-portrait.png", "yanfu-share-card.png"):
            asset = LANDING_ASSETS / name
            self.assertTrue(asset.is_file(), f"missing landing brand asset: {name}")
            self.assertGreater(asset.stat().st_size, 1_000, f"empty landing brand asset: {name}")

    def test_single_h1(self):
        self.assertEqual(
            1,
            sum(1 for tag, _ in self.parser.headings if tag == "h1"),
        )


class DemoPageContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = DEMO_PAGE.read_text(encoding="utf-8") if DEMO_PAGE.exists() else ""
        cls.parser = PageParser()
        cls.parser.feed(cls.html)

    def test_demo_page_file_exists(self):
        self.assertTrue(DEMO_PAGE.exists())

    def test_demo_page_is_letspod_real_replay(self):
        self.assertIn("Let’s Pod", self.html)
        self.assertIn("真实生成回放", self.html)
        self.assertIn("基于一次真实严复生成记录", self.html)
        self.assertIn("不调用模型", self.html)
        self.assertNotIn("打工 Demo", self.html)
        self.assertNotIn("TransWeb", self.html)
        self.assertNotIn("正在调用模型", self.html)

    def test_demo_page_replays_recorded_generation_events(self):
        self.assertTrue(LETS_POD_EVENTS.exists())
        events = json.loads(LETS_POD_EVENTS.read_text(encoding="utf-8"))
        event_types = {event["type"] for event in events}
        self.assertIn("status", event_types)
        self.assertIn("patch", event_types)
        self.assertIn("complete", event_types)
        self.assertIn('data-live-landing-preview', self.html)
        self.assertIn('data-event-log', self.html)
        self.assertIn('data-replay-status', self.html)
        self.assertIn('letspod-events.json', self.html)
        self.assertIn("重新播放", self.html)

    def test_demo_page_visualizes_live_landing_page_generation(self):
        self.assertIn("Landing Page 实时生成", self.html)
        self.assertIn('data-live-landing-preview', self.html)
        self.assertIn('data-preview-block', self.html)
        for block in ("Hero", "问题", "机制", "CTA"):
            self.assertIn(block, self.html)

    def test_demo_page_animates_text_and_lines_in_real_time(self):
        self.assertIn("逐字写入", self.html)
        self.assertIn("data-typewriter-root", self.html)
        self.assertIn("data-typewriter", self.html)
        self.assertIn("data-draw-line", self.html)
        events = json.loads(LETS_POD_EVENTS.read_text(encoding="utf-8"))
        patch_events = [event for event in events if event["type"] == "patch"]
        self.assertGreaterEqual(len(patch_events), 4)
        for event in patch_events:
            self.assertEqual(event["animation"]["text"], "typewriter")
            self.assertEqual(event["animation"]["lines"], "draw")

    def test_demo_page_removes_timeline_and_step_cards(self):
        self.assertNotIn('data-stage-card', self.html)
        self.assertNotIn('data-stage-player', self.html)
        self.assertNotIn('class="timeline"', self.html)
        self.assertNotIn("严复六阶段工作流", self.html)

    def test_demo_page_navigation_and_structure(self):
        self.assertEqual(
            1,
            sum(1 for tag, _ in self.parser.headings if tag == "h1"),
        )
        hrefs = {link.get("href") for link in self.parser.links}
        self.assertIn("../index.html", hrefs)
        self.assertIn("../index.html#download", hrefs)


if __name__ == "__main__":
    unittest.main()
