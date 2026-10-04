"""Build index.html - a local contact sheet of every figure in the book.

Open figures/index.html in a browser. No PDF toolchain needed.

Stepped figures (a folder of boards) are shown board by board, in the order
they appear on camera. Single-image figures are shown as one picture.
Figures the book references but that have never been drawn are listed too,
so the gaps are visible rather than merely absent.
"""

import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)

PARTS = [
    ("Part One — Foundation", range(1, 7), "Part-01-Foundation"),
    ("Part Two — Prompt Injection", range(7, 14), "Part-02-Prompt-Injection"),
    ("Part Three — Agentic Attacks", range(14, 23), "Part-03-Agentic-Attacks"),
]


def captions():
    """Pull every '**Figure N.N.** ...' caption out of the chapter text."""
    out = {}
    for _, _, folder in PARTS:
        for path in glob.glob(os.path.join(BOOK, folder, "Chapter*.md")):
            text = open(path, encoding="utf-8").read()
            for num, cap in re.findall(
                r"\*\*Figure (\d+\.\d+)\.\*\*\s*(.+?)(?:\n\n|\Z)", text, re.S
            ):
                out[num] = " ".join(cap.split())
    return out


def figure_number(stem):
    m = re.match(r"(\d+)-(\d+)", stem)
    return f"{int(m.group(1))}.{int(m.group(2))}" if m else None


def boards(stem):
    """Board files for a stepped figure, in display order: index, 1, 2, ..."""
    folder = os.path.join(HERE, stem)
    if not os.path.isdir(folder):
        return []
    found = [os.path.basename(p) for p in glob.glob(os.path.join(folder, "*.png"))]
    numbered = sorted(
        (f for f in found if f != "index.png"),
        key=lambda f: int(os.path.splitext(f)[0]),
    )
    return (["index.png"] if "index.png" in found else []) + numbered


def collect():
    figs = {}
    for path in glob.glob(os.path.join(HERE, "*.d2")):
        stem = os.path.splitext(os.path.basename(path))[0]
        num = figure_number(stem)
        if not num:
            continue
        figs[num] = {"stem": stem, "boards": boards(stem),
                     "single": os.path.exists(os.path.join(HERE, stem + ".png"))}
    return figs


CSS = """
:root{--bg:#ffffff;--fg:#1a1a1f;--muted:#6b6b76;--line:#e3e3e8;--card:#fafafa;--warn:#c14545}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){
  --bg:#141418;--fg:#ececf0;--muted:#9a9aa6;--line:#2c2c34;--card:#1c1c22}}
*{box-sizing:border-box}
body{margin:0;padding:40px 16px 80px;background:var(--bg);color:var(--fg);
  font:16px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:1100px;margin:0 auto}
h1{font-size:28px;margin:0 0 6px}
.sub{color:var(--muted);margin:0 0 36px}
h2{font-size:20px;margin:48px 0 4px;padding-bottom:8px;border-bottom:2px solid var(--line)}
.count{color:var(--muted);font-size:14px;font-weight:400}
.fig{margin:30px 0 10px;padding:18px;background:var(--card);
  border:1px solid var(--line);border-radius:10px}
.fig h3{margin:0 0 4px;font-size:17px}
.cap{color:var(--muted);font-size:14px;margin:0 0 14px}
.boards{display:flex;flex-direction:column;gap:14px}
.board{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fff}
.board .lbl{font:12px ui-monospace,monospace;letter-spacing:.04em;color:var(--muted);
  padding:7px 10px;border-bottom:1px solid var(--line);background:var(--card)}
.board img{display:block;width:100%;height:auto}
.missing{border-style:dashed;border-color:var(--warn)}
.missing h3{color:var(--warn)}
.tag{display:inline-block;font:11px ui-monospace,monospace;letter-spacing:.05em;
  padding:3px 7px;border-radius:5px;border:1px solid var(--line);color:var(--muted);
  margin-left:8px;vertical-align:middle}
@media(max-width:700px){body{padding:24px 12px 60px}}
"""


def main():
    caps = captions()
    figs = collect()
    html = ["<!doctype html><html lang=en><meta charset=utf-8>",
            "<meta name=viewport content='width=device-width,initial-scale=1'>",
            "<title>Figure Gallery</title>", f"<style>{CSS}</style>",
            "<div class=wrap>",
            "<h1>Figure Gallery</h1>",
            "<p class=sub>Every diagram in the book. Stepped figures show each board "
            "in the order it appears on camera. Regenerate with "
            "<code>python make-gallery.py</code>.</p>"]

    for title, chapters, _ in PARTS:
        nums = sorted((n for n in caps if int(n.split(".")[0]) in chapters),
                      key=lambda n: [int(x) for x in n.split(".")])
        have = sum(1 for n in nums if n in figs)
        html.append(f"<h2>{title} <span class=count>— {have} of {len(nums)} drawn</span></h2>")

        for num in nums:
            cap = caps.get(num, "")
            if num not in figs:
                html.append(
                    f"<div class='fig missing'><h3>Figure {num}"
                    f"<span class=tag>NOT DRAWN — ASCII only</span></h3>"
                    f"<p class=cap>{cap}</p></div>")
                continue

            f = figs[num]
            bs = f["boards"]
            tag = (f"<span class=tag>{len(bs)} boards</span>" if bs
                   else "<span class=tag>single</span>")
            html.append(f"<div class=fig><h3>Figure {num}{tag}</h3>"
                        f"<p class=cap>{cap}</p><div class=boards>")
            if bs:
                for i, b in enumerate(bs):
                    lbl = "board 0 (opening)" if b == "index.png" else f"board {i}"
                    html.append(f"<div class=board><div class=lbl>{lbl} &middot; "
                                f"{f['stem']}/{b}</div>"
                                f"<img loading=lazy src='{f['stem']}/{b}' alt='Figure {num}'></div>")
            else:
                html.append(f"<div class=board><div class=lbl>{f['stem']}.png</div>"
                            f"<img loading=lazy src='{f['stem']}.png' alt='Figure {num}'></div>")
            html.append("</div></div>")

    html.append("</div></html>")
    out = os.path.join(HERE, "index.html")
    open(out, "w", encoding="utf-8").write("\n".join(html))

    drawn = len(figs)
    total = len(caps)
    print(f"wrote {out}")
    print(f"  {drawn} of {total} referenced figures are drawn")
    print(f"  {sum(len(f['boards']) for f in figs.values())} stepped boards")


if __name__ == "__main__":
    main()
