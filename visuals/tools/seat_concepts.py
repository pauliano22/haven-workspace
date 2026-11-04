"""Re-seat every shape concept in ear pp3 for display, with a hard skin-penetration limit.

The fit search in the hardware repos treated skin as rigid and allowed several mm of overlap, so
shells visibly passed through the ear in the explorer. Here each concept gets a display pose
that keeps the shell outside the skin to within PEN_LIMIT (soft tissue gives a little), except
for the nozzle and tip inside the canal entrance. If no pose meets the limit, the least-bad pose
is kept and the overlapping part of the shell is coloured red, so the misfit is shown, not hidden.
Stems are also required to hang downward and slightly forward (out of the intertragic notch).

The behind-the-ear pod is settled onto the skin in the groove behind the pinna, and its cable is
routed from the in-ear unit up past the tragus, over the root of the helix and down to the pod,
held at least CABLE_R + CABLE_GAP off the skin everywhere.

usage: seat_concepts.py <assets.glb> <assets.json> <out.glb> <out.json> <report.json>
Signed distance to the ear: dense surface samples + normals (positive = air, negative = tissue).
"""
import json
import math
import os
import sys

import numpy as np
import trimesh
from scipy.optimize import minimize
from scipy.spatial import cKDTree

in_glb, in_json, out_glb, out_json, out_report = sys.argv[1:6]
A = json.load(open(in_json))
N_IN = np.asarray(A["n_in"], float)
PEN_LIMIT = 1.0          # mm of skin compression allowed for display
TRAGUS_Y = 13.2          # pp3 tragus height above the canal entrance (lateral, ergonomic README)
CABLE_R, CABLE_GAP = 0.6, 0.5
DOWN_FWD = np.array([0.30, -1.0, 0.0]) / np.linalg.norm([0.30, -1.0, 0.0])

sc = trimesh.load(in_glb, process=False)
geom_of = {n: sc.graph[n][1] for n in sc.graph.nodes_geometry}
G = {n: sc.geometry[g] for n, g in geom_of.items()}
for kv in filter(None, os.environ.get("SEAT_SHELLS", "").split(",")):   # key=path.stl: swap in a regenerated shell
    k_, p_ = kv.split("=")
    m_ = trimesh.load(p_)
    G[f"shell_{k_}"] = m_.simplify_quadric_decimation(face_count=min(18000, len(m_.faces)))
ear = G["ear"]
SP, fi = trimesh.sample.sample_surface_even(ear, 400000, seed=1)
SN = ear.face_normals[fi]
TREE = cKDTree(SP)


def sdist(Q):
    d, i = TREE.query(Q)
    return np.einsum("ij,ij->i", Q - SP[i], SN[i]), SN[i]


def rot(axis, deg):
    return trimesh.transformations.rotation_matrix(math.radians(deg), axis)[:3, :3]


def pose_R(roll, ta, ts):
    return rot([1, 0, 0], ts) @ rot([0, 1, 0], ta) @ rot(N_IN, roll)


def in_canal(Q):
    along = Q @ N_IN
    rad = np.linalg.norm(Q - np.outer(along, N_IN), axis=1)
    # canal opening: the scan closes it at the entrance, so the first part of the canal reads as tissue.
    # Real entrances are ~8.3 x 9.5 mm (radius ~4.8); the nozzle root sits just outside.
    return ((along > -1.6) & (rad < 4.4)) | ((along > -1.2) & (rad < 4.8))


FIT_SEEDS = dict(current=(67, 15, -15, 0.75), stem_head_cell=(67, 15, 5, -0.75), stem_cyl=(-67, 15, -15, -0.75),
                 bean_wing=(38, -5, 15, -0.75), bte=(30, 15, -10, -0.75))   # pp3 poses from the fit studies


def evaluate(P, x, stem_dir=None):
    roll, ta, ts, ins = x
    R = pose_R(roll, ta, ts)
    Q = P @ R.T + N_IN * ins
    s, _ = sdist(Q)
    m = ~in_canal(Q)
    pen = np.clip(-s[m], 0, None)
    pmax = float(pen.max()) if m.any() else 0.0
    deep = float((pen > 0.5).sum()) / len(P)
    contact = float(((s > -0.6) & (s < 0.8) & m).sum()) / len(P)
    stem_pen = 0.0
    if stem_dir is not None:
        d = R @ stem_dir
        ang = math.degrees(math.acos(max(-1.0, min(1.0, float(-d[1])))))
        # hang down (within ~40 deg of vertical, free to lean out past the antitragus), never backward
        stem_pen = 0.01 * ang + 0.3 * max(0.0, ang - 40.0) + 3.0 * max(0.0, -float(d[0]) - 0.05)
    return dict(pmax=pmax, deep=deep, contact=contact, prot=float(Q[:, 2].max()) - TRAGUS_Y, stem=stem_pen)


