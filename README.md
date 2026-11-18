# Campus Stores

Campus Stores is a Product Engineer work sample set at a fictional campus media equipment desk. Work through a club’s screening, from equipment pickup to a partial return and the next morning’s handover. Open **Candidate brief** in the app for the assignment.

## Product decision

The full write-up (what I reviewed, what I changed, how I checked it, and what I left alone) is in [decision.md](decision.md).

**Keep:** The inventory and loan register show availability per physical unit. During pickup, that lets the desk issue the approved projector, speaker, and adapter separately and see which specific units remain out.

**Change:** At the Saturday handover, the desk book says Leela will return the screening adapter, but the loan register lists outstanding slips without connecting that arrival to the screening. A staff member has to find the matching request and unit before closing the right slip.

**Prototype:** Issue the screening kit on Friday (projector, speaker, one adapter), then advance to Saturday morning and open **Loan register**. The new **Return from Leela Das** panel matches the screening request and adapter type to the outstanding physical unit, shows its slip number, and offers a return action for that slip. The regular loan list remains available as a fallback. This is a proposed change in the fictional exercise, not a result validated at a real counter.

**What I would keep:** The physical-unit records and the ability to handle a partial return without closing the other items.

**Counter observation:** In a short test with desk staff handling real or representative partial returns, observe whether each arriving item is matched to the correct open slip. Record correct matches, wrong-slip selections or corrections, and time from item arrival to a correctly updated record. Compare the current flow with the prototype on comparable returns; do not infer an improvement from the prototype alone.

## Run the app

Open `index.html` in a modern browser. The app includes its scripts, styles, and icons and can run offline.

To serve it over local HTTP, run this from the repository folder and visit `http://localhost:8000`.

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Each browser stores its own sample shift locally when browser storage is available. **Restart sample shift** restores the fictional starting records.

## Source

- `index.html` contains the desk layout, candidate brief, and bundled icons.
- `app.js` contains the sample records and interactions.
- `styles.css` defines the desktop and mobile layouts.
- `decision.md` records the product decision, changes, checks and known gaps.

Icon license notices are in [third-party/lucide-LICENSE.txt](third-party/lucide-LICENSE.txt). Notices for the AI skills in `.claude/skills/` are in [third-party/skills-LICENSE.md](third-party/skills-LICENSE.md).


## Submit your work

1. [Fork Campus Stores](https://github.com/virinchi-healthcare/campus-stores/fork) into your GitHub account. Review and adapt the prototype and decision above, then push your changes to your public fork. Update this README to point reviewers to your work and explain your final decision.
2. In your fork, open **Commits**, select the final commit you want reviewed, and copy the page URL. It should look like `https://github.com/YOUR-USERNAME/campus-stores/commit/COMMIT-SHA`.
3. [Submit your work through the Google Form](https://docs.google.com/forms/d/e/1FAIpQLScvzoh1R4WS-SkiwAVBQbMvniieJYSoOEfLMyVo5CyjOvYUgQ/viewform). Your **roll number**, **email ID**, and **final commit link from your public fork** are required. Enter your roll number and email ID in the form only.
