#!/usr/bin/env python3
"""Generate the static recipe site from recipes.json.

Usage: python3 build.py
Writes index.html and recipes/<slug>.html in this directory.
To add a recipe: append an entry to recipes.json and re-run this script.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return html.escape(str(s))


def tag_chips(tags):
    return "".join(
        f'<span class="tag">{esc(t)}</span>' for t in tags
    )


def json_ld(r):
    """Schema.org Recipe structured data (JSON-LD) for a recipe entry."""
    import json as _json

    data = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": r["title"],
        "description": r["intro"],
        "recipeIngredient": r["ingredients"],
        "recipeInstructions": [
            {"@type": "HowToStep", "text": s} for s in r["steps"]
        ],
    }
    servings = r.get("servings") or ""
    if servings and servings != "See notes":
        data["recipeYield"] = servings
    if r.get("source_url"):
        data["isBasedOn"] = r["source_url"]
    # Escape any "</" sequences so the JSON can never break out of <script>.
    return _json.dumps(data, ensure_ascii=True).replace("</", "<\\/")


def recipe_page(r):
    nutrition = (
        f'<p class="meta-line"><strong>Per serving:</strong> {esc(r["nutrition"])}</p>'
        if r.get("nutrition")
        else ""
    )
    attribution = (
        f'<p class="attribution">{esc(r["attribution"])}</p>'
        if r.get("attribution")
        else ""
    )
    source = ""
    if r.get("source_url"):
        from urllib.parse import urlparse

        domain = urlparse(r["source_url"]).netloc.replace("www.", "")
        source = (
            f'<p class="source">Source: '
            f'<a href="{esc(r["source_url"])}">{esc(domain)}</a></p>'
        )
    cooked = (
        '<span class="badge cooked">Cooked ✓</span>' if r.get("cooked") else ""
    )
    ingredients = "".join(f"<li>{esc(i)}</li>" for i in r["ingredients"])
    steps = "".join(f"<li>{esc(s)}</li>" for s in r["steps"])
    notes = ""
    if r.get("notes"):
        notes = "<h2>Notes</h2><ul>" + "".join(
            f"<li>{esc(n)}</li>" for n in r["notes"]
        ) + "</ul>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(r["title"])} — Recipes</title>
<link rel="stylesheet" href="../assets/style.css">
<script type="application/ld+json">{json_ld(r)}</script>
</head>
<body>
<main class="recipe-page">
<p class="back"><a href="../index.html">← All recipes</a></p>
<h1>{esc(r["title"])} {cooked}</h1>
<p class="meta-line"><strong>Servings:</strong> {esc(r["servings"])}</p>
{nutrition}
<p class="meta-line"><strong>From:</strong> {esc(r["delivered"])}</p>
{attribution}
{source}
<div class="tags">{tag_chips(r["tags"])}</div>
<p class="intro">{esc(r["intro"])}</p>
<h2>Ingredients</h2>
<ul class="ingredients">{ingredients}</ul>
<h2>Steps</h2>
<ol class="steps">{steps}</ol>
{notes}
<p class="back"><a href="../index.html">← All recipes</a></p>
</main>
</body>
</html>
"""


def index_page(recipes):
    cards = []
    for r in recipes:
        cooked = (
            '<span class="badge cooked">Cooked ✓</span>' if r.get("cooked") else ""
        )
        nutrition = esc(r["nutrition"]) if r.get("nutrition") else ""
        search_text = esc(
            " ".join(
                [r["title"], " ".join(r["tags"]), " ".join(r["ingredients"])]
            ).lower()
        )
        cards.append(f"""<article class="card" data-search="{search_text}">
<a href="recipes/{esc(r["slug"])}.html"><h2>{esc(r["title"])}</h2></a>
<p class="card-meta">{esc(r["servings"])} · {nutrition} {cooked}</p>
<p class="card-intro">{esc(r["intro"])}</p>
<div class="tags">{tag_chips(r["tags"])}</div>
</article>""")
    all_tags = sorted({t for r in recipes for t in r["tags"]})
    tag_buttons = "".join(
        f'<button class="tag-filter" data-tag="{esc(t)}">{esc(t)}</button>'
        for t in all_tags
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Recipes</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<main>
<header>
<h1>Recipes</h1>
<p class="subtitle">Every recipe Scout has made for Angel — {len(recipes)} recipes, all in one place.</p>
</header>
<div class="search-wrap">
<input id="search" type="search" placeholder="Search recipes, ingredients, tags…" aria-label="Search recipes">
</div>
<div class="tag-row">
<button class="tag-filter active" data-tag="">All</button>
{tag_buttons}
</div>
<p id="no-results" hidden>No recipes match your search.</p>
<div class="grid">
{''.join(cards)}
</div>
<footer><p>Search filters by title, ingredient, and tag. Click a recipe for the full version.</p></footer>
</main>
<script src="assets/search.js"></script>
</body>
</html>
"""


def main():
    with open(os.path.join(HERE, "recipes.json")) as f:
        data = json.load(f)
    recipes = data["recipes"]
    with open(os.path.join(HERE, "index.html"), "w") as f:
        f.write(index_page(recipes))
    outdir = os.path.join(HERE, "recipes")
    os.makedirs(outdir, exist_ok=True)
    for r in recipes:
        with open(os.path.join(outdir, r["slug"] + ".html"), "w") as f:
            f.write(recipe_page(r))
    print(f"Built index + {len(recipes)} recipe pages.")


if __name__ == "__main__":
    main()
