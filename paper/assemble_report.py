#!/usr/bin/env python3
"""Assemble the PS-PIR internal report from its ordered section sources."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
SECTIONS = [
    ROOT / "sections/01-abstract.md",
    ROOT / "sections/02-introduction.md",
    ROOT / "sections/03-related-work.md",
    ROOT / "sections/04-methodology.md",
    ROOT / "sections/05-experimental-setup.md",
    ROOT / "sections/06-results.md",
    ROOT / "sections/07-discussion.md",
    ROOT / "sections/08-conclusion.md",
    ROOT / "sections/09-references.md",
    ROOT / "sections/10-supplementary.md",
]
OUTPUT = ROOT / "orf-internal-technical-report.md"


def main() -> None:
    missing = [str(path.relative_to(ROOT.parent)) for path in SECTIONS if not path.is_file()]
    if missing:
        raise SystemExit(f"missing sections: {missing}")
    text = "\n\n".join(path.read_text(encoding="utf-8").strip() for path in SECTIONS)
    OUTPUT.write_text(text + "\n", encoding="utf-8", newline="\n")
    print(f"assembled={OUTPUT.relative_to(ROOT.parent)} sections={len(SECTIONS)} lines={len(text.splitlines())}")


if __name__ == "__main__":
    main()
