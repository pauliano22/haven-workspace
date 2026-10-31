"""Turn the variant explorer into the shape-concept explorer (shared ear, N concepts, BTE pod).

usage: patch_concepts.py <in.html> <assets.glb> <assets.json> <out.html>
Input is the previous visuals/haven_ear_explorer.html (variant-aware build). Concepts are data:
each entry in assets.json "variants" gives a shell node, part frames, pose, stats and text.
"""
import base64
import json
import re
import sys

src, glb, ajson, out = sys.argv[1:5]
s = open(src).read()
A = json.load(open(ajson))


def rep(a, b, count=1):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b, count)


def cut(start, end):
    i = s.index(start)
    j = s.index(end, i)
    return s[:i], s[i:j], s[j:]


# ---------------------------------------------------------------- embedded assets
s = re.sub(r'(<script id="haven-assets" type="application/json">).*?(</script>)',
           lambda m: m.group(1) + json.dumps(A, separators=(",", ":")) + m.group(2), s, count=1, flags=re.S)
s = re.sub(r'(<script>window\.HAVEN_GLB = ")[^"]*(";</script>)',
           lambda m: m.group(1) + base64.b64encode(open(glb, "rb").read()).decode() + m.group(2), s, count=1)

# ---------------------------------------------------------------- page text
rep("Switch the design variant to compare the current parts with a smaller battery and speaker.",
    "Switch between shape concepts: all use the same chosen parts, only the shape changes.")
rep("Earbuds: Haven v2 ergonomic shells (stacked layout), each seated by the same fit simulation.",
    "Earbuds: Haven v2 shape concepts, each seated in this ear by the same fit simulation and scored in six scanned ears.")
rep("<h2>Design variant</h2>", "<h2>Shape concept</h2>")
rep("Haven v2 · ergonomic shell in a scanned ear · all sizes in mm", "Haven v2 · shape concepts in a scanned ear · all sizes in mm")
rep("and the earbud is the v2 ergonomic shell, seated where the fit simulation put it.", "and each concept is seated where the fit simulation put it.")
rep('aria-label="Design variant"', 'aria-label="Shape concept"')
rep(".variant { margin-bottom: 8px; }", ".variant { margin-bottom: 8px; flex-wrap: wrap; }")
rep(".stats dd { margin: 0; font-variant-numeric: tabular-nums; }",
    ".stats dd { margin: 0; font-variant-numeric: tabular-nums; }\n.stats .pro { color: var(--left, #2f6b52); }\n.stats .con { color: var(--right, #94600f); }\n.stats .warn { grid-column: 1 / -1; font-size: 0.8rem; color: var(--ink-soft); font-style: italic; }")

# ---------------------------------------------------------------- extra part descriptions
rep("  // ------------------------------------------------------------ the bud",
    """  Object.assign(PARTS, {
    flex: { name: "Flex circuit", pn: "Thin flex in the in-ear unit", size: "6 × 6 × 0.6", role: "Carries the speaker and outer-mic wires from the in-ear unit to the cable.", status: ["concept", "Behind-the-ear concept only"] },
    cable: { name: "Cable", pn: "Thin cable over the ear (route illustrative)", size: "~Ø1.2", role: "Connects the in-ear unit to the pod behind the ear: speaker drive, mic data and power.", status: ["concept", "Route drawn for illustration, not fitted"] },
    pod: { name: "Behind-ear pod", pn: "CP1454 + v2 board + radio + charging pads", size: "17.8 × 33.4 × 9.2 · 4.77 g", role: "Holds the battery and electronics behind the ear, like a hearing aid. Its weight rests on the head, not in the ear.", status: ["concept", "Resting position on the head is approximate"] }
  });

  // ------------------------------------------------------------ the bud""")

# ---------------------------------------------------------------- concept data
rep("""    const geo = nodeGeo("shell_" + key); geo.computeBoundingBox();
    VAR[key] = { a, PF, geo, C: geo.boundingBox.getCenter(new THREE.Vector3()) };
  }""", """    const geo = nodeGeo("shell_" + key); geo.computeBoundingBox();
    VAR[key] = { a, PF, geo, C: geo.boundingBox.getCenter(new THREE.Vector3()) };
    if (a.pod) {
      const pPF = {};
      for (const k in a.pod.parts) {
        const p = a.pod.parts[k], m = new THREE.Matrix4().fromArray(p.matrix);
        pPF[k] = { m, ext: p.extents, c: new THREE.Vector3().setFromMatrixPosition(m), ax: new THREE.Vector3().setFromMatrixColumn(m, 0).normalize() };
      }
      const pg = nodeGeo("shell_" + key + "_pod"); pg.computeBoundingBox();
      VAR[key].pod = { PF: pPF, geo: pg, C: pg.boundingBox.getCenter(new THREE.Vector3()), top: pg.boundingBox.max.y, M: new THREE.Matrix4().fromArray(a.pod.matrix) };
    }
  }""")

