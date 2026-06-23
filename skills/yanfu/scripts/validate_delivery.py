#!/usr/bin/env python3
"""Validate a Yanfu v0.1 landing-page delivery."""

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
        errors.append("missing required file: landing.html")
    if not notes_path.is_file():
        errors.append("missing required file: yanfu-notes.md")
    if errors:
        return errors

    html = landing_path.read_text(encoding="utf-8")
    parser = LandingParser()
    parser.feed(html)

    if not parser.has_viewport:
        errors.append("landing.html missing viewport meta")
    if parser.h1_count != 1:
        errors.append(
            "landing.html must contain exactly one h1 "
            f"(found {parser.h1_count})"
        )

    for resource in parser.local_resources:
        clean_path = resource.split("?", 1)[0].split("#", 1)[0]
        if not (output_dir / clean_path).is_file():
            errors.append(f"missing local asset: {resource}")

    notes = notes_path.read_text(encoding="utf-8")
    for section in REQUIRED_NOTES_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", notes, re.MULTILINE):
            errors.append(f"missing notes section: {section}")

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate landing.html and yanfu-notes.md.",
    )
    parser.add_argument("output_dir", help="Directory containing the Yanfu delivery")
    args = parser.parse_args()

    errors = validate(args.output_dir)
    if errors:
        print("Yanfu delivery invalid:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Yanfu delivery valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
