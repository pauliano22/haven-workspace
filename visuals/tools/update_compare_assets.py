"""Refresh two shapes in the explorer build used for the v2 / v3 / typical-aid comparison pictures (2026-11-14).

usage: python3 update_compare_assets.py <in explorer_with_v3.html> <out explorer.html>

1. The v2 pod was drawn 17.8 x 33.4 x 9.2 mm; the current v2 shell file (hardware/mechanical_cad/v2_bte/bte_pod_R.stl)
   is 19.5 x 33.2 x 11.4 mm. Swap the real file in: same top end, same head-side face, same centre line. Of the four
   ways the file could be turned, the one that overlaps the old shape best is used.
2. The v3 in-ear piece was a stand-in capsule. Swap in the real draft (inear_v3_body + inear_v3_cap), nozzle root on
   the explorer's nozzle base, axis into the canal.
Only build/ copies are written. The published explorer and the website copy are not touched.
"""
import base64, io, json, os, re, sys
import numpy as np
import trimesh

src, out = sys.argv[1:3]
HERE = os.path.dirname(os.path.abspath(__file__))
CAD = os.path.join(HERE, "..", "..", "hardware", "mechanical_cad")
s = open(src).read()
glb = base64.b64decode(re.search(r'window\.HAVEN_GLB = "([^"]+)"', s).group(1))
A = json.loads(re.search(r'<script id="haven-assets" type="application/json">(.*?)</script>', s, re.S).group(1))
scene = trimesh.load(io.BytesIO(glb), file_type="glb")

# 1. v2 pod
gname = scene.graph["shell_bte_pod"][1]
old = scene.geometry[gname]
ob = old.bounds
best = None
for rz in (0, 180):
    for ry in (0, 180):
        m = trimesh.load(os.path.join(CAD, "v2_bte", "bte_pod_R.stl"))
        m.apply_transform(trimesh.transformations.euler_matrix(0, np.radians(ry), np.radians(rz)))
        b = m.bounds
        m.apply_translation([(ob[0][0] + ob[1][0]) / 2 - (b[0][0] + b[1][0]) / 2, ob[1][1] - b[1][1], ob[0][2] - b[0][2]])
        pts = old.sample(4000)
        score = float(np.mean(m.contains(pts) | (np.abs(trimesh.proximity.signed_distance(m, pts)) < 1.5)))
        print("v2 pod turn", rz, ry, "overlap", round(score, 3))
        if best is None or score > best[0]:
            best = (score, m, (rz, ry))
pod = best[1]
if len(pod.faces) > 60000:
    pod = pod.simplify_quadric_decimation(face_count=60000)
pod.visual = old.visual.copy() if hasattr(old.visual, "copy") and len(getattr(old.visual, "vertex_colors", [])) == 0 else pod.visual
print("v2 pod: old", old.extents.round(1).tolist(), "new", pod.extents.round(1).tolist(), "turn", best[2])
scene.geometry[gname] = pod

# 2. v3 in-ear piece
gname3 = scene.graph["shell_v3"][1]
n = np.array(A["n_in"], float); n /= np.linalg.norm(n)
base = np.array(A["nozzle_base_bud"], float)
parts = [trimesh.load(os.path.join(CAD, "v3_slim", f"inear_v3_{k}.stl")) for k in ("body", "cap")]
cap = trimesh.util.concatenate(parts)
cap.apply_transform(trimesh.geometry.align_vectors([0, 0, 1], n))
cap.apply_translation(base)
print("v3 in-ear: old", scene.geometry[gname3].extents.round(1).tolist(), "new", cap.extents.round(1).tolist())
scene.geometry[gname3] = cap

new_glb = scene.export(file_type="glb")
v3 = A["variants"]["v3"]
v3["note"] = v3["note"].replace("The in-ear piece is a rough stand-in for a 4.9 mm speaker with Haven's sealing tip", "The in-ear piece is the first draft capsule (7.0 mm across) for a 4.9 mm speaker, with Haven's sealing tip")
s = re.sub(r'(<script id="haven-assets" type="application/json">).*?(</script>)', lambda m: m.group(1) + json.dumps(A, separators=(",", ":")) + m.group(2), s, count=1, flags=re.S)
s = re.sub(r'(<script>window\.HAVEN_GLB = ")[^"]*(";</script>)', lambda m: m.group(1) + base64.b64encode(new_glb).decode() + m.group(2), s, count=1)
open(out, "w").write(s)
print("wrote", out, len(s) // 1024, "KB")