# ---------------------------------------------------------------- generic bud builder
pre, _, post = cut("  function buildBud(shared, key) {", "  // ------------------------------------------------------------ the ear")
BUD = r"""  // Parts are built from their frames (x = thin or cylinder axis), so any concept's layout works.
  function buildParts(PF, parent, add, SHELL_C, batLabel, nozzle) {
    const inFrame = (id, obj) => { const gr = new THREE.Group(); gr.add(obj); gr.applyMatrix4(PF[id].m); return gr; };
    const side = (id, toward) => Math.sign(PF[id].ax.dot(toward.clone().sub(PF[id].c))) || 1;
    const has = id => !!PF[id];
    const boards = ["pcb", "codec_pcb"].filter(has);
    const nearBoard = id => boards.reduce((b, k) => (!b || PF[k].c.distanceTo(PF[id].c) < PF[b].c.distanceTo(PF[id].c)) ? k : b, null);
    const epoxy = phys(0x1c1e20, { roughness: 0.5 });
    const gold = phys(0xd9a83c, { metalness: 1, roughness: 0.26 });
    if (has("driver")) {
      const D = PF.driver, d = Math.max(D.ext[1], D.ext[2]), sD = side("driver", nozzle || SHELL_C);
      const drv = new THREE.Group();
      drv.add(cylX(d, D.ext[0], phys(0x3f474f, { metalness: 0.9, roughness: 0.38 }), 56));
      drv.add(discX(d * 0.42, phys(0xffffff, { map: TEX.grille, metalness: 0.6, roughness: 0.45 }), sD * (D.ext[0] / 2 + 0.01), sD));
      add("driver", inFrame("driver", drv), parent);
    }
    if (has("battery")) {
      const Bt = PF.battery, bd = Math.max(Bt.ext[1], Bt.ext[2]);
      const sB = -side("battery", has("driver") ? PF.driver.c : SHELL_C);
      const bat = new THREE.Group();
      bat.add(cylX(bd, Bt.ext[0], phys(0xc6cace, { metalness: 1, roughness: 0.24 }), 64));
      bat.add(discX(bd / 2 * 0.93, phys(0xffffff, { map: batteryTex(batLabel), metalness: 0.85, roughness: 0.3 }), sB * (Bt.ext[0] / 2 + 0.01), sB));
      add("battery", inFrame("battery", bat), parent);
    }
    const pcbM = phys(0xffffff, { map: TEX.pcb, roughness: 0.32, clearcoat: 0.7, clearcoatRoughness: 0.15 });
    const pcbEdge = phys(0x23402c, { roughness: 0.6 });
    boards.forEach(k => { const P = PF[k]; add("pcb", inFrame(k, boxAt(P.ext[0], P.ext[1], P.ext[2], 0, 0, 0, [pcbM, pcbM, pcbEdge, pcbEdge, pcbEdge, pcbEdge])), parent); });
    if (has("module")) {
      const Mo = PF.module, ref = nearBoard("module"), sM = ref ? -side("module", PF[ref].c) : 1;
      const canSide = phys(0xb4b9be, { metalness: 0.9, roughness: 0.35 });
      const mats = [canSide, canSide, canSide, canSide, canSide, canSide]; mats[sM > 0 ? 0 : 1] = phys(0xffffff, { map: TEX.module, metalness: 0.85, roughness: 0.32 });
      add("module", inFrame("module", boxAt(Mo.ext[0], Mo.ext[1], Mo.ext[2], 0, 0, 0, mats)), parent);
    }
    // chips under a board: all of them on a single board, or split codec / power across two
    const chipRegion = (rid, set) => {
      if (!has(rid)) return;
      const BP = PF[rid], ref = nearBoard(rid), sBP = ref ? side(rid, PF[ref].c) : 1, yS = BP.ext[1] / 9, zS = BP.ext[2] / 13;
      const atPcb = h => sBP * (BP.ext[0] / 2 - h / 2);
      const put = (id, obj) => add(id, inFrame(rid, obj), parent);
      const chipBox = (tex, sx, sy, h, x, y) => {
        const mats = [epoxy, epoxy, epoxy, epoxy, epoxy, epoxy]; mats[sBP > 0 ? 1 : 0] = phys(0xffffff, { map: tex, roughness: 0.5 });
        return boxAt(h, sx, sy, atPcb(h), x * yS, y * zS, mats);
      };
      if (set !== "pmic") {
        put("codec", chipBox(TEX.codec, 3.0, 2.7, 0.6, set === "all" ? 1.6 : 0.0, set === "all" ? 2.4 : 1.2));
        const xt = new THREE.Group(), xm = phys(0xd0d4d8, { metalness: 1, roughness: 0.3 });
        xt.add(boxAt(0.5, 2.0, 1.6, atPcb(0.5), -2.4 * yS, (set === "all" ? 2.8 : -2.2) * zS, xm));
        if (set === "all") xt.add(boxAt(0.5, 1.6, 1.0, atPcb(0.5), 2.7 * yS, -3.6 * zS, xm));
        put("xtal", xt);
      }
      if (set !== "codec") put("pmic", chipBox(TEX.pmic, 2.1, 2.1, 0.55, -2.3, set === "all" ? -3.2 : 0.8));
      const pas = new THREE.Group();
      const capM = phys(0x9b8160, { roughness: 0.55 }), resM = phys(0x202224, { roughness: 0.5 }), term = phys(0xd8dbde, { metalness: 1, roughness: 0.3 });
      const spots = set === "all" ? [[-0.4, 0.6], [0.6, -0.8], [-1.2, -1.4], [3.4, 0.4], [3.5, 3.9], [-3.4, 0.2], [-0.6, 4.8], [1.2, -5.2], [-3.3, -5.4], [0.2, -3.0], [3.0, -1.6], [-1.5, 5.6], [2.2, 5.6], [-3.6, 3.9]]
        : set === "codec" ? [[2.6, 1.0], [2.8, -1.4], [-2.6, 1.6], [0.4, -3.6], [-0.8, 4.6]] : [[1.0, 2.6], [2.8, -0.6], [-0.6, -2.8], [2.6, 3.8], [-3.2, 3.4], [0.6, 5.2]];
      spots.forEach(([x, y], i) => {
        const horiz = i % 3 === 0, L = 0.6, W = 0.3, cx = atPcb(0.3);
        pas.add(boxAt(0.3, horiz ? L * 0.6 : W, horiz ? W : L * 0.6, cx, x * yS, y * zS, i % 2 ? capM : resM));
        [-1, 1].forEach(sg => pas.add(boxAt(0.3, horiz ? 0.12 : W, horiz ? W : 0.12, cx, (x + (horiz ? sg * 0.24 : 0)) * yS, (y + (horiz ? 0 : sg * 0.24)) * zS, term)));
      });
      put("passives", pas);
      if (set !== "codec") {
        const swd = new THREE.Group();
        [-1.8, -0.6, 0.6, 1.8].forEach(y => { const d = discX(0.4, gold, sBP * (BP.ext[0] / 2 - 0.02), -sBP, 20); d.position.y = 3.7 * yS; d.position.z = (y - 4.6) * zS; swd.add(d); });
        put("swd", swd);
      }
    };
    chipRegion("bottom_parts", "all");
    chipRegion("codec_parts", "codec");
    chipRegion("pmic_parts", boards.length > 1 ? "pmic" : "all");
    if (has("mic")) {
      const Mi = PF.mic, sMi = -side("mic", SHELL_C);
      const mats = [epoxy, epoxy, epoxy, epoxy, epoxy, epoxy]; mats[sMi > 0 ? 0 : 1] = phys(0xc9ced2, { metalness: 0.9, roughness: 0.3 });
      add("mic", inFrame("mic", boxAt(Mi.ext[0], Mi.ext[1], Mi.ext[2], 0, 0, 0, mats)), parent);
    }
    if (has("magnet")) add("magnet", inFrame("magnet", cylX(Math.max(PF.magnet.ext[1], PF.magnet.ext[2]), PF.magnet.ext[0], phys(0x7c8288, { metalness: 1, roughness: 0.3 }), 32)), parent);
    if (has("pad1")) {
      const padG = new THREE.Group();
      ["pad1", "pad2"].filter(has).forEach(k => padG.add(inFrame(k, cylX(Math.max(PF[k].ext[1], PF[k].ext[2]), PF[k].ext[0], gold, 28))));
      add("pads", padG, parent);
    }
    if (has("flex")) { const F = PF.flex; add("flex", inFrame("flex", boxAt(F.ext[0], F.ext[1], F.ext[2], 0, 0, 0, phys(0xc8862a, { roughness: 0.45, clearcoat: 0.4 }))), parent); }
    if (has("cable_boss")) { const Cb = PF.cable_boss; add("cable", inFrame("cable_boss", cylX(Math.max(Cb.ext[1], Cb.ext[2]), Cb.ext[0], phys(0x6f757b, { roughness: 0.5 }), 24)), parent); }
  }

  function buildBud(shared, key) {
    const V0 = VAR[key];
    const g = new THREE.Group();
    const items = {}, extra = [];
    const add = (id, obj, parent = g) => { parent.add(obj); (items[id] = items[id] || []).push(obj); if (!shared) obj.traverse(o => { if (o.isMesh) reg(o, id); }); return obj; };

    const resin = () => phys(0xe9ece8, { roughness: 0.32, clearcoat: 0.5, clearcoatRoughness: 0.25, transparent: true, opacity: 0.3, depthWrite: false, side: THREE.DoubleSide, envMapIntensity: 1.2 });
    const shell = new THREE.Mesh(V0.geo, resin());
    shell.renderOrder = 5; shell.castShadow = false;
    add("shell", shell);

    const resinSolid = phys(0xe6e9e5, { roughness: 0.38, clearcoat: 0.4, clearcoatRoughness: 0.3, side: THREE.DoubleSide });
    const nozPts = [[1.5, -0.8], [3.0, -0.8], [2.6, 0.2], [2.6, 3.7], [3.0, 4.3], [3.0, 4.9], [2.6, 5.5], [1.5, 5.5]].map(p => new THREE.Vector2(p[0], p[1]));
    const noz = new THREE.Mesh(new THREE.LatheGeometry(nozPts, 48), resinSolid);
    noz.position.copy(NOZ_BASE); orientY(noz, NOZ_AXIS); noz.castShadow = true;
    add("nozzle", noz);
    const foam = phys(0x4b5156, { roughness: 1.0, bumpMap: TEX.foamBump, bumpScale: 0.06, sheen: col(0x2f3438), side: THREE.DoubleSide });
    const tipPts = [[2.75, 0.8], [3.3, 0.95], [3.95, 1.7], [4.25, 3.0], [4.25, 4.6], [3.95, 5.8], [3.0, 6.55], [1.6, 6.6]].map(p => new THREE.Vector2(p[0], p[1]));
    const tip = new THREE.Mesh(new THREE.LatheGeometry(tipPts, 56), foam);
    tip.scale.set(1, 1, 1.16);
    tip.position.copy(NOZ_BASE); orientY(tip, NOZ_AXIS); tip.castShadow = true;
    add("eartip", tip);

    buildParts(V0.PF, g, add, V0.C, V0.a.battery_label, NOZ_BASE);
    if (V0.pod) {
      const pg = new THREE.Group();
      const ps = new THREE.Mesh(V0.pod.geo, resin()); ps.renderOrder = 5;
      add("pod", ps, pg);
      buildParts(V0.pod.PF, pg, add, V0.pod.C, V0.a.battery_label, null);
      pg.applyMatrix4(V0.pod.M);
      extra.push(pg);
    }
    g.traverse(o => { if (o.isMesh && o !== shell) { o.castShadow = true; o.receiveShadow = true; } });
    extra.forEach(e => e.traverse(o => { if (o.isMesh && o.userData.part !== "pod") { o.castShadow = true; o.receiveShadow = true; } }));
    return { group: g, items, extra };
  }

"""
s = pre + BUD + post

