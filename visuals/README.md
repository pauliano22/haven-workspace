# Visuals

- `haven_ear_explorer.html`: interactive 3D explorer of the v2 shape concepts in a scanned ear
  (HUTUBS pp3, CC BY 4.0, three.js). Published at https://claude.ai/artifact/Efp6ajujduH5kyyy33Yrv7 —
  republish from this file to update it. Opens on the side cut-away; the website copy
  (`website/explorer/index.html`, branch `redesign/sanctuary`) opens on the full outer ear.

## Adding or changing a shape concept

1. `tools/build_concepts.py` lists the concepts (shell STL, part frames, pp3 fit pose, README stats,
   pro/con). It reuses the ear and cut-away cap embedded in the previous explorer, so the HUTUBS
   scans aren't needed. Outputs go to `build/` (git-ignored).
2. `tools/patch_concepts.py` writes the assets into the explorer.
3. `tools/check_explorer.js` loads it headless at desktop and 400 px and switches every concept.

```
python3 - <<'PY'   # extract the previous build's embedded assets into build/prev_assets.{glb,json}
PY
python3 tools/build_concepts.py build/prev_assets.glb build/prev_assets.json <hardware>/mechanical_cad/v2_ergonomic_shell <form-concepts worktree>/mechanical_cad/v2_form_concepts build/assets_concepts.glb build/assets_concepts.json
python3 tools/patch_concepts.py build/prev_explorer.html build/assets_concepts.glb build/assets_concepts.json haven_ear_explorer.html
```
