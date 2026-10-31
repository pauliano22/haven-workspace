"""Build the explorer's shared assets: one HUTUBS pp3 ear + cut-away cap, and every shape concept.

All concepts use Paul's chosen parts; only the shape differs. The ear and cap are reused from the
previous explorer build (whole pp3 outer ear + head margin, CC BY 4.0), so the scans don't have to
be downloaded again. Concept shells/parts/poses come from the haven-hardware branches:
  v2_ergonomic_shell (current stacked pebble, bean + wing = nestled + fin)
  v2_form_concepts   (stems, behind-the-ear in-ear unit + pod)

usage: build_concepts.py <prev_assets.glb> <prev_assets.json> <ergo dir> <form dir> <out.glb> <out.json>
Frames (mm): ear frame X anterior, Y up, Z lateral, origin = canal entrance of pp3.
"""
import json
import math
import os
import sys

import numpy as np
import trimesh

prev_glb, prev_json, ergo, form, out_glb, out_json = sys.argv[1:7]
PREV = json.load(open(prev_json))
N_IN = np.asarray(PREV["n_in"], float)
E_PP3 = np.array([-7.035999223589897, -67.47169549953813, -3.7570002526044846])   # pp3 canal entrance, head frame (mm)
RH = np.stack([np.eye(3)[0], np.eye(3)[2], -np.eye(3)[1]], 1)                     # columns: ear X, Y, Z in head coords


def rot(axis, deg):
    return trimesh.transformations.rotation_matrix(math.radians(deg), axis)[:3, :3]


def pose_matrix(p):
    R = rot([1, 0, 0], p["tilt_s"]) @ rot([0, 1, 0], p["tilt_a"]) @ rot(N_IN, p["roll"])
    M = np.eye(4)
    M[:3, :3] = R
    M[:3, 3] = N_IN * p["insert"]
    return M


def pp3_pose(rows):
    rows = rows if isinstance(rows, list) else next(iter(rows.values()))
    return next(r for r in rows if r["subject"] == 3)["pose"]


def frame(x_axis, y_hint, center):
    """4x4 (column-major list) with column 0 = x_axis (the part's thin/cylinder axis)."""
    x = np.asarray(x_axis, float); x /= np.linalg.norm(x)
    y = np.asarray(y_hint, float) - x * (np.asarray(y_hint, float) @ x)
    if np.linalg.norm(y) < 1e-6:
        y = np.cross(x, [0, 0, 1.0]) if abs(x[2]) < 0.9 else np.cross(x, [1.0, 0, 0])
    y /= np.linalg.norm(y)
    z = np.cross(x, y)
    M = np.eye(4)
    M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = x, y, z, center
    return M.T.flatten().round(5).tolist()


def parts_from_json(path):
    out = {}
    for p in json.load(open(path)):
        if p["kind"] == "cylinder":
            ax = np.asarray(p["axis"], float)
            ctr = p.get("center") or (np.asarray(p["base"], float) + ax / np.linalg.norm(ax) * p["height"] / 2).tolist()
            out[p["name"]] = dict(matrix=frame(ax, [0, 1, 0], ctr), extents=[p["height"], p["diameter"], p["diameter"]], kind="cyl")
        else:
            axes, size = np.asarray(p["axes"], float), np.asarray(p["size"], float)
            o = np.argsort(size)
            out[p["name"]] = dict(matrix=frame(axes[o[0]], axes[o[1]], p["center"]), extents=size[o].round(4).tolist(), kind="box")
    return out


def parts_from_stl(d):
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith(".stl"):
            to, ext = trimesh.bounds.oriented_bounds(trimesh.load(os.path.join(d, f)))
            out[f[:-4]] = dict(matrix=np.linalg.inv(to).T.flatten().round(5).tolist(), extents=np.round(ext, 4).tolist())
    return out


def shell(path, faces):
    m = trimesh.load(path)
    return m.simplify_quadric_decimation(face_count=min(faces, len(m.faces)))


