const {chromium}=require('playwright-core');
(async()=>{const b=await chromium.launch({executablePath:process.env.HOME+'/.cache/ms-playwright/chromium-1254/chrome-linux64/chrome',args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1300,height:900}});
await p.goto('file://'+process.argv[2],{waitUntil:'load'});await p.waitForTimeout(7000);
const bb=await (await p.$('#viewer')).boundingBox();const clip={x:bb.x,y:bb.y,width:bb.width,height:bb.height};
for(const v of ['bte','v3','ric']){
  await p.evaluate(v=>{document.querySelector('#variant button[data-v="'+v+'"]').click();},v);await p.waitForTimeout(1200);
  await p.evaluate(()=>{for(const [i,val] of [['t-cut',false],['t-labels',false]]){const e=document.getElementById(i);if(e&&e.checked!==val)e.click();}});
  for(const c of ['out','front','wide','below']){
    await p.evaluate(c=>window.havenCam(c),c);await p.waitForTimeout(1800);
    await p.screenshot({path:process.argv[3]+'/'+v+'_'+c+'.png',clip});
  }
  console.log(v,'done');
}
await b.close();})();
