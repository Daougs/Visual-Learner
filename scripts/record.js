// Record an explainer page to MP4: node record.js dayN.html out.mp4 narration.mp3
// The page's capture mode drives the timeline by wall clock; Playwright records the screen; ffmpeg adds the MP3.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
// Browser: $CHROME if set, else a preinstalled /opt/pw-browsers/chromium if present, else Playwright's own download
const launchOpts = () => { const p = process.env.CHROME || '/opt/pw-browsers/chromium'; return require('fs').existsSync(p) ? { executablePath: p } : {}; };
(async () => {
  const [src, out, mp3] = process.argv.slice(2);
  const tmp = fs.mkdtempSync('/tmp/rec-');
  // Google Fonts may be unreachable from the recorder, so load the same faces from local @fontsource files
  const nm = path.join(__dirname, 'node_modules');
  const ff = (fam, file, w) => `@font-face{font-family:"${fam}";src:url("file://${nm}/${file}") format("woff2");font-weight:${w};font-display:block}`;
  const fonts = '<style>' + [
    ff('Bricolage Grotesque', '@fontsource-variable/bricolage-grotesque/files/bricolage-grotesque-latin-standard-normal.woff2', '200 800'),
    ff('Instrument Sans', '@fontsource/instrument-sans/files/instrument-sans-latin-400-normal.woff2', 400),
    ff('Instrument Sans', '@fontsource/instrument-sans/files/instrument-sans-latin-500-normal.woff2', 500),
    ff('Instrument Sans', '@fontsource/instrument-sans/files/instrument-sans-latin-600-normal.woff2', 600),
    ff('JetBrains Mono', '@fontsource/jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2', 500),
    ff('JetBrains Mono', '@fontsource/jetbrains-mono/files/jetbrains-mono-latin-700-normal.woff2', 700),
  ].join('') + '</style>';
  const html = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + fonts + '</head><body>' + fs.readFileSync(src, 'utf8') + '</body></html>';
  fs.writeFileSync(path.join(tmp, 'p.html'), html);
  const browser = await chromium.launch(launchOpts());
  const W = 1280, H = 720;
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, recordVideo: { dir: tmp, size: { width: W, height: H } } });
  const page = await ctx.newPage();
  const t0 = Date.now();
  await page.goto('file://' + path.join(tmp, 'p.html'));
  await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(800);
  const offset = (Date.now() - t0) / 1000;
  let total = await page.evaluate(() => window.__capture());
  if (process.env.MAXT) { total = Math.min(total, +process.env.MAXT); await page.waitForTimeout(total * 1000); }
  else await page.waitForFunction(() => window.__done === true, null, { timeout: (total + 60) * 1000, polling: 500 });
  await page.waitForTimeout(400);
  const vid = await page.video().path();
  const wall = (Date.now() - t0) / 1000;
  await ctx.close(); await browser.close();
  // the screencast's timeline can run slightly slower than the wall clock under load: rescale it to real time
  const vdur = parseFloat(execFileSync('ffprobe', ['-v', 'error', '-count_packets', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', vid]).toString()) / 25;
  const k = wall / vdur;
  console.log('wall', wall.toFixed(2), 'video', vdur.toFixed(2), 'scale', k.toFixed(4));
  execFileSync('ffmpeg', ['-y', '-i', vid, '-i', mp3, '-map', '0:v', '-map', '1:a',
    '-vf', `setpts=PTS*${k.toFixed(5)},trim=start=${offset.toFixed(3)},setpts=PTS-STARTPTS,fps=30,format=yuv420p`, '-t', total.toFixed(2), '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
    '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out], { stdio: 'inherit' });
  console.log('wrote', out, 'offset', offset, 'total', total);
})();