CP1254 = dict(pn="VARTA CoinPower CP1254", size="Ø12.1 × 5.4 · 60–77 mAh", status=["chosen", "Chosen; small-quantity source still to find"])
DRIVER = dict(pn="8 mm dynamic driver, 16–32 Ω", size="Ø8.0 × 3.6", role="Plays the filtered sound into the nozzle. The codec's output is rated for 16–32 Ω loads.", status=["pending", "Real part still to source: no 16–32 Ω earbud driver at DigiKey/Mouser"])

# README table (v2_form_concepts/README.md, "Fit in six scanned ears"): mean / worst across six ears
CONCEPTS = [
    dict(key="current", label="Stacked pebble", case=True, battery_label="CP 1254",
         stats=dict(bbox=[21.6, 15.8, 23.3], mass="4.63 g", comp=[3.7, 4.5], prot=[7.8, 10.6], moment=0.49, life=["6.4–8.2 h", "13.7–17.6 h"]),
         pro="Best fit of the earbud shapes, one shell and one board.", con="Still presses about 4.5 mm into the smallest ear.",
         text=dict(battery=dict(CP1254, role="It's the widest part, so it sets the earbud's footprint."), driver=DRIVER)),
    dict(key="stem_head_cell", label="Stem (cell in head)", case=False, battery_label="CP 1254",
         shell=os.path.join(form, "stem_head_cell_shell.stl"), parts=os.path.join(form, "parts_stem_head_cell", "parts.json"),
         fit=os.path.join(form, "fit_stem_head_cell.json"),
         stats=dict(bbox=[19.4, 33.0, 22.3], mass="5.13 g", comp=[3.9, 4.7], prot=[6.7, 13.3], moment=0.59, life=["6.4–8.2 h", "13.7–17.6 h"]),
         pro="AirPods look, sits about 1 mm flatter, antenna at the stem tip.", con="Presses a bit more, 0.5 g heavier, needs two boards and a flex.",
         text=dict(battery=dict(CP1254, role="Kept in the head next to the driver; the stem holds the radio module and power board."), driver=DRIVER)),
    dict(key="stem_cyl", label="Stem (cell in stem)", case=False, battery_label="GP 1018L10",
         shell=os.path.join(form, "stem_cyl_shell.stl"), parts=os.path.join(form, "parts_stem_cyl", "parts.json"),
         fit=os.path.join(form, "fit_stem_cyl.json"),
         stats=dict(bbox=[19.8, 34.6, 22.4], mass="6.92 g", comp=[4.1, 4.4], prot=[9.7, 18.5], moment=0.91, life=["10.7–11.2 h", "22.9–24.0 h"]),
         pro="Most battery of the earbud shapes (about 11 h loud).", con="Heavy at 6.9 g and levers itself out: twice the tipping force.",
         text=dict(battery=dict(pn="GP Batteries GP1018L10 (cylindrical)", size="Ø10.5 × 18 · 100 mAh min", role="A cylindrical cell in the stem. It's why this stem is about 13.5 mm thick.", status=["concept", "Only small cylinder cell with a public datasheet that beats the CP1254"]), driver=DRIVER)),
    dict(key="bean_wing", label="Bean + wing", case=True, battery_label="CP 1254",
         shell=os.path.join(ergo, "v2_nestled_fin_shell.stl"), parts_stl=os.path.join(ergo, "parts_nestled"),
         fit=(os.path.join(ergo, "fit_results.json"), "v2_nestled_fin"),
         stats=dict(bbox=[18.9, 29.1, 16.9], mass="4.63 g", comp=[4.3, 5.7], prot=[8.0, 12.2], moment=0.40, life=["6.4–8.2 h", "13.7–17.6 h"]),
         pro="Low profile, wing locks into the concha, lowest tipping force of the buds.", con="Battery beside the driver is too long for most conchas; fits worse.",
         text=dict(battery=dict(CP1254, role="Lies beside the driver in the concha bowl; the board spans both."), driver=DRIVER)),
    dict(key="bte", label="Behind-the-ear", case=False, battery_label="CP 1454",
         shell=os.path.join(form, "bte_inear_shell.stl"), parts=os.path.join(form, "parts_bte_inear", "parts.json"),
         fit=os.path.join(form, "fit_bte_inear.json"),
         stats=dict(bbox=[12.5, 15.5, 15.9], mass="1.37 g in the ear + 4.77 g pod", comp=[2.7, 3.2], prot=[-2.4, -0.5], moment=0.06, life=["9.1–12.8 h", "19.4–27.4 h"]),
         pro="Most comfortable in the ear (a third of the pressure), flush, longest battery.", con="Not an earbud: a 33 mm pod and cable behind the ear; glasses and helmets conflict.",
         note="The pod's resting position on the head is approximate (the fit check ran on cropped scans).",
         text=dict(battery=dict(pn="VARTA CoinPower CP1454 (in the pod)", size="Ø14.1 × 5.4 · 85–120 mAh", role="In the behind-ear pod with the board, radio, charger pads and magnet.", status=["concept", "Pod check not reliable on cropped scans"]), driver=DRIVER)),
]

