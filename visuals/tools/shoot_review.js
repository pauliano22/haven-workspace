// Review shots: every concept from out / side (cut-away) / close / below / front, explode 0, default finish.
// usage: node shoot_review.js <playwright-core dir> <chrome binary> <url> <out dir>
const [pwDir, chrome, url, outDir, only] = process.argv.slice(2);   // optional 5th arg: comma-separated concept keys
const { chromium } = require(pwDir);
(async () => {
  const browser = await chromium.launch({ executablePath: chrome, args: ["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"] });
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
  const errors = [];
  page.on("pageerror", e => errors.push(e.message));
  page.on("console", m => { if (m.type() === "error" && !/favicon|404/.test(m.text())) errors.push(m.text()); });
  await page.goto(url, { waitUntil: "load" });
  await page.waitForTimeout(7000);
  const keys = await page.evaluate(() => [...document.querySelectorAll("#variant button")].map(b => b.dataset.v));
  for (const k of keys.filter(k => !only || only.split(",").includes(k))) {
    for (const view of ["out", "side", "close", "below", "front"]) {
      await page.evaluate(([k, view]) => {
        document.querySelector(`#variant button[data-v="${k}"]`).click();
        const ex = document.getElementById("explode"); ex.value = 0; ex.dispatchEvent(new Event("input"));
        const cut = document.getElementById("t-cut");
        const wantCut = view === "side";
        if (cut.checked !== wantCut) cut.click();
        if (["out", "side", "close"].includes(view)) document.getElementById("cam-" + view).click();
        if (view === "side" && !cut.checked) cut.click();
        if (["below", "front"].includes(view)) window.havenCam(view);
      }, [k, view]);
      await page.waitForTimeout(2200);
      const canvas = await page.$("canvas");
      await canvas.screenshot({ path: `${outDir}/${k}_${view}.png` });
    }
  }
  console.log(JSON.stringify({ keys, errors }));
  await browser.close();
})();
