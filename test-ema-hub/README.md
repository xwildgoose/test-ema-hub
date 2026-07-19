# EMA Knowledge Hub

A single website that holds all the content the **EMA chatbot** (FastBots) is trained on.
FastBots crawls this site on a schedule, so updating the bot means editing a page here —
no re-uploading files, no manual retrain.

## How it works

```
source/            <- drop raw PDFs / Word / Excel here (auto-converted)
docs/
  index.md         <- landing page (hand-authored)
  clarion.md       <- weekly Clarion announcements (hand-authored, pasted)
  documents/       <- Markdown auto-generated from source/ by convert.py
mkdocs.yml         <- site config
convert.py         <- documents -> Markdown (Microsoft markitdown)
.github/workflows/deploy.yml   <- on every push: convert -> build -> publish to Pages
```

On every push, the GitHub Action converts anything in `source/`, builds the Markdown into a
website (MkDocs) with an auto-generated `sitemap.xml`, and publishes it to GitHub Pages.

## One-time setup

1. Create a GitHub repo named `ema-hub` and add these files (drag-and-drop in the web UI is fine).
2. In **Settings -> Pages**, set **Source = GitHub Actions**.
3. Edit `mkdocs.yml` and set `site_url` to your Pages URL (`https://YOURUSERNAME.github.io/ema-hub/`).
4. Add your documents: drop the files into `source/`, or commit ready-made `.md` files into `docs/documents/`.
5. Commit. The Action runs and publishes the site. Your sitemap is at
   `https://YOURUSERNAME.github.io/ema-hub/sitemap.xml`.

## Point FastBots at it

1. In FastBots, add a **Website** source using the Pages URL (or the `sitemap.xml` URL).
2. Set **Auto Retrain** to weekly (or daily).
3. **Delete the old individual document uploads** from FastBots so nothing is indexed twice.

## Ongoing

- New/updated document: drop it in `source/` (or edit the `.md`) via github.com, commit, done.
- New Clarion: paste the week's relevant text into `docs/clarion.md`, prune expired items, commit.

## Finding things (search)

The published site has a **search box in the top bar** (built into the theme, no backend).
Type a term like `tertiary grant` and it instantly lists every document that mentions it,
with a highlighted preview excerpt — so you never have to open files one by one to find
where something lives. The **All Documents** page is an auto-generated catalog of every
document with a short preview, rebuilt on each commit.

Note: search runs on the *published* (public) site, so keep internal-only material out of
the hub — those stay as private FastBots uploads.