# ---------------------------------------------------------------- scene placement, explode, visibility
rep("""    earRoot.add(v.bud.group);
    const o = k => OUT.clone().multiplyScalar(k);
    v.explode = { driver: o(3), battery: o(9), passives: o(16), codec: o(16), pmic: o(16), xtal: o(16), swd: o(16), pcb: o(21), module: o(27) };
    v.explode.mic = v.PF.mic.c.clone().sub(v.C).normalize().multiplyScalar(10).add(o(14));
    for (const id in v.bud.items) v.bud.items[id].forEach(ob => { ob.userData.base = ob.position.clone(); });
  }""", """    earRoot.add(v.bud.group);
    v.bud.extra.forEach(e => earRoot.add(e));
    // explode: each part moves out from its own housing's centre, plus outward from the head
    const podOut = V(0, 0, 1);
    for (const id in v.bud.items) v.bud.items[id].forEach(ob => {
      ob.userData.base = ob.position.clone();
      if (["shell", "nozzle", "eartip", "pod"].includes(id)) return;
      const inPod = v.pod && ob.parent !== v.bud.group;
      const c0 = inPod ? v.pod.C : v.C;
      const dir = ob.position.clone().sub(c0); if (dir.lengthSq() < 1e-6) dir.copy(inPod ? podOut : OUT);
      ob.userData.ex = dir.normalize().multiplyScalar(9).addScaledVector(inPod ? podOut : OUT, 5);
    });
  }
  earRoot.updateMatrixWorld(true);
  // behind-the-ear: a cable from the in-ear unit's boss over the ear to the top of the pod (route illustrative)
  for (const key in VAR) {
    const v = VAR[key];
    if (!v.pod || !v.bud.items.cable) continue;
    const a0 = new THREE.Box3().setFromObject(v.bud.items.cable[0]).getCenter(new THREE.Vector3());
    const top = V(v.pod.C.x, v.pod.top - 1.5, v.pod.C.z).applyMatrix4(v.bud.extra[0].matrixWorld);
    const path = new THREE.CatmullRomCurve3([a0, a0.clone().add(V(0, 7, 6)), V(a0.x - 6, 31, a0.z + 6), V(top.x + 3, top.y + 9, top.z + 4), top]);
    const cable = new THREE.Mesh(new THREE.TubeGeometry(path, 80, 0.6, 10, false), phys(0x3b4045, { roughness: 0.45, clearcoat: 0.3 }));
    cable.castShadow = true; reg(cable, "cable"); v.bud.items.cable.push(cable); v.bud.extra.push(cable); earRoot.add(cable);
  }""")
