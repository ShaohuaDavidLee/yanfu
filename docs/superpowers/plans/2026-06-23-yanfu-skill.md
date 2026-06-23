# Yanfu Skill v0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an installable `yanfu` skill that translates an existing public landing page into a clearer responsive HTML page and a concise evidence-backed translation note.

**Architecture:** Keep the main workflow in `skills/yanfu/SKILL.md`. Move evidence rules, translation method, and output details into focused references loaded only when needed. Add a deterministic Python validator for the two-file delivery contract and Python tests for the skill metadata, scope boundaries, workflow, and validator behavior.

**Tech Stack:** Agent Skills Markdown/YAML, Python 3 standard library, HTML5.

---

### Task 1: Define the skill contract with failing tests

**Files:**
- Create: `tests/test_skill.py`

- [ ] Write tests asserting the required metadata, input behavior, scope boundaries, evidence ledger, output filenames, references, and delivery validator.
- [ ] Run `python3 -m unittest tests/test_skill.py -v`.
- [ ] Verify failure occurs because `skills/yanfu/` does not exist.
- [ ] Commit the tests.

### Task 2: Initialize and implement the skill package

**Files:**
- Create: `skills/yanfu/SKILL.md`
- Create: `skills/yanfu/agents/openai.yaml`
- Create: `skills/yanfu/assets/yanfu-icon.png`
- Create: `skills/yanfu/references/evidence-and-browsing.md`
- Create: `skills/yanfu/references/translation-method.md`
- Create: `skills/yanfu/references/output-spec.md`
- Create: `skills/yanfu/scripts/validate_delivery.py`

- [ ] Run `init_skill.py yanfu --path skills --resources scripts,references,assets` with Yanfu interface metadata.
- [ ] Replace generated placeholders with the v0.1 workflow and references.
- [ ] Copy the approved Yanfu portrait into the skill assets.
- [ ] Implement `validate_delivery.py` with checks for both required output files, responsive metadata, one H1, local resource existence, and required notes headings.
- [ ] Run `python3 -m unittest tests/test_skill.py -v` and verify all tests pass.
- [ ] Commit the skill implementation.

### Task 3: Validate packaging and a representative delivery

**Files:**
- Create temporarily under the system temp directory: valid and invalid delivery fixtures.

- [ ] Run `quick_validate.py skills/yanfu`.
- [ ] Run `validate_delivery.py` against a valid fixture and expect exit code 0.
- [ ] Run it against an invalid fixture and expect non-zero exit code with actionable errors.
- [ ] Scan the skill for placeholders and inconsistent filenames.
- [ ] Run the complete test suite and `git diff --check`.
- [ ] Commit any validation fixes.
