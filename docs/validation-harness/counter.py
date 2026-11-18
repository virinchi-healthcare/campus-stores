from cdp import Browser
_orig_call = Browser.call
COUNT = {"clicks": 0, "keys": 0, "typed": 0}
def call(self, method, params=None):
    if method == "Input.dispatchMouseEvent" and params and params.get("type") == "mousePressed": COUNT["clicks"] += 1
    if method == "Input.dispatchKeyEvent" and params and params.get("type") == "keyDown": COUNT["keys"] += 1
    if method == "Input.insertText": COUNT["typed"] += 1
    return _orig_call(self, method, params)
Browser.call = call
def reset():
    for k in COUNT: COUNT[k] = 0