rep("""  ORDER.slice(1).forEach(k => { VAR[k].bud.group.visible = false; });""",
    """  const showConcept = (k, on) => { VAR[k].bud.group.visible = on; VAR[k].bud.extra.forEach(e => { e.visible = on; }); };
  ORDER.slice(1).forEach(k => showConcept(k, false));""")
rep("""    const EXPLODE = VAR[active].explode;
    for (const id in EXPLODE) (bud.items[id] || []).forEach(o => o.position.copy(o.userData.base).add(EXPLODE[id].clone().multiplyScalar(e)));""",
    """    for (const id in bud.items) bud.items[id].forEach(o => { if (o.userData.ex) o.position.copy(o.userData.base).addScaledVector(o.userData.ex, e); });""")
rep("""  function setShell(see) { for (const k in VAR) { const m = VAR[k].bud.items.shell[0].material; m.opacity = see ? 0.32 : 1; m.depthWrite = !see; m.needsUpdate = true; } }""",
    """  function setShell(see) { for (const k in VAR) ["shell", "pod"].forEach(id => (VAR[k].bud.items[id] || []).forEach(o => { const m = o.material; m.opacity = see ? 0.32 : 1; m.depthWrite = !see; m.needsUpdate = true; })); }""")

# ---------------------------------------------------------------- cases: only for concepts that have one
rep("""  ORDER.forEach(k => { CASES[k] = buildCase(k); });
  ORDER.slice(1).forEach(k => { CASES[k].visible = false; });
  caseRoot.userData.lid = CASES[active].userData.lid;""",
    """  ORDER.forEach(k => { if (VAR[k].a.case) CASES[k] = buildCase(k); });
  for (const k in CASES) if (k !== active) CASES[k].visible = false;
  caseRoot.userData.lid = CASES[active] ? CASES[active].userData.lid : new THREE.Group();""")

