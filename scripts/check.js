// Check a built page: node check.js N  (reads dayN.html, writes screenshots to shots/)
const { chromium } = require('playwright');
const fs = require('fs'), os = require('os'), path = require('path');
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'chk-'));
// Browser: $CHROME if set, else a preinstalled /opt/pw-browsers/chromium if present, else Playwright's own download
const launchOpts = () => { const p = process.env.CHROME || '/opt/pw-browsers/chromium'; return require('fs').existsSync(p) ? { executablePath: p } : {}; };
(async () => {
  fs.mkdirSync('shots', { recursive: true });
  const day = process.argv[2];
  const html = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + fs.readFileSync(`day${day}.html`, 'utf8') + '</body></html>';
  fs.writeFileSync(path.join(TMP, `t${day}.html`), html);
  const browser = await chromium.launch(launchOpts());
  for (const [wd, tag] of [[1040, 'w'], [400, 'n']]) {
    const page = await browser.newPage({ viewport: { width: wd, height: 900 }, reducedMotion: 'reduce' });
    const errs = [];
    page.on('pageerror', e => errs.push('pageerror: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    await page.goto('file://' + path.join(TMP, `t${day}.html`));
    await page.waitForTimeout(800);
    await page.locator('.player').screenshot({ path: `shots/d${day}_${tag}_rest.png` });
    const n = await page.locator('.chap').count();
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    for (let i = 0; i < n; i++) {
      await page.locator('#chap' + i).click();
      await page.waitForTimeout(250);
      if (tag === 'w' || i % 3 === 0) await page.locator('.player').screenshot({ path: `shots/d${day}_${tag}_${String(i).padStart(2,'0')}.png` });
    }
    // overflow check per scene in stage
    console.log(tag, 'scenes', n, 'scrollWidth', sw, 'errors', JSON.stringify(errs));
    await page.close();
  }
  // live play test without reduced motion
  const page = await browser.newPage({ viewport: { width: 1040, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await page.goto('file://' + path.join(TMP, `t${day}.html`));
  await page.locator('#seek').click({ position: { x: 300, y: 6 } });
  await page.waitForTimeout(300);
  const info = await page.evaluate(() => ({ t: document.getElementById('nar').currentTime, d: document.getElementById('nar').duration, time: document.getElementById('time').textContent }));
  console.log('seek test', JSON.stringify(info), 'errors', JSON.stringify(errs));
  await browser.close();
})();
