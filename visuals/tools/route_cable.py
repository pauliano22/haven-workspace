"""Route the behind-the-ear cable through free space (never through tissue) and smooth it.

Path: in-ear unit's cable boss -> up in front of the root of the helix (on the side of the face) ->
over the top where the pinna meets the head -> down into the top of the pod. A* on a 1 mm voxel grid
whose free cells are at least CLEAR_GRID off the skin, with a cost that keeps the cable off the
lateral face of the pinna; then smoothing that only accepts moves keeping >= NEED clearance.
Every sample AND every segment midpoint is checked at the end.

usage: route_cable.py <assets.glb> <assets.json>   (rewrites variants.bte.cable)
"""
import heapq
import json
import sys

import numpy as np
import trimesh
from scipy.spatial import cKDTree

glb, js = sys.argv[1:3]
A = json.load(open(js))
sc = trimesh.load(glb, process=False)
G = {n: sc.geometry[sc.graph[n][1]] for n in sc.graph.nodes_geometry}
ear = G["ear"]
SP, fi = trimesh.sample.sample_surface_even(ear, 400000, seed=1)
SN = ear.face_normals[fi]
TREE = cKDTree(SP)
NEED, CLEAR_GRID, H = 1.1, 1.6, 1.0


def sdist(Q):
    d, i = TREE.query(Q)
    return np.einsum("ij,ij->i", Q - SP[i], SN[i])


v = A["variants"]["bte"]
Mb = np.asarray(v["pose"]["matrix"]).reshape(4, 4).T
cb = np.asarray(v["parts"]["cable_boss"]["matrix"]).reshape(4, 4)
boss = (Mb @ np.append(cb[3, :3], 1))[:3]
bax = Mb[:3, :3] @ cb[0, :3]
pod = G["shell_bte_pod"]
Mp = np.asarray(v["pod"]["matrix"]).reshape(4, 4).T
top_local = np.array([pod.bounds[:, 0].mean(), pod.bounds[1, 1] - 1.5, pod.bounds[:, 2].mean()])
pod_top = Mp[:3, :3] @ top_local + Mp[:3, 3]
# make sure the boss axis points away from the head
if bax[2] < 0:
    bax = -bax
start = boss + bax * 3.0

lo = np.minimum(start, pod_top) - np.array([22.0, 18.0, 14.0])
hi = np.maximum(start, pod_top) + np.array([24.0, 20.0, 18.0])
axes = [np.arange(lo[k], hi[k] + H, H) for k in range(3)]
GX, GY, GZ = np.meshgrid(*axes, indexing="ij")
cells = np.stack([GX, GY, GZ], -1).reshape(-1, 3)
S = sdist(cells).reshape(GX.shape)
free = S >= CLEAR_GRID
shape = GX.shape
print("grid", shape, "free", round(float(free.mean()), 3), flush=True)


def to_idx(p):
    return tuple(np.clip(np.round((p - lo) / H).astype(int), 0, np.array(shape) - 1))


def nearest_free(idx):
    best, bd = None, 1e9
    fi_ = np.argwhere(free)
    d = np.linalg.norm(fi_ - np.array(idx), axis=1)
    return tuple(fi_[d.argmin()])


NB = [(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1) if (a, b, c) != (0, 0, 0)]


def cell_cost(i):
    s = S[i]
    z = axes[2][i[2]]
    hug = 0.25 * max(0.0, s - 4.0)                  # stay near the skin rather than floating off it
    lateral = 0.08 * max(0.0, z - 14.0)              # keep off the lateral face of the pinna
    return 1.0 + hug + lateral


def astar(a, b):
    a = a if free[a] else nearest_free(a)
    b = b if free[b] else nearest_free(b)
    openq = [(0.0, a)]
    g = {a: 0.0}
    came = {}
    bb = np.array(b)
    while openq:
        _, cur = heapq.heappop(openq)
        if cur == b:
            break
        for d in NB:
            nx = (cur[0] + d[0], cur[1] + d[1], cur[2] + d[2])
            if not (0 <= nx[0] < shape[0] and 0 <= nx[1] < shape[1] and 0 <= nx[2] < shape[2]) or not free[nx]:
                continue
            ng = g[cur] + np.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2) * cell_cost(nx)
            if ng < g.get(nx, 1e18):
                g[nx] = ng
                came[nx] = cur
                heapq.heappush(openq, (ng + np.linalg.norm(np.array(nx) - bb), nx))
    path = [b]
    while path[-1] != a:
        path.append(came[path[-1]])
    return [lo + np.array(p) * H for p in path[::-1]]


def lateral_skin(x, y):
    ts = np.arange(0, 70, 0.25)
    Q = np.array([x, y, 55.0])[None] + ts[:, None] * np.array([0, 0, -1.0])[None]
    s = sdist(Q)
    hit = np.where(s < CLEAR_GRID + 0.5)[0]
    return Q[hit[0]] if len(hit) else None


way = [start]
for dx, dy in ((7.0, 12.0), (9.5, 22.0)):          # in front of the crus and root of the helix
    h = lateral_skin(boss[0] + dx, boss[1] + dy)
    if h is not None:
        way.append(h)
way.append(pod_top)
pts = [way[0]]
for a, b in zip(way[:-1], way[1:]):
    seg = astar(to_idx(a), to_idx(b))
    pts += seg[1:]
pts[-1] = pod_top
pts = np.asarray(pts)


def resample(p, step=0.5):
    t = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    u = np.linspace(0, t[-1], max(8, int(t[-1] / step)))
    return np.stack([np.interp(u, t, p[:, k]) for k in range(3)], 1)


pts = resample(np.vstack([boss, pts]))
for it in range(1200):
    q = pts.copy()
    q[2:-2] = 0.5 * pts[2:-2] + 0.25 * (pts[1:-3] + pts[3:-1])
    ok = sdist(q) >= NEED
    ok[:3] = False; ok[-3:] = False
    pts[ok] = q[ok]
# final check: samples and segment midpoints (the tube is drawn between samples)
mid = 0.5 * (pts[1:] + pts[:-1])
chk = np.vstack([pts[4:-4], mid[4:-4]])
s = sdist(chk)
seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
d = np.diff(pts, axis=0) / seg[:, None]
turn = np.degrees(np.arccos(np.clip((d[:-1] * d[1:]).sum(1), -1, 1)))
v["cable"] = pts.round(3).tolist()
json.dump(A, open(js, "w"), indent=1)
print(dict(min_clearance=round(float(s.min()), 2), need=NEED, max_seg=round(float(seg.max()), 2),
           max_turn_deg=round(float(turn[3:-3].max()), 1), length_mm=round(float(seg.sum()), 1),
           top_y=round(float(pts[:, 1].max()), 1), max_z=round(float(pts[:, 2].max()), 1)))
