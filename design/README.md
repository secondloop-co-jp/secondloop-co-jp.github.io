# Figma and code coordination

The source file is [Corporate Website](https://www.figma.com/design/HVfBJvdRq2H356JIguk7Kh/Corporate-Website), page `Website`, file key `HVfBJvdRq2H356JIguk7Kh`.

| Figma source | Node / role | Code |
| --- | --- | --- |
| Desktop | `1:194`, 1440 × 2112 | `index.html`, desktop rules in `assets/site.css` |
| Mobile | `1:256`, 390 × 2368 | mobile rules in `assets/site.css` |
| Foundations | `1:322` | `handoff.json`, generated `assets/tokens.css` |
| `Website foundations` collection | 11 numeric variables, stable IDs in export | `figma/website-foundations.tokens.json` |
| `action/primary-link` | desktop master, mobile linked instance | `.primary-link` |
| `color/*` paint styles | six shared colors | `handoff.json` → CSS variables |
| `type/*` text styles | eight shared roles | `handoff.json` → CSS variables |

The original export is preserved with Figma variable IDs. `handoff.json` records typography, color styles, component dimensions and which variables are actually bound. Not every position in Figma is Auto Layout or bound to variables. The implementation uses responsive document flow, so intermediate widths and text expansion are handled by CSS rather than absolute Figma coordinates.

## Update procedure

1. Edit this same Figma file. Review both frames and the shared component/styles. Keep approved company information current.
2. In Variables, export the `Website foundations` collection mode as JSON. This is a manual export; no Figma token, API subscription or permission change is needed.
3. Save the downloaded export outside the tracked source and run:

   ```sh
   python3 scripts/design_tokens.py --import-export /absolute/path/to/export.tokens.json
   ```

   The command prints old/new values, validates numeric values and stable IDs, updates the native export, and regenerates `assets/tokens.css`. Token removals/renames or variable-ID changes stop the import. Review their CSS references and mappings first; use `--allow-schema-change` only after that review. Inspect the Git diff before committing.
4. Color and typography are native Figma **styles**, so they are not contained in the number export. Compare changed style definitions with `handoff.json`, edit those records, then run `python3 scripts/design_tokens.py`. Font-family changes also require manually updating the font stack in `assets/site.css` and the Google Fonts stylesheet URL in `index.html`; the generator covers size and line-height, not font loading. Update one-off layout rules in `assets/site.css` deliberately. Export both final frames as PNG for visual review.
5. Complete the checklist below and include the Figma nodes, changed values, screenshots and check results in the pull request. Do not put private Notion links, internal notes or credentials into the public repository.

## Review checklist

- Compare desktop 1440 and mobile 390 with the latest exported frames: hierarchy, spacing, logo/screenshot, Japanese line breaks, company details, restrained email treatment.
- Check 320, 390, 600, 768, 1024 and 1440 CSS pixels; no horizontal overflow, overlap or clipped text. Check 200% zoom and intermediate reflow.
- Navigate using Tab/Shift+Tab/Enter: skip link, brand, section links, service CTA and email. Focus stays visible. Navigation, CTA and email targets are at least 44px high.
- Verify ImageBGM opens the correct HTTPS service, internal section links resolve, and email is `mailto:contact@secondloop.co.jp` without submitting a message.
- Review semantic headings, image alternatives, text contrast and font fallback. Color ratios are recorded in `handoff.json`; those ratios alone do not establish full accessibility conformance.
- Run token and site checks, review the final commit's CI, and check GitHub Pages deployment plus the live page after merging.

## Scope of automation

CI compares committed JSON to committed generated CSS. It cannot see unexported edits in Figma, detect screenshot/content/layout changes, infer new variables, or synchronize code back to Figma. Color/type comparison and visual review remain manual. Any future API integration should be proposed separately with its required access and cost.
