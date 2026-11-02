// Renders one entry frame by frame. Usage: node rec.js <id>
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const d = __dirname, id = process.argv[2], W = `${d}/work/${id}`;
  const entry = JSON.parse(fs.readFileSync(d + '/entries.json')).entries.find(e => e.id === id);
  const j = f => JSON.parse(fs.readFileSync(`${W}/${f}`));
  fs.rmSync(W + '/frames', { recursive: true, force: true }); fs.mkdirSync(W + '/frames');
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + d + '/anim.html');
  // load every face before measuring line breaks (empty elements don't trigger font loading)
  await p.evaluate(() => Promise.all(['200 132px Manrope', '400 44px Manrope', '700 54px Manrope', '66px Hand'].map(f => document.fonts.load(f))));
  const pl = j('plan.json'); pl.yesbut = process.env.YESBUT === '1';
  const plan = await p.evaluate(a => setup(...a), [entry, j('timings.json'), pl, j('envelope.json')]);
  const fps = 30, n = Math.round(plan.TOTAL * fps);
  for (let i = 0; i < n; i++) { await p.evaluate(t => render(t), i / fps); await p.screenshot({ path: `${W}/frames/f${String(i).padStart(4, '0')}.png` }); }
  await b.close(); console.log(id, 'frames', n);
})();
