#!/usr/bin/env python3
"""校验严复 v0.1 的 Landing Page 交付目录。"""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlparse


REQUIRED_NOTES_SECTIONS = ("信", "达", "雅", "待确认")


class LandingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_count = 0
        self.has_viewport = False
        self.local_resources = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and attributes.get("name", "").lower() == "viewport":
            self.has_viewport = bool(attributes.get("content", "").strip())

        resource = None
        if tag in {"img", "script", "source", "video", "audio"}:
            resource = attributes.get("src")
        elif tag == "link":
            resource = attributes.get("href")

        if resource and self._is_local_resource(resource):
            self.local_resources.append(resource)

    @staticmethod
    def _is_local_resource(value):
        value = value.strip()
        if not value or value.startswith(("#", "data:", "mailto:", "tel:", "javascript:")):
            return False
        return not urlparse(value).scheme and not value.startswith("//")


def validate(output_dir):
    output_dir = Path(output_dir).resolve()
    errors = []
    landing_path = output_dir / "landing.html"
    notes_path = output_dir / "yanfu-notes.md"

    if not landing_path.is_file():
        errors.append("缺少必需文件：landing.html")
    if not notes_path.is_file():
        errors.append("缺少必需文件：yanfu-notes.md")
    if errors:
        return errors

    html = landing_path.read_text(encoding="utf-8")
    parser = LandingParser()
    parser.feed(html)

    if not parser.has_viewport:
        errors.append("landing.html 缺少 viewport meta")
    if parser.h1_count != 1:
        errors.append(
            "landing.html 必须且只能包含一个 h1 "
            f"（当前为 {parser.h1_count} 个）"
        )

    for resource in parser.local_resources:
        clean_path = resource.split("?", 1)[0].split("#", 1)[0]
        if not (output_dir / clean_path).is_file():
            errors.append(f"缺少本地资源：{resource}")

    notes = notes_path.read_text(encoding="utf-8")
    for section in REQUIRED_NOTES_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", notes, re.MULTILINE):
            errors.append(f"译注缺少章节：{section}")

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="校验 landing.html 与 yanfu-notes.md。",
    )
    parser.add_argument("output_dir", help="包含严复交付文件的目录")
    args = parser.parse_args()

    errors = validate(args.output_dir)
    if errors:
        print("严复交付校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print("严复交付校验通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
