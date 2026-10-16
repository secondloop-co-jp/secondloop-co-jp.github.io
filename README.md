# Second Loop corporate website

The public one-page website at <https://secondloop.co.jp/>. GitHub Pages publishes `main` from `/`; keep `CNAME` unchanged. No build step or JavaScript runtime is required for production.

## Local preview and checks

```sh
python3 -m http.server 8873 --bind 127.0.0.1
# Open http://127.0.0.1:8873/
python3 scripts/design_tokens.py --check
python3 scripts/check_site.py
git diff --check
```

`Site checks` runs the same checks on pull requests and `main`. It catches stale generated tokens, broken local asset/anchor references, missing image metadata, undefined CSS variables and basic semantic regressions. It does not replace browser, accessibility or Figma review.

## Design source and updates

Use the existing [Corporate Website Figma file](https://www.figma.com/design/HVfBJvdRq2H356JIguk7Kh/Corporate-Website). Keep its identity when making future changes. See [design/README.md](design/README.md) for the mapping, import procedure and review checklist.

The favicon and Apple touch icon retain the white-background assets from [Second Loop logo v1.0.0](https://github.com/secondloop-co-jp/logo/releases/tag/v1.0.0). `assets/imagebgm-logo.png` is the existing ImageBGM launch-record logo; `assets/imagebgm-screen.jpg` is the centered current service screenshot used in Figma. Their source is <https://imagebgm.secondloopapps.com/>. Refresh these deliberately when the service UI changes.

Noto Sans JP is requested from Google Fonts with `display=swap`. Local Japanese system fonts remain available when the font request is blocked. The page does not use analytics or client-side JavaScript.