# ---------------------------------------------------------------- stats + switching
pre, _, post = cut("  function renderStats() {", "  ORDER.forEach(k => {\n    const b = document.createElement(\"button\");")
STATS = r"""  function renderStats() {
    const c = VAR[active].a, st = c.stats;
    for (const id in c.text) Object.assign(PARTS[id], c.text[id]);
    PARTS.shell.pn = c.label + " shell (v2, chosen parts)";
    PARTS.shell.size = `${st.bbox.map(x => x.toFixed(1)).join(" × ")} · ${st.mass}`;
    const sg = x => (x > 0 ? "+" : x < 0 ? "−" : "") + Math.abs(x).toFixed(1);
    if (CASES[active]) {
      const d = CASES[active].userData.dims.map(x => x.toFixed(1)).join(" × ");
      PARTS.caseshell.size = d;
      $("case-note").textContent = `Case envelope ${d} mm, sized around the ${c.label.toLowerCase()} buds. Buds lie on their charging-pad side over spring pins; magnets pull them into place. Paul chose a larger case battery (about 3 full recharges) over a smaller case.`;
    } else {
      $("case-note").textContent = `Case not designed yet for the ${c.label.toLowerCase()} concept. ${c.key === "bte" ? "It would need room for the pod and a stowed cable." : "A stem needs tall slots instead of shallow pockets."}`;
    }
    $("stats").innerHTML = `<dt>Size</dt><dd>${st.bbox.map(x => x.toFixed(1)).join(" × ")} mm</dd>`
      + `<dt>Weight</dt><dd>${st.mass}</dd>`
      + `<dt>Skin compression</dt><dd>${st.comp[0].toFixed(1)} mm avg · ${st.comp[1].toFixed(1)} mm worst</dd>`
      + `<dt>Past the tragus</dt><dd>${sg(st.prot[0])} mm avg · ${sg(st.prot[1])} mm worst</dd>`
      + `<dt>Tipping moment</dt><dd>${st.moment.toFixed(2)} N·mm (lower stays in better)</dd>`
      + `<dt>Battery life</dt><dd>${st.life[0]} loud · ${st.life[1]} quiet</dd>`
      + `<dt>Pro</dt><dd class="pro">${c.pro}</dd><dt>Con</dt><dd class="con">${c.con}</dd>`
      + `<dd class="warn">Averages and worst case over 6 scanned ears.${c.note ? " " + c.note : ""}</dd>`;
    document.querySelectorAll("#variant button").forEach(b => b.setAttribute("aria-pressed", b.dataset.v === active ? "true" : "false"));
    const list = $("part-list"); list.innerHTML = "";
    fillList(list, EAR_LIST.filter(id => bud.items[id] || ["canal", "eardrum", "pinna"].includes(id)));
    if (state.selected) showInfo(state.selected);
  }
  function setVariant(key) {
    if (key === active || !VAR[key]) return;
    showConcept(active, false); if (CASES[active]) CASES[active].visible = false;
    const r = caseRoot.userData.lid.rotation.x;
    active = key; bud = VAR[key].bud; shellMesh = bud.items.shell[0];
    showConcept(key, true);
    if (CASES[key]) { CASES[key].visible = true; caseRoot.userData.lid = CASES[key].userData.lid; caseRoot.userData.lid.rotation.x = r; }
    if (state.selected && !bud.items[state.selected] && !["canal", "eardrum", "pinna"].includes(state.selected)) select(null);
    placeAnchors(); STEPS = buildSteps(); buildCams();
    applyExplode(); renderStats();
    if (state.mode === "how") renderStep();
  }
"""
s = pre + STATS + post

