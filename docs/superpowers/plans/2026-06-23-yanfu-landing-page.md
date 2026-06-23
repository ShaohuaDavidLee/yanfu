# Yanfu Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a responsive static landing page for Yanfu Skill that faithfully follows the approved “source / translation” visual direction and product-story contract.

**Architecture:** The deliverable is a framework-free static site in `landing/`. One semantic HTML document owns content, layout, styles, and small progressive-enhancement behavior. Real raster assets live under `landing/assets/`; Python standard-library tests parse the page and enforce its copy, links, states, and structural accessibility.

**Tech Stack:** HTML5, CSS, small vanilla JavaScript, Python `unittest`, local HTTP server, in-app browser.

---

## File Structure

- `landing/index.html`: semantic page, responsive CSS, anchor navigation, external links, download-unavailable state.
- `landing/assets/yanfu-portrait.png`: generated monochrome Yan Fu portrait used by the brand and hero.
- `landing/assets/manuscript-texture.png`: generated low-contrast manuscript texture.
- `landing/assets/cases/*.png`: real screenshots for Let’s Pod, TransWeb, and Baoqingtian comparisons.
- `tests/test_landing.py`: content, link, image-alt, heading, and download-state contract tests.
- `design-qa.md`: final comparison evidence and QA result.

### Task 1: Lock the page contract

**Files:**
- Create: `tests/test_landing.py`

- [ ] **Step 1: Write the failing tests**

```python
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
        for section_id in ("comparison", "principles", "process", "cases", "download", "family"):
            self.assertIn(section_id, self.parser.ids)

    def test_family_links_are_real_and_safe(self):
        expected = {
            "https://b.caojuege.com/",
            "https://simaqian.caojuege.com/",
            "https://www.caojuege.com/",
            "https://www.caojuege.com/davidli",
        }
        external = {link.get("href") for link in self.parser.links if link.get("href", "").startswith("https://")}
        self.assertTrue(expected.issubset(external))
        for link in self.parser.links:
            if link.get("href") in expected:
                self.assertEqual(link.get("target"), "_blank")
                self.assertIn("noopener", link.get("rel", ""))

    def test_images_have_alt_text_and_local_sources(self):
        self.assertGreaterEqual(len(self.parser.images), 8)
        for image in self.parser.images:
            self.assertIn("alt", image)
            self.assertFalse(image.get("src", "").startswith("data:"))

    def test_unpublished_download_does_not_fake_a_file(self):
        self.assertIn("Skill 完成后开放下载", self.html)
        self.assertNotIn('download="', self.html)

    def test_single_h1(self):
        self.assertEqual(1, sum(1 for tag, _ in self.parser.headings if tag == "h1"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify RED**

Run: `python3 -m unittest tests/test_landing.py -v`

Expected: error because `landing/index.html` does not exist.

- [ ] **Step 3: Commit the contract test**

```bash
git add tests/test_landing.py
git commit -m "test: define yanfu landing page contract"
```

### Task 2: Prepare visual assets

**Files:**
- Create: `landing/assets/yanfu-portrait.png`
- Create: `landing/assets/manuscript-texture.png`
- Create: `landing/assets/cases/*.png`

- [ ] **Step 1: Generate the portrait and manuscript assets**

Generate a monochrome engraved Yan Fu portrait with transparent-looking paper background and a separate pale manuscript texture. Preserve the approved cool-gray, ink-black, and cinnabar art direction.

- [ ] **Step 2: Capture real case images**

Capture Let’s Pod and TransWeb translated pages from the existing local experiment. Use the Baoqingtian site and its real product card for the third case. Do not use placeholder rectangles.

- [ ] **Step 3: Verify asset dimensions and file integrity**

Run:

```bash
find landing/assets -type f -print0 | xargs -0 file
```

Expected: every file reports a valid PNG or JPEG image.

- [ ] **Step 4: Commit assets**

```bash
git add landing/assets
git commit -m "assets: add yanfu landing visuals"
```

### Task 3: Build the responsive page

**Files:**
- Create: `landing/index.html`

- [ ] **Step 1: Implement semantic HTML and responsive CSS**

Create the approved section order:

```html
<header>...</header>
<main>
  <section id="top">...</section>
  <section id="comparison">...</section>
  <section id="principles">...</section>
  <section id="process">...</section>
  <section id="cases">...</section>
  <section id="download">...</section>
</main>
<footer id="family">...</footer>
```

Use the approved copy, real family URLs, a disabled unpublished-download state, source/target comparison, horizontal principle rows, linear workflow, and three real before/after case pairs.

- [ ] **Step 2: Run tests and verify GREEN**

Run: `python3 -m unittest tests/test_landing.py -v`

Expected: all six tests pass.

- [ ] **Step 3: Validate HTML invariants**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
page = Path("landing/index.html").read_text(encoding="utf-8")
assert "<!doctype html>" in page.lower()
assert page.count("<h1") == 1
assert "TODO" not in page and "TBD" not in page
print("HTML invariants passed")
PY
```

Expected: `HTML invariants passed`.

- [ ] **Step 4: Commit the page**

```bash
git add landing/index.html
git commit -m "feat: build yanfu landing page"
```

### Task 4: Browser verification and design QA

**Files:**
- Create: `design-qa.md`
- Create: `.artifacts/yanfu-desktop.png`
- Create: `.artifacts/yanfu-mobile.png`

- [ ] **Step 1: Start the static server**

Run: `python3 -m http.server 4173 --bind 127.0.0.1`

Expected: server listens on `http://127.0.0.1:4173/landing/`.

- [ ] **Step 2: Verify desktop behavior**

At `1440px` width, verify:

- Hero and comparison match the selected visual hierarchy.
- All anchors scroll to valid sections.
- Four family links contain the exact production URLs.
- No horizontal overflow, clipped text, broken images, or fake download.

- [ ] **Step 3: Verify mobile behavior**

At `390px` width, verify:

- Header retains brand and download action without overlap.
- Hero title wraps without clipping.
- Comparison and cases become readable single-column stacks.
- Buttons and family links remain keyboard and touch accessible.

- [ ] **Step 4: Compare source and implementation**

Place the approved source image and desktop implementation screenshot in one comparison image. Review typography, spacing, colors, image quality, and copy. Fix every actionable P0/P1/P2 issue.

- [ ] **Step 5: Write passing QA report**

Write `design-qa.md` with source path, screenshot paths, viewport, comparison evidence, findings, fixes, residual P3 notes, and:

```text
final result: passed
```

- [ ] **Step 6: Run final verification**

Run:

```bash
python3 -m unittest tests/test_landing.py -v
git diff --check
```

Expected: all tests pass and `git diff --check` prints no errors.

- [ ] **Step 7: Commit QA artifacts**

```bash
git add design-qa.md .artifacts
git commit -m "test: verify yanfu landing page"
```
