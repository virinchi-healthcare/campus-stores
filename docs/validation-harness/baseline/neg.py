import sys; sys.path.insert(0, sys.argv[1])
from cdp import *
b = Browser()
b.call("Network.enable")
def loans(): return [(l["num"], l["req"], l["asset"], l["who"], l["due"], l["back"]) for l in json.loads(b.saved())["loans"]]
def asset_opts(): return b.js(f"[...{sel_named('asset')}.options].map(o=>o.text)")
def fill(req, asset, who, due):
    b.choose(sel_named("req"), req); b.choose(sel_named("asset"), asset); b.choose(sel_named("who"), who); b.choose(sel_named("due"), due)
def restart():
    b.click("Restart sample shift"); assert json.loads(b.saved())["loans"] == [{"num":401,"req":"RQ-209","asset":"MI-09","who":"Tara Shah","due":"Sat 10 am","back":False}]

print("##### N1 unit already on loan (MI-09 at start; PR-04 after issuing)")
b.reload(); restart(); b.click("Loan register"); b.click("New issue slip")
o = asset_opts(); print("asset options:", o); print("MI-09 offered?", any("MI-09" in x for x in o))
fill("RQ-214 · Film Society", "PR-04 · HDMI projector", "Kabir Sen", "Fri 8 pm"); b.click("Save issue slip"); print("status:", b.status())
b.click("New issue slip"); o = asset_opts(); print("PR-04 offered after issue?", any("PR-04" in x for x in o), o)
b.choose(sel_named("req"), "RQ-209 · Debate Union")
print("asset options with RQ-209 selected (unchanged by request?):", asset_opts()); b.shot("N1-on-loan-units-not-offered")
print("loans:", loans())

print("\n##### N2 unit in repair (PR-06)")
restart(); b.click("Loan register"); b.click("New issue slip")
o = asset_opts(); print("PR-06 offered?", any("PR-06" in x for x in o))
b.click("Inventory"); b.choose("document.querySelector('[data-filter]')", "In repair"); print(b.text("[data-page]")); b.shot("N2-inventory-in-repair")
b.choose("document.querySelector('[data-filter]')", "All items")

print("\n##### N3 type not in approved request")
restart(); b.click("Loan register"); b.click("New issue slip")
fill("RQ-214 · Film Society", "CA-03 · Digital camera", "Kabir Sen", "Fri 8 pm"); b.click("Save issue slip")
print("status:", b.status()); print("form still open?", json.loads(b.saved())["editing"], "| selections kept:", b.js(f"[{sel_named('req')}.value,{sel_named('asset')}.value]"))
print("loans:", loans()); b.shot("N3-type-not-approved-RQ214-camera")
b.choose(sel_named("req"), "RQ-217 · Photo Circle"); b.choose(sel_named("asset"), "PR-04 · HDMI projector"); b.click("Save issue slip")
print("RQ-217 + PR-04 status:", b.status(), "| loans:", len(loans()))
b.choose(sel_named("asset"), "CA-03 · Digital camera"); b.choose(sel_named("who"), "Dev Menon"); b.choose(sel_named("due"), "Sat noon")
print("before valid save, status still shows:", b.status())
b.click("Save issue slip"); print("RQ-217 + CA-03 (valid) status:", b.status(), "| loans:", loans()[-1])

print("\n##### N4 second unit of same type on same request")
restart(); b.click("Loan register"); b.click("New issue slip")
fill("RQ-214 · Film Society", "AD-12 · USB-C → HDMI adapter", "Kabir Sen", "Fri 8 pm"); b.click("Save issue slip"); print("AD-12:", b.status())
b.click("New issue slip"); fill("RQ-214 · Film Society", "AD-15 · USB-C → HDMI adapter", "Kabir Sen", "Fri 8 pm"); b.click("Save issue slip")
print("AD-15 same request status:", b.status(), "| loans:", len(loans())); b.shot("N4-second-adapter-blocked")
b.choose(sel_named("req"), "RQ-214 · Film Society"); b.choose(sel_named("asset"), "SP-02 · Portable speaker"); b.click("Save issue slip")
b.click("New issue slip"); fill("RQ-214 · Film Society", "SP-05 · Portable speaker", "Kabir Sen", "Fri 8 pm"); b.click("Save issue slip")
print("SP-05 after SP-02 status:", b.status(), "| loans:", len(loans()))
b.click("Cancel"); b.click_in_row("L-402 · AD-12", "Record return"); print("returned AD-12:", b.status())
b.click("New issue slip"); fill("RQ-214 · Film Society", "AD-15 · USB-C → HDMI adapter", "Kabir Sen", "Fri 8 pm"); b.click("Save issue slip")
print("AD-15 after AD-12 returned:", b.status(), "| last loan:", loans()[-1])

print("\n##### N5 other form rules: empty submit, wrong person, return-by beyond request")
restart(); b.click("Loan register"); b.click("New issue slip")
b.click("Save issue slip"); print("empty submit -> loans:", len(loans()), "| form valid?", b.js("document.querySelector('[data-issue]').checkValidity()"), "| status:", b.status())
fill("RQ-214 · Film Society", "PR-04 · HDMI projector", "Dev Menon", "Sat noon"); b.click("Save issue slip")
print("RQ-214 to Dev Menon due Sat noon (request return-by Fri 8 pm):", b.status(), loans()[-1]); b.shot("N5-due-date-and-person-not-checked")

print("\n##### N6 leaving the form mid-issue")
restart(); b.click("Loan register"); b.click("New issue slip")
b.choose(sel_named("req"), "RQ-214 · Film Society"); b.choose(sel_named("who"), "Kabir Sen")
b.click("Requests"); b.click("Loan register")
print("form open after returning to register?", json.loads(b.saved())["editing"], "| page shows:", b.text("[data-page]").splitlines()[:4])

print("\n##### N7 Record return has no confirmation / undo")
restart(); b.click("Loan register")
b.click_in_row("L-401 · MI-09", "Record return"); print("status:", b.status()); print(b.text("[data-page]"))
b.shot("N7-empty-outstanding-after-one-click-return")
b.click("All slips"); print(b.text("[data-page]")); print("any undo/reopen control?", "Undo" in b.text() or "Reopen" in b.text())

print("\n##### 404s seen")
for e in b.events:
    if e.get("method") == "Network.responseReceived" and e["params"]["response"]["status"] >= 400:
        print(e["params"]["response"]["status"], e["params"]["response"]["url"])
print("ERRORS:", b.errors())