def f1(e):   # stage 1: least penetration (and a hanging stem)
    return e["pmax"] + 0.5 * e["deep"] + e["stem"]


def f2(e):   # stage 2: within the limit, touch the concha and stand out less
    return 50 * max(0.0, e["pmax"] - PEN_LIMIT) + e["stem"] - 1.5 * e["contact"] + 0.05 * max(0.0, e["prot"])


def clampx(x):
    x = np.array(x, float); x[1:3] = np.clip(x[1:3], -32, 32); x[3] = np.clip(x[3], -1.5, 1.2); return x


def nm(P, x0, fn, stem_dir, iters=260):
    r = minimize(lambda x: fn(evaluate(P, clampx(x), stem_dir)), np.array(x0, float), method="Nelder-Mead",
                 options=dict(xatol=0.15, fatol=1e-4, maxiter=iters))
    return clampx(r.x)


def seat(P, key, stem_dir=None):
    cands = []
    for roll in range(-180, 180, 15):
        for ta in (-24, -12, 0, 12, 24):
            for ts in (-24, -12, 0, 12, 24):
                for ins in (-0.8, 0.6):
                    x = (roll, ta, ts, ins)
                    cands.append((f1(evaluate(P, x, stem_dir)), x))
    cands.sort(key=lambda c: c[0])
    starts, seen = [], []
    for c, x in cands:
        if all(min(abs(x[0] - y[0]) % 360, 360 - abs(x[0] - y[0]) % 360) > 20 or abs(x[1] - y[1]) > 10 or abs(x[2] - y[2]) > 10 for y in seen):
            starts.append(x); seen.append(x)
        if len(starts) == 6:
            break
    starts.append(FIT_SEEDS[key])
    best = None
    for x0 in starts:
        x = nm(P, x0, f1, stem_dir)
        e = evaluate(P, x, stem_dir)
        if best is None or f1(e) < f1(best[1]):
            best = (x, e)
    x, e = best
    if e["pmax"] <= PEN_LIMIT:
        x2 = nm(P, x, f2, stem_dir)
        e2 = evaluate(P, x2, stem_dir)
        if e2["pmax"] <= PEN_LIMIT and f2(e2) < f2(e):
            x, e = x2, e2
    return x, e


def matrix(x):
    R = pose_R(*x[:3])
    M = np.eye(4); M[:3, :3] = R; M[:3, 3] = N_IN * x[3]
    return M


def shell_colors(mesh, M):
    Q = mesh.vertices @ M[:3, :3].T + M[:3, 3]
    s, _ = sdist(Q)
    pen = np.where(in_canal(Q), 0.0, np.clip(-s, 0, None))
    t = np.clip((pen - PEN_LIMIT) / 1.0, 0, 1)                   # red ramps in from the limit to limit + 1 mm
    base = np.array([255, 255, 255], float); red = np.array([214, 48, 49], float)
    col = (base[None] * (1 - t[:, None]) + red[None] * t[:, None]).astype(np.uint8)
    return np.hstack([col, np.full((len(col), 1), 255, np.uint8)]), float(pen.max())


def stem_axis(parts, keys):
    """Unit vector in the bud frame from the head (driver) toward the stem's far end."""
    C = lambda k: np.asarray(parts[k]["matrix"]).reshape(4, 4)[3, :3]
    far = np.mean([C(k) for k in keys], axis=0)
    v = far - C("driver")
    return v / np.linalg.norm(v)


import os
POD_ONLY = os.environ.get("SEAT_POD_ONLY") == "1"      # concepts already seated in the input files
KEYS = [k for k in os.environ.get("SEAT_KEYS", "").split(",") if k]   # re-seat only these; keep the rest as given
SKIP_POD = os.environ.get("SEAT_SKIP_POD") == "1"
report, scene = {}, trimesh.Scene()
scene.add_geometry(ear, node_name="ear")
scene.add_geometry(G["cap"], node_name="cap")
if POD_ONLY or KEYS:
    report = json.load(open(out_report)) if os.path.exists(out_report) else {}
    for key in A["order"]:
        if key not in KEYS:
            scene.add_geometry(G[f"shell_{key}"], node_name=f"shell_{key}")
