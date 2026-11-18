# Validation harness

These are the scripts that produced the evidence in [BASELINE_TESTING.md](../BASELINE_TESTING.md) and [VALIDATION.md](../VALIDATION.md). They use only the Python 3 standard library and drive an installed Google Chrome over the DevTools protocol.

- **Interaction:** real mouse clicks and keypresses only.
- **JavaScript:** read-only. It is used to locate elements, read text, read `localStorage` and measure layout. It never writes app state.

| File | Purpose |
|---|---|
| `cdp.py` | Minimal DevTools client: WebSocket, input events, screenshots, read-only queries |
| `counter.py` | Counts the clicks and keypresses sent (used for the effort measures) |
| `v_main.py` | The baseline shift repeated, plus acceptance criteria AC1–AC8 and AC10–AC12, AC14 |
| `v_reg.py` | Regression N1–N7, P1–P4, AC9 (V1 variant), keyboard K1, old-save compatibility O1 |
| `v_layout.py` | AC13: desktop and mobile (390 px), light and dark, contrast and overflow checks |
| `v_extra.py` | Request content, P3, blank handover note |
| `baseline/` | The scripts used for the original baseline run, kept for reference |
| `results/` | Raw pass/fail output from the validation run (64 checks) |

## Run

```sh
# 1. serve the repo
python -m http.server 5500 --bind 127.0.0.1
# 2. start Chrome with a throwaway profile
"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --remote-debugging-port=9333 --user-data-dir=<temp dir> about:blank
# 3. from this folder
SHOTS=../screenshots/after python v_main.py .
```

`v_reg.py` test O1 also needs the original app on the same origin. Copy `git show HEAD~N:{index.html,app.js,styles.css}` from the pre-change commit into `<repo>/.baseline-tmp/` before running it, and delete that folder afterwards.
