const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const d = __dirname; fs.rmSync(d + '/frames', { recursive: true, force: true }); fs.mkdirSync(d + '/frames');
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + d + '/anim.html'); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => render(4.5)); await p.waitForTimeout(400);
  const total = await p.evaluate(() => TOTAL), fps = 30, n = Math.round(total * fps);
  for (let i = 0; i < n; i++) { await p.evaluate(t => render(t), i / fps); await p.screenshot({ path: `${d}/frames/f${String(i).padStart(4, '0')}.png` }); }
  
  await b.close();
})();