rep('const EAR_LIST = ["shell", "nozzle", "eartip", "module", "pcb", "codec", "pmic", "xtal", "passives", "swd", "mic", "driver", "battery", "pads", "magnet", "canal", "eardrum", "pinna"];',
    'const EAR_LIST = ["shell", "nozzle", "eartip", "module", "pcb", "codec", "pmic", "xtal", "passives", "swd", "mic", "driver", "battery", "pads", "magnet", "flex", "cable", "pod", "canal", "eardrum", "pinna"];')
rep('const LABEL_IDS = ["module", "pcb", "codec", "pmic", "passives", "battery", "driver", "mic", "nozzle", "eartip", "magnet", "pads"];',
    'const LABEL_IDS = ["module", "pcb", "codec", "pmic", "passives", "battery", "driver", "mic", "nozzle", "eartip", "magnet", "pads", "flex", "pod"];')
rep("""    LABEL_IDS.forEach(id => {
      const el = tag("p-" + id, PARTS[id].name, "", () => select(id, false));""",
    """    LABEL_IDS.forEach(id => {
      if (!bud.items[id]) { if (tagEls["p-" + id]) tagEls["p-" + id].style.display = "none"; return; }
      const el = tag("p-" + id, PARTS[id].name, "", () => select(id, false));""")
rep("""const inner = hits.find(h => !["shell", "caseshell"].includes(h.object.userData.part)""",
    """const inner = hits.find(h => !["shell", "caseshell", "pod"].includes(h.object.userData.part)""")
open(out, "w").write(s)
print("ok", round(len(s) / 1e6, 2), "MB")
