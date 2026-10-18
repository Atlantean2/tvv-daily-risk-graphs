import os,re,html,io,datetime
from PIL import Image
import sys;sys.path.insert(0,'/workspace/risk-watcher');from tvv_nav import nav,NAV_CSS
SRC_CSS=open('/workspace/risk-watcher/site/build.py').read().split('CSS="""')[1].split('"""')[0]
CSS=SRC_CSS+"""
figure.g{margin:0 0 28px;padding:0}figure.g figcaption{font-size:15px;margin:4px 6px}figure.g .t{font-weight:700}
figure.g .s{font-size:14px;word-break:break-all}ul.src li{margin:4px 0;word-break:break-all}"""
E=lambda s:html.escape(str(s),quote=True)
def save_img(data_or_path,out):
    im=Image.open(data_or_path if isinstance(data_or_path,str) else io.BytesIO(data_or_path))
    if im.mode in("P","LA","RGBA"):
        im=im.convert("RGBA");bg=Image.new("RGB",im.size,"white");bg.paste(im,mask=im.split()[-1]);im=bg
    im=im.convert("RGB")
    if im.width>1600: im=im.resize((1600,round(im.height*1600/im.width)),Image.LANCZOS)
    im.save(out,"WEBP",quality=86,method=6)
def figure(src,title,caption,urls):
    links=" ".join(f'<a href="{E(u)}" target="_blank" rel="noopener">{E(u)}</a>' for u in urls if u.startswith("https://"))
    t=f'<span class="t">{E(title)}.</span> ' if title else ''
    return f'<figure class="g"><img src="{E(src)}" alt="{E(title or caption)}" loading="lazy"><figcaption>{t}{E(caption)}<br><span class="s">Source: {links}</span></figcaption></figure>'
def page(T,key,body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{T} — {key}</title><link rel="stylesheet" href="../assets/style.css"><script>if(!/[?&]raw/.test(location.search))location.replace("../index.html#{key}")</script></head><body><main id="issue">{body}</main></body></html>'''
JS="""const tabs=[...document.querySelectorAll('#tabs button')],m=document.getElementById('content'),ds=tabs.map(t=>t.dataset.d);
async function show(d){if(!ds.includes(d))d=ds[0];tabs.forEach(t=>t.setAttribute('aria-selected',t.dataset.d==d));
document.querySelector(`#tabs [data-d="${d}"]`).scrollIntoView({inline:'nearest',block:'nearest'});
m.innerHTML='<p>Loading…</p>';try{const r=await fetch('issues/'+d+'.html',{cache:'no-cache'});const doc=new DOMParser().parseFromString(await r.text(),'text/html');
const c=doc.querySelector('#issue');c.querySelectorAll('img').forEach(i=>i.setAttribute('src','issues/'+i.getAttribute('src')));
c.querySelectorAll('a[href]').forEach(a=>{const h=a.getAttribute('href');if(!/^(https?:|#)/.test(h))a.setAttribute('href','issues/'+h);if(/^http/.test(h)){a.target='_blank';a.rel='noopener'}});m.innerHTML=c.innerHTML;document.title=TT+' — '+(tabs.find(t=>t.dataset.d==d).textContent);window.scrollTo(0,0)}
catch(e){m.innerHTML='<p>Could not load '+d+'.</p>'}}
const TT=document.title;tabs.forEach(t=>t.onclick=()=>{location.hash=t.dataset.d});
addEventListener('hashchange',()=>show(location.hash.slice(1)));show(location.hash.slice(1));"""
def index(T,tabs,label="Tabs",cur=None):
    b="".join(f'<button role="tab" data-d="{E(k)}" aria-selected="false">{E(v)}</button>' for k,v in tabs)
    open("assets/style.css","w").write(CSS+NAV_CSS); open(".nojekyll","w").write("")
    open("index.html","w").write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{T}</title><link rel="stylesheet" href="assets/style.css"></head><body>{nav(cur)}<div id="top"><header><img src="assets/logo.png" alt="TVV logo"><h1>{T}</h1></header><nav id="tabs" role="tablist" aria-label="{label}">{b}</nav></div><main id="content"></main><script>{JS}</script></body></html>''')
