// Screenshot every shape concept from three camera presets, for visual review.
// usage: node shoot_concepts.js <playwright-core dir> <chrome binary> <url> <out dir>
const [pwDir, chrome, url, outDir] = process.argv.slice(2);
const { chromium } = require(pwDir);
(async () => {
  const browser = await chromium.launch({ executablePath: chrome, args: ["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"] });
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
  await page.goto(url, { waitUntil: "load" });
  await page.waitForTimeout(6000);
  const keys = await page.evaluate(() => [...document.querySelectorAll("#variant button")].map(b => b.dataset.v));
  for (const k of keys) {
    for (const cam of ["cam-out", "cam-side", "cam-close"]) {
      await page.evaluate(([k, cam]) => {
        document.querySelector(`#variant button[data-v="${k}"]`).click();
        const ex = document.getElementById("explode"); ex.value = 0; ex.dispatchEvent(new Event("input"));
        document.getElementById(cam).click();
      }, [k, cam]);
      await page.waitForTimeout(2500);
      const canvas = await page.$("canvas");
      await canvas.screenshot({ path: `${outDir}/${k}_${cam.replace("cam-", "")}.png` });
    }
  }
  await browser.close();
})();