for key in ([] if POD_ONLY else (KEYS or A["order"])):
    v = A["variants"][key]
    shell = G[f"shell_{key}"]
    P = np.asarray(shell.vertices)            # score every vertex: sparse samples let the search hide overlaps between them
    M_old = np.asarray(v["pose"]["matrix"]).reshape(4, 4).T
    old_pen = shell_colors(shell, M_old)[1]
    stem = None
    if key == "stem_cyl":
        stem = stem_axis(v["parts"], ["battery"])
    elif key == "stem_head_cell":
        stem = stem_axis(v["parts"], ["module", "pad1", "pad2"])
    x, ev_ = seat(P, key, stem)
    M = matrix(x)
    colors, pen = shell_colors(shell, M)
    shell.visual = trimesh.visual.ColorVisuals(shell, vertex_colors=colors)
    scene.add_geometry(shell, node_name=f"shell_{key}")
    Qv = shell.vertices @ M[:3, :3].T + M[:3, 3]
    rep = dict(old_pose_pen=round(old_pen, 2), display_pen=round(pen, 2), fits=bool(pen <= PEN_LIMIT + 1e-6),
               protrusion=round(float(Qv[:, 2].max()) - TRAGUS_Y, 1), pose=[round(float(a), 2) for a in x])
    if stem is not None:
        d = M[:3, :3] @ stem
        rep["stem_dir_world"] = [round(float(a), 3) for a in d]
        rep["stem_down_deg"] = round(math.degrees(math.acos(max(-1, min(1, float(d @ np.array([0, -1.0, 0])))))), 1)
    v["pose"] = dict(matrix=M.T.flatten().round(6).tolist())
    v["display"] = dict(pen=round(pen, 2), fits=rep["fits"], protrusion=rep["protrusion"], limit=PEN_LIMIT)
    report[key] = rep
    print(key, rep, flush=True)

# ---------------------------------------------------------------- behind-the-ear pod + cable
v = A["variants"]["bte"]
if SKIP_POD:
    scene.add_geometry(G["shell_bte_pod"], node_name="shell_bte_pod")
    open(out_glb, "wb").write(trimesh.exchange.gltf.export_glb(scene, include_normals=True))
    json.dump(A, open(out_json, "w"), indent=1); json.dump(report, open(out_report, "w"), indent=1)
    print("wrote", out_glb); sys.exit(0)
pod = G["shell_bte_pod"]
PP, _ = trimesh.sample.sample_surface_even(pod, 1200, seed=3)
M0 = np.asarray(v["pod"]["matrix"]).reshape(4, 4).T
R0 = M0[:3, :3]


def pod_eval(theta, yaw, x, y, z):
    R = rot([0, 1, 0], yaw) @ rot([0, 0, 1], theta) @ R0
    Q = PP @ R.T + np.array([x, y, z])
    s, _ = sdist(Q)
    return R, Q, s


def settle_z(theta, yaw, x, y, z_out=30.0, z_in=-25.0, limit=0.5):
    """Most medial z where the pod presses no more than `limit` into skin."""
    R, Q, s = pod_eval(theta, yaw, x, y, z_out)
    if -s.min() > limit:
        return None
    lo, hi = z_out, z_in
    for _ in range(14):
        mid = 0.5 * (lo + hi)
        _, _, s = pod_eval(theta, yaw, x, y, mid)
        if -s.min() > limit:
            hi = mid
        else:
            lo = mid
    return lo


best = None
for theta in (-15, 0, 15):
    for yaw in (-15, 0, 15):
        for x in np.arange(-48, -17.9, 3.0):
            for y in np.arange(8, 26.1, 3.0):
                z = settle_z(theta, yaw, x, y)
                if z is None or z > 14.0:          # resting on the pinna, not on the scalp behind it
                    continue
                R, Q, s = pod_eval(theta, yaw, x, y, z)
                contact = float(((s > -0.6) & (s < 0.6)).sum()) / len(PP)
                # tucked toward the pinna (larger x), resting on skin, upright-ish
                sc_ = contact * 4 + 0.05 * x + 0.03 * y - 0.01 * abs(theta) - 0.004 * abs(yaw)
                if best is None or sc_ > best[0]:
                    best = (sc_, theta, yaw, x, y, z, contact, float(-s.min()))
