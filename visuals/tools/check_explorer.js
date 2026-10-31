// One-shot check of the explorer: desktop + 400 px, console errors, concept switching, screenshot.
// usage: node check_explorer.js <playwright-core dir> <chrome binary> <url> <screenshot.png>
const [pwDir, chrome, url, shot] = process.argv.slice(2);
const { chromium } = require(pwDir);
(async () => {
  const browser = await chromium.launch({ executablePath: chrome, args: ["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"] });
  const page = await browser.newPage({ viewport: { width: 1360, height: 900 } });
  const errors = [];
  page.on("console", m => { if (m.type() === "error") errors.push(m.text()); });
  page.on("pageerror", e => errors.push("pageerror: " + e.message));
  await page.goto(url, { waitUntil: "load" });
  await page.waitForTimeout(6000);
  const res = await page.evaluate(async () => {
    const out = { cut: document.getElementById("t-cut").checked };
    const btns = [...document.querySelectorAll("#variant button")];
    out.buttons = btns.map(b => b.textContent);
    for (const b of btns) {
      b.click(); await new Promise(r => setTimeout(r, 400));
      out[b.dataset.v] = { stats: document.getElementById("stats").innerText.split("\n").slice(0, 6).join(" | "), parts: document.querySelectorAll("#part-list button").length };
    }
    btns[btns.length - 1].click();
    const ex = document.getElementById("explode"); ex.value = 60; ex.dispatchEvent(new Event("input"));
    await new Promise(r => setTimeout(r, 400));
    return out;
  });
  await page.screenshot({ path: shot.replace(".png", "_bte_explode.png") });
  await page.evaluate(() => { document.querySelector('#variant button').click(); const ex = document.getElementById("explode"); ex.value = 0; ex.dispatchEvent(new Event("input")); });
  await page.waitForTimeout(500);
  await page.screenshot({ path: shot });
  await page.setViewportSize({ width: 400, height: 860 });
  await page.waitForTimeout(800);
  res.phone = await page.evaluate(() => ({ hscroll: document.documentElement.scrollWidth > document.documentElement.clientWidth, ruler: !document.getElementById("ruler").hidden }));
  res.errors = errors;
  console.log(JSON.stringify(res, null, 1));
  await browser.close();
})();
