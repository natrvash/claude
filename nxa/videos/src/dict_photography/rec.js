// Renders the dictionary entry frame by frame. Usage: node rec.js [avaSeconds]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const d = __dirname, avaDur = parseFloat(process.argv[2] || '4.2');
  const timings = JSON.parse(fs.readFileSync(d + '/timings.json'));
  fs.rmSync(d + '/frames', { recursive: true, force: true }); fs.mkdirSync(d + '/frames');
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + d + '/anim.html'); await p.evaluate(() => document.fonts.ready);
  const plan = await p.evaluate(([tm, a]) => setup(tm, a), [timings, avaDur]);
  fs.writeFileSync(d + '/plan.json', JSON.stringify(plan));
  const fps = 30, n = Math.round(plan.TOTAL * fps);
  for (let i = 0; i < n; i++) { await p.evaluate(t => render(t), i / fps); await p.screenshot({ path: `${d}/frames/f${String(i).padStart(4, '0')}.png` }); }
  await b.close(); console.log(JSON.stringify(plan), 'frames', n);
})();
