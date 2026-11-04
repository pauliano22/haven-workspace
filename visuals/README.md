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
3. `tools/seat_concepts.py` re-seats every concept in pp3 for display with a hard limit (≤ 1.0 mm into
   skin, canal entrance excluded); concepts that can't meet it keep their least-bad pose and the
   overlap is coloured red. It also settles the behind-the-ear pod on the scalp behind the pinna.
   `tools/route_cable.py` then routes the BTE cable through free space (A* on a voxel grid, ≥ 1.1 mm
   off the skin at every sample and segment midpoint) and smooths it.
4. `tools/shoot_review.js` renders every concept from out / side / close / below / front for review;
   `tools/check_explorer.js` loads it headless at desktop and 400 px and switches every concept.

```
cp haven_ear_explorer.html build/prev_explorer.html
python3 -c "import re,base64,json; s=open('build/prev_explorer.html').read(); open('build/prev_assets.glb','wb').write(base64.b64decode(re.search(r'window\.HAVEN_GLB = \"([^\"]+)\"', s).group(1))); open('build/prev_assets.json','w').write(re.search(r'<script id=\"haven-assets\" type=\"application/json\">(.*?)</script>', s, re.S).group(1))"
python3 tools/build_concepts.py build/prev_assets.glb build/prev_assets.json <hardware>/mechanical_cad/v2_ergonomic_shell <form-concepts worktree>/mechanical_cad/v2_form_concepts build/assets_concepts.glb build/assets_concepts.json
python3 tools/seat_concepts.py build/assets_concepts.glb build/assets_concepts.json build/assets_seated.glb build/assets_seated.json build/seat_report.json
python3 tools/route_cable.py build/assets_seated.glb build/assets_seated.json
python3 tools/patch_concepts.py build/prev_explorer.html build/assets_seated.glb build/assets_seated.json haven_ear_explorer.html
```
