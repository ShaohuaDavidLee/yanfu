# Output Specification

## Output Folder

Produce:

```text
output/
├── landing.html
├── yanfu-notes.md
└── assets/                 # only when local assets are needed
```

`landing.html` may also reference user-provided assets outside `assets/` when the final folder remains portable and all paths resolve.

## landing.html

Requirements:

- Single responsive HTML entry point.
- `lang` attribute and viewport metadata.
- Exactly one H1.
- Clear product identity, user value, and primary CTA in the first viewport.
- Original brand character and real product screenshots.
- Working primary links and local assets.
- No internal confidence labels or translation commentary.
- No invented metrics, testimonials, customer logos, or capabilities.
- No unnecessary framework or build step when plain HTML/CSS is sufficient.

The exact section order varies by evidence. Prefer:

> Hero → situation → mechanism → interface → result → proof → FAQ → CTA

## yanfu-notes.md

Use this structure:

```markdown
# 严复译注

## 信
- 原始价值主张：
- 忠实保留：
- 表达依据：
- 因证据不足未使用：

## 达
- 最终一句话 Pitch：
- 故事主线：
- 信息顺序调整：
- 删除、合并或弱化：

## 雅
- 保留的设计元素：
- 产品截图选择：
- 必要且克制的视觉修正：

## 待确认
- 需要开发者确认：
- 暂未进入页面：
```

Keep notes concise. Use `无` when a subsection has no items.

## Completion Message

Return:

1. `landing.html` preview/path.
2. `yanfu-notes.md` path.
3. One sentence containing the highest-priority confirmation, or state that no confirmation remains.

Do not replace file delivery with a long critique.
