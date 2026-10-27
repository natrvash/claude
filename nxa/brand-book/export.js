// Export the brand book and logo pack: JPG pages, full PDF, Illustrator (.ai), and logo PNG/JPG/PDF.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const FONTS='<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;700&family=Fraunces:wght@600&family=Inter&family=Playfair+Display:ital@1&family=Space+Grotesk&family=Unbounded:wght@700&family=Vazirmatn:wght@700&family=IBM+Plex+Sans+Arabic:wght@700&display=block" rel="stylesheet">';
const ex=path.join(__dirname,'exports');
(async()=>{const b=await chromium.launch();
 const pages=fs.readdirSync(path.join(__dirname,'pages')).filter(f=>f.endsWith('.svg')).sort();
 fs.mkdirSync(path.join(ex,'jpg'),{recursive:true});
 const p=await b.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:2});
 for(const f of pages){await p.setContent(`<html><head>${FONTS}<style>body{margin:0}</style></head><body>${fs.readFileSync(path.join(__dirname,'pages',f),'utf8')}</body></html>`,{waitUntil:'networkidle'});
  await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:path.join(ex,'jpg',f.replace('.svg','.jpg')),type:'jpeg',quality:92});}
 const all=pages.map(f=>fs.readFileSync(path.join(__dirname,'pages',f),'utf8')).join('');
 const d=await b.newPage();await d.setContent(`<html><head>${FONTS}<style>@page{size:1920px 1080px;margin:0}body{margin:0}svg{display:block;page-break-after:always}</style></head><body>${all}</body></html>`,{waitUntil:'networkidle'});
 await d.evaluate(()=>document.fonts.ready);
 await d.pdf({path:path.join(ex,'NxA-Brand-Identity-Book.pdf'),width:'1920px',height:'1080px',printBackground:true});
 fs.copyFileSync(path.join(ex,'NxA-Brand-Identity-Book.pdf'),path.join(ex,'NxA-Brand-Identity-Book.ai'));
 // logo pack
 const lp=path.join(ex,'logo-pack');for(const k of ['png','jpg','pdf'])fs.mkdirSync(path.join(lp,k),{recursive:true});
 for(const f of fs.readdirSync(path.join(lp,'svg')).sort()){const svg=fs.readFileSync(path.join(lp,'svg',f),'utf8');
  const w=+svg.match(/width="(\d+)"/)[1],h=+svg.match(/height="(\d+)"/)[1];const base=f.replace('.svg','');
  const q=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:Math.max(1,3000/w)});
  await q.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
  await q.screenshot({path:path.join(lp,'png',base+'.png'),omitBackground:true});
  await q.setContent(`<html><body style="margin:0;background:#F6F2EC">${svg}</body></html>`);
  await q.screenshot({path:path.join(lp,'jpg',base+'.jpg'),type:'jpeg',quality:95});
  await q.pdf({path:path.join(lp,'pdf',base+'.pdf'),width:w+'px',height:h+'px',printBackground:true,pageRanges:'1'});
  await q.close();}
 await b.close();})();
