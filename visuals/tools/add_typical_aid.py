"""Add a "Typical hearing aid" concept to the built explorer, seated in the same scanned ear as Haven's
behind-the-ear concept, so the two can be compared in the viewer Paul already uses.

usage: python3 add_typical_aid.py <in explorer.html> <out explorer.html>

The typical aid is a GENERIC stand-in built from published sizes (a receiver-in-canal body about 30 mm long,
10 mm wide in the plane of the head and 8 mm thick, a thin wire, a small receiver and a soft dome). It is not
any real product. It reuses the BTE concept's pod placement, cable route and in-ear pose, so the only
difference between the two concepts is the hardware. Nothing here changes the Haven concepts.
"""
import base64
import copy
import io
import json
import math
import re
import sys

import numpy as np
import trimesh

src, out = sys.argv[1:3]
s = open(src).read()
glb = base64.b64decode(re.search(r'window\.HAVEN_GLB = "([^"]+)"', s).group(1))
A = json.loads(re.search(r'<script id="haven-assets" type="application/json">(.*?)</script>', s, re.S).group(1))
if "ric" in A["variants"]:
    sys.exit("already has the typical aid")
scene = trimesh.load(io.BytesIO(glb), file_type="glb")


def catmull(pts, n):
    P = np.array(pts, float)
    out_ = []
    for i in range(len(P) - 1):
        p0, p1, p2, p3 = P[max(i - 1, 0)], P[i], P[i + 1], P[min(i + 2, len(P) - 1)]
        for t in np.linspace(0, 1, n, endpoint=False):
            out_.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out_.append(P[-1])
    return np.array(out_)


# ---- generic receiver-in-canal body, in the pod's local frame (x anterior, y up, z lateral)
pod_geo = scene.geometry[scene.graph[[n for n in scene.graph.nodes_geometry if n == "shell_bte_pod"][0]][1]]
top_y = float(pod_geo.bounds[1][1])
zc = float((pod_geo.bounds[0][2] + pod_geo.bounds[1][2]) / 2)
LEN, HALF_W, HALF_T = 30.0, 5.0, 4.0     # 30 long, 10 wide (in the plane of the head), 8 thick (lateral)
spine = catmull([[-1.5, top_y - 30], [-2.4, top_y - 22], [-1.8, top_y - 13], [0.4, top_y - 5.5], [4.6, top_y - 0.5]], 14)
spine = np.c_[spine, np.full(len(spine), zc)]
N, R = len(spine), 48
verts = []
for i, c in enumerate(spine):
    t = i / (N - 1)
    T = spine[min(i + 1, N - 1)] - spine[max(i - 1, 0)]
    T /= np.linalg.norm(T)
    inplane = np.array([-T[1], T[0], 0.0]); inplane /= np.linalg.norm(inplane)
    taper = math.sin(math.pi * t) ** 0.42
    for a in np.linspace(0, 2 * math.pi, R, endpoint=False):
        verts.append(c + math.cos(a) * HALF_W * taper * inplane + math.sin(a) * HALF_T * taper * np.array([0, 0, 1.0]))
verts = np.array(verts)
faces = []
for sidx in range(N - 1):
    for k in range(R):
        k2 = (k + 1) % R
        a0, a1, b0, b1 = sidx * R + k, sidx * R + k2, (sidx + 1) * R + k, (sidx + 1) * R + k2
        faces += [[a0, b0, a1], [a1, b0, b1]]
body = trimesh.Trimesh(verts, faces, process=True)
body.fix_normals()
print("generic body bounds", body.bounds.round(1).tolist(), "size", (body.bounds[1] - body.bounds[0]).round(1).tolist())

# ---- receiver + dome, in the in-ear unit's local frame, along the canal axis from the nozzle base
n = np.array(A["n_in"], float); n /= np.linalg.norm(n)
base = np.array(A["nozzle_base_bud"], float)


