import sys; sys.path.insert(0, sys.argv[1])
from cdp import *
R = []
def check(i, ok, detail=""):
    R.append((i, "PASS" if ok else "FAIL", detail)); print(("PASS " if ok else "FAIL ") + i, "|", detail)
b = Browser()
def st(): return json.loads(b.saved())
def fill(req, asset, who, due):
    for n, v in (("req", req), ("asset", asset), ("who", who), ("due", due)): b.choose(sel_named(n), v)
CONTRAST = """(() => {
  const lum = c => { const m = c.match(/[\\d.]+/g).slice(0,3).map(Number).map(v => { v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055, 2.4)}); return 0.2126*m[0]+0.7152*m[1]+0.0722*m[2]; };
  const ratio = (a,b) => { const [x,y] = [lum(a), lum(b)].sort((p,q)=>q-p); return Math.round((x+0.05)/(y+0.05)*100)/100; };
  const out = {};
  for (const [name, sel] of [["Overdue tag",".tag.warn"],["Not issued tag",".tag.memo"],["Back tag",".tag.muted"],["Back row label",".row.done strong"],["Row sub text",".kit .row small"],["Kit summary",".kithead .acts small"]]) {
    const el = document.querySelector('#campus-stores ' + sel); if (!el) continue;
    let bg = getComputedStyle(el).backgroundColor, p = el;
    while (bg === 'rgba(0, 0, 0, 0)' && p.parentElement) { p = p.parentElement; bg = getComputedStyle(p).backgroundColor; }
    out[name] = ratio(getComputedStyle(el).color, bg);
  }
  return out; })()"""
def overflow(): return b.js("[document.documentElement.scrollWidth, innerWidth]")
def setup_morning():
    b.click("Restart sample shift"); b.click("Loan register")
    for u in ["PR-04 · HDMI projector", "SP-02 · Portable speaker"]:
        b.click("New issue slip"); fill("RQ-214 · Film Society", u, "Kabir Sen", "Fri 8 pm"); b.click("Save issue slip")
b.goto("http://localhost:5500/")
for scheme in ["dark", "light"]:
    b.viewport(1280, 900, False, scheme)
    setup_morning()   # 2 of 3 issued -> Not issued row visible
    b.shot(f"L-desktop-{scheme}-pickup-not-issued"); c0 = b.js(CONTRAST)
    b.click("New issue slip"); fill("RQ-214 · Film Society", "AD-12 · USB-C → HDMI adapter", "Kabir Sen", "Fri 8 pm"); b.click("Save issue slip")
    b.click("Move to return time"); b.click_in_row("HDMI projector", "Record return"); b.click_in_row("Portable speaker", "Record return")
    b.click("Move to next morning"); b.click("Loan register")
    b.shot(f"L-desktop-{scheme}-morning")
    c = {**c0, **b.js(CONTRAST)}; w = overflow()
    check(f"L-desktop-{scheme} contrast >= 4.5 and no horizontal scroll", min(c.values()) >= 4.5 and w[0] <= w[1], f"{c}; scrollWidth/innerWidth={w}")
    b.click("Restart sample shift")
for scheme in ["dark", "light"]:
    b.viewport(390, 844, True, scheme)
    b.call("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 1})
    b.reload()
    setup_morning()
    b.shot(f"L-mobile-{scheme}-pickup-not-issued"); c0 = b.js(CONTRAST)
    b.click("New issue slip")
    fill("RQ-214 · Film Society", "AD-12 · USB-C → HDMI adapter", "Kabir Sen", "Fri 8 pm")
    form_cols = b.js("getComputedStyle(document.querySelector('#campus-stores .form')).gridTemplateColumns")
    b.shot(f"L-mobile-{scheme}-issue-form")
    b.click("Save issue slip"); issued = b.status()
    b.click("Move to return time"); b.click_in_row("HDMI projector", "Record return"); b.click_in_row("Portable speaker", "Record return")
    b.click("Move to next morning"); b.click("Loan register")
    b.shot(f"L-mobile-{scheme}-morning")
    w = overflow(); c = {**c0, **b.js(CONTRAST)}
    cols = b.js("getComputedStyle(document.querySelector('#campus-stores .kit .row')).gridTemplateColumns")
    btn_h = b.js("Math.round([...document.querySelectorAll('#campus-stores .kit button')][0].getBoundingClientRect().height)")
    coarse = b.js("matchMedia('(pointer: coarse)').matches")
    nav_dir = b.js("getComputedStyle(document.querySelector('#campus-stores nav')).flexDirection")
    b.click_in_row("USB-C → HDMI adapter", "Record return"); closed = st()["loans"][3]["back"]
    check(f"L-mobile-{scheme} layout and controls", w[0] <= w[1] and " " not in cols.strip() and closed and issued.startswith("Issued AD-12") and min(c.values()) >= 4.5,
          f"scrollWidth/innerWidth={w}; kit row columns='{cols}'; issue form columns='{form_cols}'; nav={nav_dir}; pointer:coarse={coarse}; Record return height={btn_h}px; contrast={c}")
    b.call("Emulation.setTouchEmulationEnabled", {"enabled": False})
    b.click("Restart sample shift")
b.viewport(1280, 900, False, "dark")
print("ERRORS:", [e for e in b.errors() if not e.startswith("LOG Failed to load resource")])
json.dump(R, open(sys.argv[1] + "/r_layout.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
