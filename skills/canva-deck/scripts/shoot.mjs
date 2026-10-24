// Screenshot every slide of a deck file before it is hosted (references/pitfalls.md 8: import copies the layout as-is).
// Usage: node shoot.mjs <deck.html> [out-dir]   → out-dir/01.png, 02.png … (default: ./shots)
// Needs Playwright: `npm i -D playwright && npx playwright install chromium` (or run with `npx -p playwright node shoot.mjs …`).
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [file, out = "shots"] = process.argv.slice(2);
if (!file) {
  console.error("usage: node shoot.mjs <deck.html> [out-dir]");
  process.exit(2);
}
mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(pathToFileURL(resolve(file)).href, { waitUntil: "networkidle" });
await page.evaluate(() => document.fonts.ready);
const slides = await page.locator('section[data-document-role="page"]').all();
for (const [i, slide] of slides.entries()) {
  const name = `${String(i + 1).padStart(2, "0")}.png`;
  await slide.screenshot({ path: `${out}/${name}` });
  console.log(`${name}  ${(await slide.getAttribute("data-label")) ?? ""}`);
}
await browser.close();
console.log(`${slides.length} slides → ${out}/  (look at every one before hosting)`);