def along(mesh, axis):
    q = trimesh.geometry.align_vectors([0, 0, 1], axis)
    mesh.apply_transform(q)
    return mesh


rec = trimesh.creation.cylinder(radius=2.7, height=7.5, sections=40)
rec.apply_translation([0, 0, 3.75])
rec = along(rec, n); rec.apply_translation(base + n * 1.6)
dome = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
dome.apply_scale([4.6, 4.6, 3.4]); dome.apply_translation([0, 0, 2.2])
dome = along(dome, n); dome.apply_translation(base + n * 0.2)
recv = trimesh.util.concatenate([rec, dome])
print("receiver+dome bounds", recv.bounds.round(1).tolist())

scene.add_geometry(body, node_name="shell_ric_pod", geom_name="ric_pod")
scene.add_geometry(recv, node_name="shell_ric", geom_name="ric_recv")
new_glb = scene.export(file_type="glb")

# ---- concept data
bte = A["variants"]["bte"]
ric = copy.deepcopy(bte)
size_in = (recv.bounds[1] - recv.bounds[0]).round(1).tolist()
ric.update(
    key="ric", label="Typical hearing aid", generic=True, case=False, battery_label="",
    stats=dict(bbox=[round(float(x), 1) for x in (body.bounds[1] - body.bounds[0])], mass="not given",
               comp=[0, 0], prot=[0, 0], moment=0, life=["", ""]),
    pro="The size and shape people already wear all day: a slim body behind the ear and a tiny receiver in the canal.",
    con="A generic stand-in built from published sizes, not any real product. Real aids are curved and vary by model.",
    note="Same ear, same pod position and same wire route as the Haven behind-the-ear concept, so the size difference is the only difference.",
    text={}, parts={}, display=None)
ric["pod"] = dict(matrix=bte["pod"]["matrix"], parts={})
A["variants"]["ric"] = ric
A["order"] = [k for k in A["order"]] + ["ric"] if "ric" not in A["order"] else A["order"]

# ---- patch the page
s = re.sub(r'(<script id="haven-assets" type="application/json">).*?(</script>)',
           lambda m: m.group(1) + json.dumps(A, separators=(",", ":")) + m.group(2), s, count=1, flags=re.S)
s = re.sub(r'(<script>window\.HAVEN_GLB = ")[^"]*(";</script>)',
           lambda m: m.group(1) + base64.b64encode(new_glb).decode() + m.group(2), s, count=1)


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# the foam tip and nozzle are Haven's; hide them for the generic aid
rep('    add("eartip", tip);\n', '    add("eartip", tip);\n    if (V0.a.generic) { noz.visible = false; tip.visible = false; }\n')
# thinner wire, plus a short stub from the wire's start to the receiver
rep("const cable = new THREE.Mesh(new THREE.TubeGeometry(path, 240, 0.6, 12, false),",
    "const cable = new THREE.Mesh(new THREE.TubeGeometry(path, 240, v.a.generic ? 0.45 : 0.6, 12, false),")
rep("    cable.castShadow = true; reg(cable, \"cable\"); v.bud.items.cable.push(cable); v.bud.extra.push(cable); earRoot.add(cable);\n",
    "    cable.castShadow = true; reg(cable, \"cable\"); v.bud.items.cable.push(cable); v.bud.extra.push(cable); earRoot.add(cable);\n"
    "    if (v.a.generic) {\n"
    "      const rb = v.bud.group.localToWorld(NOZ_BASE.clone());\n"
    "      const stub = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([path.getPoint(0), path.getPoint(0).clone().lerp(rb, 0.5).add(V(0, 0, 1.2)), rb]), 40, 0.45, 10, false), cable.material);\n"
    "      stub.castShadow = true; reg(stub, \"cable\"); v.bud.items.cable.push(stub); v.bud.extra.push(stub); earRoot.add(stub);\n"
    "    }\n")
