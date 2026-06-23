---
name: yanfu
description: Use when a developer provides an existing public Landing Page and 1–5 product screenshots and wants the structure and copy translated into a clearer user-facing landing page without changing positioning or inventing claims.
---

# 严复 Skill

## Purpose

Translate a developer-view Landing Page into a page users can understand and retell quickly.

Apply three principles:

- **信:** preserve product facts, original positioning, and real capabilities.
- **达:** translate features and mechanisms into visible user actions and results.
- **雅:** improve structure, rhythm, and clarity without letting style outrun evidence.

The core rule is: **preserve the product, translate the story.**

## Required Input

Require both:

1. One public Landing Page URL.
2. 1–5 core product screenshots.

Optional input:

- The one idea the developer most wants users to understand.
- The primary CTA and its real destination.
- Logo, fonts, or other brand assets.
- Content that must remain unchanged.

Handle incomplete input narrowly:

- **Only URL:** request 1–5 core product screenshots; do not register or log in.
- **Only screenshots:** request the public Landing Page URL.
- Inaccessible page, unrelated screenshots, or unclear value proposition: stop and request only the minimum missing evidence.

Do not use generic marketing knowledge to fill product-fact gaps.

## Scope Boundaries

- Do not reposition the product.
- Do not change the target audience.
- Do not invent claims, metrics, testimonials, customers, or capabilities.
- Do not perform competitor analysis.
- Do not judge whether the product should exist.
- Do not broadly redesign the visual identity.
- Do not independently generate pitch decks or multiple pitch lengths in v0.1.

Preserve the brand name, logo, main colors, typography character, product screenshots, component language, real CTA, and overall visual personality by default.

Adjust only the story hierarchy, section order, copy, screenshot emphasis, whitespace, and restrained accessibility or responsive fixes.

## Workflow

### 1. Confirm Evidence

Read [references/evidence-and-browsing.md](references/evidence-and-browsing.md).

Inspect the public page and provided screenshots. Separate:

- Explicit page claims.
- Facts visibly supported by product screenshots.
- Developer-supplied facts.
- Unverified assumptions.

Do not proceed to final output when the core product promise cannot be supported.

### 2. Extract the Original Story

Record:

- Product definition.
- Stated user.
- Core value proposition.
- Features and usage mechanism.
- User results.
- Proof, metrics, testimonials, and customers.
- Primary CTA and real links.
- Brand and visual elements.

Treat every claim as unverified until its source is known.

### 3. Build the Translation Ledger

Read [references/translation-method.md](references/translation-method.md).

Create an internal translation ledger before writing the page. Every important new expression must have:

- New expression.
- Source evidence.
- Treatment.
- Confidence.

Exclude unsupported expressions from `landing.html`. Put unresolved items under `待确认` in the notes.

### 4. Reorder the Story

Start with this default sequence:

> Hero → user situation → product mechanism → core interface → user result → proof → FAQ → CTA

Delete or reorder sections when the evidence calls for it. Never add a section merely to complete the template.

Prefer a concrete, repeatable expression over a technical category description. Translate through:

> Feature → User action → User result → Repeatable expression

### 5. Build the Landing Page

Read [references/output-spec.md](references/output-spec.md).

Create a responsive, directly openable `landing.html`.

Requirements:

- Use original legally accessible brand assets and provided product screenshots.
- Keep real links and CTA destinations working.
- Keep one clear H1 and a legible first viewport.
- Show product evidence early enough to support the main promise.
- Remove repeated features, empty slogans, unsupported outcomes, premature implementation detail, and distracting decoration.
- Do not expose the internal ledger, confidence labels, or consulting language in the page.

### 6. Write the Translation Notes

Create `yanfu-notes.md` with the exact top-level sections:

- `信`
- `达`
- `雅`
- `待确认`

Keep it concise, normally about one page. Explain consequential preservation, rewriting, deletion, and restrained visual changes.

### 7. Validate and Preview

Run:

```bash
python3 /path/to/yanfu/scripts/validate_delivery.py /path/to/output
```

Fix every reported error.

When a browser is available:

- Open the generated page.
- Check desktop and mobile layouts.
- Verify CTA links and local assets.
- Check for overflow, overlap, unreadable screenshots, and broken hierarchy.

Do not claim completion from source inspection alone.

## Delivery

Return:

1. The local preview link or path to `landing.html`.
2. The path to `yanfu-notes.md`.
3. One short sentence naming anything the developer must still confirm.

Return the page first. Do not paste the full HTML into chat unless the user explicitly asks for source code.

## Quick Reference

| Situation | Action |
| --- | --- |
| Page and screenshots are complete | Start immediately |
| Page exists, screenshots missing | Request 1–5 screenshots |
| Screenshots exist, page missing | Request the public URL |
| Page requires login | Ask for an exported page, article, or screenshots |
| Claim lacks evidence | Omit from page; list under `待确认` |
| Original design is usable | Preserve it and change structure/copy |
| Original design blocks comprehension | Make the smallest necessary visual fix |

## Common Mistakes

- Diagnosing positioning instead of translating expression.
- Replacing the product's words with generic startup copy.
- Treating a visible interface as proof of speed, accuracy, or satisfaction.
- Inventing an ideal user story not supported by the source.
- Redesigning the brand because a cleaner style is possible.
- Delivering commentary instead of a usable HTML page.
