"""Add the "Haven v3 slim" concept to the built explorer, on the same ear, pod position and wire route as the
behind-the-ear concept and the typical hearing aid, so the three can be compared.

usage: python3 add_v3_slim.py <in explorer.html (already has the typical aid)> <out explorer.html>

The pod shell is the real generated shell hardware/mechanical_cad/v3_slim/pod_v3_A_thin_R.stl (17 mm cell, 0.8 mm
board, 0.8 mm wall). The in-ear piece is a ROUGH stand-in: a 7.2 x 8 mm barrel for the 4.9 mm speaker, outside the
canal, with Haven's own nozzle and sealing tip kept. Nothing here changes the other concepts.
"""
import base64, copy, io, json, os, re, sys
import numpy as np
import trimesh

src, out = sys.argv[1:3]
STYLED = "--raw" not in sys.argv      # default: the styled outer form (pod_v3_styled.py); --raw: the generator shrink-wrap
HERE = os.path.dirname(os.path.abspath(__file__))
STL = os.path.join(HERE, "..", "..", "hardware", "mechanical_cad", "v3_slim", "pod_v3_styled_R.stl" if STYLED else "pod_v3_A_thin_R.stl")
s = open(src).read()
glb = base64.b64decode(re.search(r'window\.HAVEN_GLB = "([^"]+)"', s).group(1))
A = json.loads(re.search(r'<script id="haven-assets" type="application/json">(.*?)</script>', s, re.S).group(1))
if "v3" in A["variants"]:
    sys.exit("already has v3")
assert "ric" in A["variants"], "run add_typical_aid.py first"
scene = trimesh.load(io.BytesIO(glb), file_type="glb")

# pod: STL frame -> the explorer's pod frame. Tops level with the v2 pod, head-side faces level, same x origin.
ref = scene.geometry[scene.graph["shell_bte_pod"][1]].bounds
pod = trimesh.load(STL)
pod.apply_translation([0, ref[1][1] - pod.bounds[1][1] - 0.4, ref[0][2] - pod.bounds[0][2]])
if len(pod.faces) > 60000:
    pod = pod.simplify_quadric_decimation(face_count=60000)
print("v3 pod bounds", pod.bounds.round(1).tolist(), "size", pod.extents.round(1).tolist(), "v2 pod", (ref[1] - ref[0]).round(1).tolist())

# in-ear: small barrel outside the canal, behind the nozzle base
n = np.array(A["n_in"], float); n /= np.linalg.norm(n)
base = np.array(A["nozzle_base_bud"], float)
bar = trimesh.creation.capsule(radius=3.6, height=1.6, count=[24, 24])     # 7.2 across, 8.8 long incl. round ends
bar.apply_transform(trimesh.geometry.align_vectors([0, 0, 1], -n))
bar.apply_translation(base - n * 3.9)
print("barrel size", bar.extents.round(1).tolist())

scene.add_geometry(pod, node_name="shell_v3_pod", geom_name="v3_pod")
scene.add_geometry(bar, node_name="shell_v3", geom_name="v3_inear")
new_glb = scene.export(file_type="glb")

bte = A["variants"]["bte"]
v3 = copy.deepcopy(A["variants"]["ric"])
body = [round(float(pod.extents[1]), 1), round(float(pod.extents[0]), 1), round(float(pod.extents[2]), 1)] if STYLED else [32.4, 13.0, 9.2]
v3.update(key="v3", label="Haven v3 slim", generic=True, slim=True,
          stats=dict(bbox=body, mass="about 3 g (estimate)", comp=[0, 0], prot=[0, 0], moment=0, life=["", ""]),
          pro="Close to a typical aid in width: about 12.6 mm wide and 10 mm thick, against 17.8 and 11.4 mm for today's Haven pod. Only a small speaker sits at the ear.",
          con="Not built. The circuit board is placed but not fully routed, the battery is not sourced, and battery life is about 13 h quiet / 6 h loud by datasheet estimate, about a third of v2.",
          note="Pod shape is a rounded outer form drawn around the real v3 parts with about 0.8 mm of cover, assuming a 3.5 × 8 × 20 mm cell that is not confirmed yet. The rounding costs about 1 mm of thickness. The hollow printable shell is not made yet. The in-ear piece is a rough stand-in for a 4.9 mm speaker with Haven's sealing tip; the microphone moves to the pod. Same ear, pod position and wire route as the other two concepts.")
A["variants"]["v3"] = v3
A["order"] = [k for k in A["order"] if k != "ric"] + ["v3", "ric"]

s = re.sub(r'(<script id="haven-assets" type="application/json">).*?(</script>)',
           lambda m: m.group(1) + json.dumps(A, separators=(",", ":")) + m.group(2), s, count=1, flags=re.S)
s = re.sub(r'(<script>window\.HAVEN_GLB = ")[^"]*(";</script>)',
           lambda m: m.group(1) + base64.b64encode(new_glb).decode() + m.group(2), s, count=1)


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b, 1)


# Haven's nozzle and sealing tip stay visible on v3 (it must seal the canal); they are hidden only for the typical aid
rep("if (V0.a.generic) { noz.visible = false; tip.visible = false; }", "if (V0.a.generic && !V0.a.slim) { noz.visible = false; tip.visible = false; }")
rep('!(c.generic && ["nozzle", "eartip"].includes(id))', '!(c.generic && !c.slim && ["nozzle", "eartip"].includes(id))')
rep('BUD_C = centerOf((active === "ric" ? VAR.bte.bud : bud).items.shell[0]);', 'BUD_C = centerOf((active === "ric" || active === "v3" ? VAR.bte.bud : bud).items.shell[0]);')
rep('    if (c.generic) {\n      Object.assign(PARTS.shell, { name: "Receiver and dome"',
    '    if (c.slim) {\n'
    '      Object.assign(PARTS.shell, { name: "Speaker housing", pn: "v3 in-ear piece (rough stand-in)", size: "about 7 × 9 mm", role: "Holds a 4.9 mm speaker just outside the canal. No microphone or circuit board in the ear.", status: ["concept", "Rough stand-in, speaker loudness not measured"] });\n'
    '      Object.assign(PARTS.pod, { name: "Slim pod", pn: "Haven v3 slim pod (styled outer form)", size: st.bbox.map(x => x.toFixed(1)).join(" × "), role: "Flat cell under a narrow circuit board, with the radio, sound chip and microphone.", status: ["concept", "Board placed, not fully routed; not built"] });\n'
    '      Object.assign(PARTS.cable, { name: "Wire", pn: "2-conductor speaker wire", size: "~Ø1.0", role: "Carries sound from the pod, over the top of the ear, to the speaker.", status: ["concept"] });\n'
    '    } else if (c.generic) {\n      Object.assign(PARTS.shell, { name: "Receiver and dome"')
open(out, "w").write(s)
print("wrote", out, len(s) // 1024, "KB")
