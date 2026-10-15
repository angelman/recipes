# Recipes

A personal recipe collection — every recipe Scout has made for Angel,
published as a plain static site (no build step, no dependencies).

## View it

Enable GitHub Pages: repo **Settings → Pages → Source: Deploy from a
branch → Branch: main, /(root) → Save**. The site will be live at
`https://angelman.github.io/recipes/` (the repo is public, so Pages works
on a free GitHub account).

## Add a recipe

1. Append an entry to `recipes.json` (copy an existing entry's shape:
   `slug`, `title`, `servings`, `nutrition`, `ingredients`, `steps`,
   `notes`, `tags`, `cooked`, `delivered`, `intro`, `attribution`).
2. Run `python3 build.py` to regenerate `index.html` and the recipe pages.
3. Commit everything.

## Files

- `index.html` — generated index page with search + tag filters.
- `recipes/*.html` — generated one page per recipe. Each page carries
  Schema.org `Recipe` structured data (JSON-LD) for portability.
- `recipes.json` — the source of truth for all recipes.
- `build.py` — regenerates the pages from `recipes.json`.
- `assets/` — stylesheet and client-side search script.
