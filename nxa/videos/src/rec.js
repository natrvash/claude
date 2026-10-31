const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const fps = 30, total = 5.5, n = Math.round(total * fps);
  fs.mkdirSync(__dirname + '/frames', { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + __dirname + '/anim.html'); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => { render(3.8); }); await p.waitForTimeout(400);
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => render(t), i / fps);
    await p.screenshot({ path: `${__dirname}/frames/f${String(i).padStart(4, '0')}.png` });
  }
  await b.close(); console.log('frames', n);
})();
