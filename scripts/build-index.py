#!/usr/bin/env python3
from __future__ import annotations

import html
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_INDEX = ROOT / "index.html"
START = "<!-- AUTO_INDEX_START -->"
END = "<!-- AUTO_INDEX_END -->"


class MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title_parts: list[str] = []
        self.description = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self.in_title = True
            return
        if tag.lower() != "meta":
            return
        values = {key.lower(): value or "" for key, value in attrs}
        if values.get("name", "").lower() == "description":
            self.description = values.get("content", "").strip()

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())


def read_meta(path: Path) -> tuple[str, str]:
    parser = MetaParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.title, parser.description


def discover_pages() -> list[tuple[str, str, str]]:
    pages: list[tuple[str, str, str]] = []
    for path in ROOT.rglob("index.html"):
        if path == ROOT_INDEX:
            continue
        relative = path.relative_to(ROOT)
        if any(part.startswith(".") for part in relative.parts):
            continue
        title, description = read_meta(path)
        if not title:
            continue
        href = "./" + relative.parent.as_posix().rstrip("/") + "/"
        pages.append((title, description, href))
    return sorted(pages, key=lambda item: item[0].casefold())


def render(pages: list[tuple[str, str, str]]) -> str:
    if not pages:
        return '        <p class="empty">아직 등록된 페이지가 없습니다.</p>'

    cards = []
    for title, description, href in pages:
        body = (
            f'<p>{html.escape(description)}</p>'
            if description
            else f'<p class="path">{html.escape(href.removeprefix("./"))}</p>'
        )
        cards.append(
            "\n".join(
                [
                    f'        <a class="card" href="{html.escape(href, quote=True)}">',
                    f"          <h2>{html.escape(title)}</h2>",
                    f"          {body}",
                    "        </a>",
                ]
            )
        )
    return "\n".join(cards)


def main() -> None:
    source = ROOT_INDEX.read_text(encoding="utf-8")
    if START not in source or END not in source:
        raise SystemExit("index.html is missing auto-index markers")

    before, rest = source.split(START, 1)
    _, after = rest.split(END, 1)
    generated = render(discover_pages())
    output = f"{before}{START}\n{generated}\n        {END}{after}"
    ROOT_INDEX.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
