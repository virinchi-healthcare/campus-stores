import sys; sys.path.insert(0, sys.argv[1])
from cdp import *
import counter
b = Browser()
print("phase/tab now:", json.loads(b.saved())["phase"], json.loads(b.saved())["tab"])
b.click("Loan register")
print("== Loan register before issuing"); print(b.text("[data-page]")); b.shot("06-register-before-issue")
counter.reset()
plan = [("PR-04 · HDMI projector", "a"), ("SP-02 · Portable speaker", "b"), ("AD-12 · USB-C → HDMI adapter", "c")]
for unit, tag in plan:
    b.click("New issue slip")
    if tag == "a":
        print("\n== Issue form options")
        for n in ["req", "asset", "who", "due"]:
            print(n, b.js(f"[...{sel_named(n)}.options].map(o=>o.text)"))
        b.shot("07-issue-form-empty")
    b.choose(sel_named("req"), "RQ-214 · Film Society")
    b.choose(sel_named("asset"), unit)
    b.choose(sel_named("who"), "Kabir Sen")
    b.choose(sel_named("due"), "Fri 8 pm")
    if tag == "a": b.shot("08-issue-form-filled-PR-04")
    b.click("Save issue slip")
    print(f"\n== after saving {unit}: status =", b.status(), "| editing:", json.loads(b.saved())["editing"])
    print("   asset options next time would exclude it; counter so far", counter.COUNT)
    if tag == "c": b.shot("09-register-after-three-slips")
print("\n== Loan register after issue"); print(b.text("[data-page]"))
print("\nTOTAL input for 3 slips:", counter.COUNT)
b.click("All slips"); print("\n== All slips"); print(b.text("[data-page]")); b.click("Outstanding")
b.click("Inventory"); print("\n== Inventory after issue"); print(b.text("[data-page]")); b.shot("10-inventory-after-issue")
b.click("Desk book"); print("\n== Desk book phase 0"); print(b.text("[data-page]")); b.shot("11-deskbook-phase0")
print("\nsaved loans:", json.loads(b.saved())["loans"])
print("ERRORS:", b.errors())
