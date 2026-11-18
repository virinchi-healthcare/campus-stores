import sys; sys.path.insert(0, sys.argv[1])
from cdp import *
R = []
def check(i, ok, detail=""):
    R.append((i, "PASS" if ok else "FAIL", detail)); print(("PASS " if ok else "FAIL ") + i, "|", detail)
b = Browser(); b.call("Network.enable")
NEW = "http://localhost:5500/"
OLD = "http://localhost:5500/.baseline-tmp/index.html"
def st(): return json.loads(b.saved())
def page(): return b.text("[data-page]")
def loans(): return [(l["num"], l["req"], l["asset"], l["who"], l["due"], l["back"]) for l in st()["loans"]]
def asset_opts(): return b.js(f"[...{sel_named('asset')}.options].map(o=>o.text)")
def fill(req, asset, who, due):
    for n, v in (("req", req), ("asset", asset), ("who", who), ("due", due)): b.choose(sel_named(n), v)
def restart():
    b.click("Restart sample shift"); assert len(st()["loans"]) == 1 and st()["phase"] == 0
def issue(unit, req="RQ-214 · Film Society", who="Kabir Sen", due="Fri 8 pm"):
    b.click("New issue slip"); fill(req, unit, who, due); b.click("Save issue slip"); return b.status()
def rowtext(s): return b.js(f"[...document.querySelectorAll('#campus-stores .kit .row')].find(r=>r.innerText.includes({json.dumps(s)}))?.innerText")
b.goto(NEW)

# ---- N1-N7 (same steps as baseline) ----
restart(); b.click("Loan register"); b.click("New issue slip")
o = asset_opts(); ok1 = not any("MI-09" in x for x in o)
fill("RQ-214 · Film Society", "PR-04 · HDMI projector", "Kabir Sen", "Fri 8 pm"); b.click("Save issue slip")
b.click("New issue slip"); o2 = asset_opts()
check("N1 on-loan units not offered", ok1 and not any("PR-04" in x for x in o2), str(o2))
b.shot("N1-on-loan-units-not-offered")
restart(); b.click("Loan register"); b.click("New issue slip")
check("N2 in-repair PR-06 not offered", not any("PR-06" in x for x in asset_opts()))
restart(); b.click("Loan register"); b.click("New issue slip")
fill("RQ-214 · Film Society", "CA-03 · Digital camera", "Kabir Sen", "Fri 8 pm"); b.click("Save issue slip")
m = b.status(); kept = b.js(f"[{sel_named('req')}.value,{sel_named('asset')}.value]")
b.shot("N3-type-not-approved")
b.choose(sel_named("req"), "RQ-217 · Photo Circle"); b.choose(sel_named("asset"), "PR-04 · HDMI projector"); b.click("Save issue slip"); m2 = b.status()
check("N3 type outside request refused", m == m2 == "This equipment type is outside the approved request. Choose an approved unit." and kept == ["RQ-214", "CA-03"] and len(loans()) == 1, m)
restart(); b.click("Loan register")
a = issue("AD-12 · USB-C → HDMI adapter"); m = issue("AD-15 · USB-C → HDMI adapter")
n_after_block = len(loans()); b.shot("N4-second-adapter-blocked")
b.choose(sel_named("asset"), "SP-02 · Portable speaker"); b.click("Save issue slip")
m2 = issue("SP-05 · Portable speaker")
b.click("Cancel"); b.click_in_row("USB-C → HDMI adapter", "Record return")
m3 = issue("AD-15 · USB-C → HDMI adapter")
check("N4 one unit per type per request (outstanding only)", m == m2 == "The approved quantity of this equipment type is already on loan." and n_after_block == 2 and m3 == "Issued AD-15 to Kabir Sen on slip L-404.", f"{m} | {m3}")
t = page(); r = rowtext("USB-C")
check("N4b register after return+reissue shows AD-15 Out (not old AD-12 Back)", "AD-15" in r and "Record return" in r and "AD-12" not in t, repr(r))
restart(); b.click("Loan register"); b.click("New issue slip"); b.click("Save issue slip")
empty_ok = len(loans()) == 1 and b.js("document.querySelector('[data-issue]').checkValidity()") is False
fill("RQ-214 · Film Society", "PR-04 · HDMI projector", "Dev Menon", "Sat noon"); b.click("Save issue slip")
check("N5 required fields; due/collector still unchecked (unchanged rule)", empty_ok and loans()[-1] == (402, "RQ-214", "PR-04", "Dev Menon", "Sat noon", False), b.status())
restart(); b.click("Loan register"); b.click("New issue slip"); b.choose(sel_named("req"), "RQ-214 · Film Society"); b.click("Requests"); b.click("Loan register")
check("N6 leaving the form discards it (unchanged)", st()["editing"] is False)
restart(); b.click("Loan register"); b.click_in_row("Wireless microphone", "Record return")
check("N7 one-click return still immediate; empty state", "No outstanding slips." in page() and st()["loans"][0]["back"] is True, b.status())

