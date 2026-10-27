const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
const dir=path.join(__dirname,'pages');const only=process.argv[2];
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.svg')&&(!only||f.startsWith(only)))){
 const svg=fs.readFileSync(path.join(dir,f),'utf8');
 await p.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;700&family=Fraunces:wght@600&family=Inter&family=Playfair+Display:ital@1&family=Space+Grotesk&family=Unbounded:wght@700&family=Vazirmatn:wght@700&family=IBM+Plex+Sans+Arabic:wght@700&display=block" rel="stylesheet"><style>body{margin:0}</style></head><body>${svg}</body></html>`,{waitUntil:'networkidle'});
 await p.evaluate(()=>document.fonts.ready);
 await p.screenshot({path:path.join(__dirname,'previews',f.replace('.svg','.png'))});}
await b.close();})();