_, th, yw, px, py, pz, pc, ppen = best
Rp = rot([0, 1, 0], yw) @ rot([0, 0, 1], th) @ R0
Mp = np.eye(4); Mp[:3, :3] = Rp; Mp[:3, 3] = [px, py, pz]
v["pod"]["matrix"] = Mp.T.flatten().round(6).tolist()
pod_pen = float(np.clip(-sdist(pod.vertices @ Rp.T + Mp[:3, 3])[0], 0, None).max())
report["bte_pod"] = dict(pen=round(pod_pen, 2), contact_frac=round(pc, 3), pos=[round(px, 1), round(py, 1), round(pz, 1)], theta=th, yaw=yw)
print("pod", report["bte_pod"], flush=True)
scene.add_geometry(G["shell_bte_pod"], node_name="shell_bte_pod")

# cable: boss (in-ear unit, posed) -> in front of the helix root -> over the top of the ear -> pod top
Mb = np.asarray(v["pose"]["matrix"]).reshape(4, 4).T
cb = np.asarray(v["parts"]["cable_boss"]["matrix"]).reshape(4, 4)
boss_c = (Mb @ np.append(cb[3, :3], 1))[:3]
boss_ax = Mb[:3, :3] @ cb[0, :3]
pod_top_local = np.array([pod.bounds[:, 0].mean(), pod.bounds[1, 1] - 1.5, pod.bounds[:, 2].mean()])
pod_top = Rp @ pod_top_local + Mp[:3, 3]


def surface_along(origin, direction, max_t=80.0, step=0.25):
    """First point where a ray from `origin` reaches the skin."""
    direction = direction / np.linalg.norm(direction)
    ts = np.arange(0, max_t, step)
    Q = origin[None] + ts[:, None] * direction[None]
    s, n = sdist(Q)
    hit = np.where(s < CABLE_R + CABLE_GAP + 0.6)[0]
    return Q[hit[0]] if len(hit) else None


def lateral_skin(x, y):
    """Skin point at (x, y) seen from the side (ray from far lateral toward the head)."""
    h = surface_along(np.array([x, y, 60.0]), np.array([0, 0, -1.0]))
    return None if h is None else h


ctrl = [boss_c, boss_c + boss_ax * 3.0]
for (xx, yy) in ((boss_c[0] + 6.0, boss_c[1] + 9.0), (boss_c[0] + 9.0, boss_c[1] + 17.0), (boss_c[0] + 9.5, boss_c[1] + 25.0)):
    h = lateral_skin(xx, yy)                     # in front of the crus / root of the helix, on the side of the face
    if h is not None:
        ctrl.append(h)
top_y = max(pod_top[1], ctrl[-1][1]) + 7.0       # over the top of the junction between pinna and head
ctrl.append(np.array([0.5 * (ctrl[-1][0] + pod_top[0]), top_y, 0.5 * (ctrl[-1][2] + pod_top[2])]))
ctrl += [pod_top + np.array([1.5, 5.0, 0.5]), pod_top]
ctrl = np.array(ctrl)
# smooth path, then push every sample off the skin and relax, keeping the ends fixed
curve = trimesh.path.entities.BSpline
t_ctrl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(ctrl, axis=0), axis=1))]
ts = np.linspace(0, t_ctrl[-1], 180)
pts = np.stack([np.interp(ts, t_ctrl, ctrl[:, k]) for k in range(3)], 1)
need = CABLE_R + CABLE_GAP
for it in range(220):
    lap = pts.copy()
    lap[1:-1] = 0.5 * pts[1:-1] + 0.25 * (pts[:-2] + pts[2:])
    pts[2:-2] = lap[2:-2]
    s, n = sdist(pts)
    low = s < need
    low[:3] = False; low[-3:] = False
    pts[low] += (need - s[low])[:, None] * n[low]
for it in range(40):                       # final push-out only, so nothing is left inside the clearance
    s, n = sdist(pts)
    low = s < need + 0.05
    low[:3] = False; low[-3:] = False
    pts[low] += (need + 0.05 - s[low])[:, None] * n[low]
s, _ = sdist(pts)
mid = slice(6, -6)
cable_min = float(s[mid].min())
report["bte_cable"] = dict(min_skin_clearance=round(cable_min, 2), needed=need, length_mm=round(float(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum()), 1))
print("cable", report["bte_cable"], flush=True)
v["cable"] = pts.round(3).tolist()

glb = trimesh.exchange.gltf.export_glb(scene, include_normals=True)
open(out_glb, "wb").write(glb)
json.dump(A, open(out_json, "w"), indent=1)
json.dump(report, open(out_report, "w"), indent=1)
print("wrote", out_glb, len(glb))