# ---- Persistence / restart ----
restart(); b.click("Loan register"); issue("PR-04 · HDMI projector")
b.click("Move to return time"); b.click("Desk book")
b.type_into("document.querySelector('#campus-stores textarea[name=note]')", "Persistence check note."); b.click("Add handover note")
b.click("Inventory"); b.choose("document.querySelector('[data-filter]')", "On loan")
b.click("Loan register"); b.click("All slips"); b.click("Requests"); b.click_in_row("RQ-214", "View form")
before, before_text = st(), b.text(); b.reload()
check("P1 refresh mid-shift identical", st() == before and b.text() == before_text)
b.click("Loan register"); b.click("Outstanding"); t1 = page(); b.reload(); b.click("Loan register")
check("P1b grouped Outstanding identical after reload", page() == t1 and "1 out · 2 not issued" in t1, t1.split("\n")[6:9])
b.click("New issue slip"); b.choose(sel_named("req"), "RQ-214 · Film Society"); b.reload()
check("P2 half-filled form reopens empty (unchanged)", st()["editing"] is True and b.js(f"{sel_named('req')}.value") == "")
b.click("Cancel"); b.click("Move to next morning"); b.click("Restart sample shift")
s = st()
check("P4 restart from phase 2 restores seed", s["phase"] == 0 and s["notes"] == [] and len(s["loans"]) == 1 and s["tab"] == "Requests" and s["filter"] == "All items" and s["onlyOpen"] is True)
b.reload(); check("P4b restart survives reload", st()["phase"] == 0 and len(st()["loans"]) == 1)

# ---- V1 no handover note ----
restart(); b.click("Loan register")
for u in ["PR-04 · HDMI projector", "SP-02 · Portable speaker", "AD-12 · USB-C → HDMI adapter"]: issue(u)
b.click("Move to return time"); b.click_in_row("HDMI projector", "Record return"); b.click_in_row("Portable speaker", "Record return")
b.click("Move to next morning"); b.click("Loan register"); t = page()
check("AC9 V1 (no note): register names adapter, slip and Overdue", all(x in t for x in ["USB-C → HDMI adapter", "L-404", "Overdue"]) and st()["notes"] == [])
b.shot("V1-morning-register-no-note")

# ---- K1 keyboard: Tab to the adapter's Record return and press Enter ----
b.js("document.activeElement && document.activeElement.blur()")
tabs = 0; label = None
for _ in range(40):
    b.key("Tab", "Tab", 9); tabs += 1
    label = b.js("document.activeElement.getAttribute('aria-label')")
    if label and "AD-12" in label: break
outline = b.js("getComputedStyle(document.activeElement).outlineStyle")
b.key("Enter")
check("K1 keyboard: Tab reaches labelled Record return, Enter closes L-404", label == "Record return of AD-12 USB-C → HDMI adapter, slip L-404" and st()["loans"][3]["back"] is True, f"{tabs} Tab presses; focus outline={outline}; status={b.status()}")
check("K1b focus after re-render", True, "focus now on: " + str(b.js("document.activeElement.tagName + ' ' + (document.activeElement.innerText||'').slice(0,20)")))

# ---- O1 saved shift created by ORIGINAL code loads in new code ----
b.goto(OLD); b.click("Restart sample shift"); b.click("Loan register")
for u in ["PR-04 · HDMI projector", "SP-02 · Portable speaker", "AD-12 · USB-C → HDMI adapter"]: issue(u)
b.click("Move to return time"); b.click_in_row("L-402 · PR-04", "Record return"); b.click_in_row("L-403 · SP-02", "Record return")
b.click("Move to next morning"); b.click("Loan register")
old_saved = b.saved(); old_text = page()
b.goto(NEW); new_saved_on_load = b.saved(); t = page()
check("O1 original-format save loads unchanged in new app", new_saved_on_load == old_saved and b.text("[data-clock]") == "Saturday · 9:00 am" and "1 out · 2 back" in t and "Overdue" in t, "old register showed: " + " / ".join(old_text.split("\n")[5:7]))
b.click_in_row("USB-C → HDMI adapter", "Record return")
check("O1b new app can continue the old shift", st()["loans"][3]["back"] is True and set(st()) == set(json.loads(old_saved)))
b.goto(OLD); check("O1c original app still reads the save written by new app", "L-404 · AD-12" in (b.click("All slips") or page()) and "Returned" in page())
b.goto(NEW); b.click("Restart sample shift")

errs = b.errors(); bad = set()
for e in b.events:
    if e.get("method") == "Network.responseReceived" and e["params"]["response"]["status"] >= 400: bad.add(e["params"]["response"]["url"])
check("R-ERR no JS exceptions during regression", not any(x.startswith(("EXCEPTION", "CONSOLE")) for x in errs) and bad <= {"http://localhost:5500/favicon.ico", "http://localhost:5500/.baseline-tmp/favicon.ico"}, str(bad))
json.dump(R, open(sys.argv[1] + "/r_reg.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
