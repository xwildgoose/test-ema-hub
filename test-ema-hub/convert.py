"""
1. Converts every document in  source/  into clean Markdown in  docs/documents/
   (Microsoft markitdown: PDF, Word, Excel, PowerPoint, txt -> Markdown).
2. Regenerates docs/documents/index.md -- a browsable catalog of every document
   with a short preview excerpt.

Runs automatically in the GitHub Action on every push. Hand-authored pages in
docs/ (index.md, clarion.md) are left alone. Scanned/image-only PDFs won't
extract -- those print a SKIP so you know to add a text version by hand.
"""
import re
from pathlib import Path
from markitdown import MarkItDown

SRC = Path("source")
OUT = Path("docs/documents")
SUPPORTED = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".csv", ".pptx", ".txt"}


def slug(stem: str) -> str:
    s = "".join(c if (c.isalnum() or c in "-_") else "-" for c in stem)
    return "-".join(p for p in s.split("-") if p).lower() or "document"


def convert_sources() -> None:
    if not SRC.exists():
        print("No source/ folder; skipping conversion.")
        return
    md = MarkItDown()
    n = 0
    for f in sorted(SRC.iterdir()):
        if not f.is_file() or f.suffix.lower() not in SUPPORTED:
            continue
        try:
            text = md.convert(str(f)).text_content
        except Exception as e:  # noqa: BLE001
            print(f"SKIP  {f.name}: {e}")
            continue
        (OUT / f"{slug(f.stem)}.md").write_text(
            f"# {f.stem}\n\n{text}\n", encoding="utf-8"
        )
        print(f"OK    {f.name} -> documents/{slug(f.stem)}.md")
        n += 1
    print(f"Converted {n} document(s).")


def _title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _excerpt(text: str, words: int = 35) -> str:
    body = "\n".join(l for l in text.splitlines() if not l.startswith("#"))
    body = re.sub(r"[`*_>#\[\]()!]", " ", body)
    body = re.sub(r"\s+", " ", body).strip()
    parts = body.split()
    return " ".join(parts[:words]) + ("…" if len(parts) > words else "")


def build_catalog() -> None:
    pages = []
    for f in sorted(OUT.glob("*.md")):
        if f.name == "index.md":
            continue
        text = f.read_text(encoding="utf-8")
        pages.append((_title(text, f.stem), f.name, _excerpt(text)))
    lines = [
        "# All Documents",
        "",
        "Use the **search box at the top** to find anything across every document "
        "(try a term like *tertiary grant*). This catalog lists what's currently in the hub.",
        "",
    ]
    for title, name, exc in pages:
        lines.append(f"- **[{title}]({name})** — {exc}")
    (OUT / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Catalog rebuilt: {len(pages)} document(s).")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    convert_sources()
    build_catalog()


if __name__ == "__main__":
    main()