# the generic aid has no radio module: anchor the phone link on the shell instead
rep("centerOf(bud.items.module[0])", "centerOf((bud.items.module || bud.items.shell)[0])")
# the sound-path steps and camera anchors look up Haven's mic, codec, driver and charging pads; fall back to the shell
for part in ("mic", "codec", "driver", "pads"):
    rep("bud.items.%s[0]" % part, "(bud.items.%s || bud.items.shell)[0]" % part)
# same camera as Haven's behind-the-ear concept, so the two views line up exactly
rep("BUD_C = centerOf(bud.items.shell[0]);", "BUD_C = centerOf((active === \"ric\" ? VAR.bte.bud : bud).items.shell[0]);")
# the generic aid has no cable-boss part, so give it an empty cable list for the wire to be added to
rep("    if (!v.pod || !v.bud.items.cable) continue;", "    if (v.a.generic) v.bud.items.cable = v.bud.items.cable || [];\n    if (!v.pod || !v.bud.items.cable) continue;")
# part descriptions: restore Haven's text when switching back, and describe the generic aid honestly
rep("    for (const id in c.text) Object.assign(PARTS[id], c.text[id]);",
    "    if (!window.__partsOrig) window.__partsOrig = JSON.parse(JSON.stringify({ pod: PARTS.pod, cable: PARTS.cable, shell: PARTS.shell }));\n"
    "    for (const id of [\"pod\", \"cable\", \"shell\"]) Object.assign(PARTS[id], window.__partsOrig[id]);\n"
    "    for (const id in c.text) Object.assign(PARTS[id], c.text[id]);")
rep('    const sg = x => (x > 0 ? "+" : x < 0 ? "−" : "") + Math.abs(x).toFixed(1);',
    '    if (c.generic) {\n'
    '      Object.assign(PARTS.shell, { name: "Receiver and dome", pn: "Receiver and soft dome (generic)", size: "about 5 × 8 mm receiver, soft dome", role: "The small speaker that sits in the ear canal, held by a soft dome.", status: ["concept", "Generic stand-in, not a real product"] });\n'
    '      Object.assign(PARTS.pod, { name: "Hearing aid body", pn: "Typical aid body (generic)", size: st.bbox.map(x => x.toFixed(1)).join(" × "), role: "A slim body behind the ear holding the battery and electronics.", status: ["concept", "Generic stand-in, not a real product"] });\n'
    '      Object.assign(PARTS.cable, { name: "Wire", pn: "Thin receiver wire", size: "~Ø0.9", role: "Carries sound from the body, over the top of the ear, to the receiver.", status: ["concept"] });\n'
    '    }\n'
    '    const sg = x => (x > 0 ? "+" : x < 0 ? "−" : "") + Math.abs(x).toFixed(1);')
rep('fillList(list, EAR_LIST.filter(id => bud.items[id] || ["canal", "eardrum", "pinna"].includes(id)));',
    'fillList(list, EAR_LIST.filter(id => !(c.generic && ["nozzle", "eartip"].includes(id)) && (bud.items[id] || ["canal", "eardrum", "pinna"].includes(id))));')
# plain stats for a generic concept (the fit-study numbers belong to Haven's concepts only)
rep('    $("stats").innerHTML = `<dt>Size</dt>',
    '    if (c.generic) { $("stats").innerHTML = `<dt>Body size</dt><dd>${st.bbox.map(x => x.toFixed(1)).join(" × ")} mm (long × wide × thick)</dd>`\n'
    '      + `<dt>Weight</dt><dd>${st.mass}</dd><dt>Pro</dt><dd class="pro">${c.pro}</dd><dt>Con</dt><dd class="con">${c.con}</dd>`\n'
    '      + `<dd class="warn">${c.note}</dd>`; } else\n'
    '    $("stats").innerHTML = `<dt>Size</dt>')
open(out, "w").write(s)
print("wrote", out)