prev = trimesh.load(prev_glb)
geom_of = {n: prev.graph[n][1] for n in prev.graph.nodes_geometry}
scene = trimesh.Scene()
scene.add_geometry(prev.geometry[geom_of["ear"]], node_name="ear")
scene.add_geometry(prev.geometry[geom_of["cap"]], node_name="cap")
var_out = {}
for c in CONCEPTS:
    k = c["key"]
    if k == "current":
        pv = PREV["variants"]["current"]
        scene.add_geometry(prev.geometry[geom_of["shell_current"]], node_name="shell_current")
        parts, pose_m = pv["parts"], pv["pose"]["matrix"]
    else:
        scene.add_geometry(shell(c["shell"], 18000), node_name=f"shell_{k}")
        parts = parts_from_json(c["parts"]) if "parts" in c else parts_from_stl(c["parts_stl"])
        if isinstance(c["fit"], tuple):
            rows = json.load(open(c["fit"][0]))[c["fit"][1]]
        else:
            rows = json.load(open(c["fit"]))
        pose_m = pose_matrix(pp3_pose(rows)).T.flatten().round(6).tolist()
    entry = {kk: v for kk, v in c.items() if kk not in ("shell", "parts", "parts_stl", "fit")}
    entry.update(parts=parts, pose=dict(matrix=pose_m))
    if k == "bte":
        pod_row = next(r for r in json.load(open(os.path.join(form, "fit_bte_pod.json"))) if r["subject"] == 3)
        a = math.radians(pod_row["theta"])
        rot_lat = np.array([[math.cos(a), 0, -math.sin(a)], [0, 1, 0], [math.sin(a), 0, math.cos(a)]])
        M0 = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float).T
        Rpod = RH.T @ (rot_lat @ M0)                                   # pod frame -> ear frame
        tpod = RH.T @ (np.asarray(pod_row["center_head"]) - E_PP3)
        Mp = np.eye(4); Mp[:3, :3] = Rpod; Mp[:3, 3] = tpod
        scene.add_geometry(shell(os.path.join(form, "bte_pod_shell.stl"), 8000), node_name="shell_bte_pod")
        entry["pod"] = dict(matrix=Mp.T.flatten().round(6).tolist(), parts=parts_from_json(os.path.join(form, "parts_bte_pod", "parts.json")),
                            size="17.8 × 33.4 × 9.2", mass="4.77 g")
    var_out[k] = entry
    print(k, "parts", sorted(parts))

glb = trimesh.exchange.gltf.export_glb(scene, include_normals=True)
open(out_glb, "wb").write(glb)
A = {kk: PREV[kk] for kk in ("n_in", "nozzle_base_bud", "cut_normal", "canal", "crop")}
A.update(attribution="Ear scan: HUTUBS HRTF database, TU Berlin (Brinkmann et al. 2019), CC BY 4.0, doi:10.14279/depositonce-8487. Subject pp3, right ear, cropped and smoothed.",
         variants=var_out, order=[c["key"] for c in CONCEPTS])
json.dump(A, open(out_json, "w"), indent=1)
print("wrote", out_glb, os.path.getsize(out_glb))
