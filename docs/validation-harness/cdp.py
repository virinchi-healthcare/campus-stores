"""Minimal stdlib Chrome DevTools Protocol driver.

Interaction is done only with synthesized user input (mouse clicks, key presses,
typed text). JavaScript evaluation is used read-only: to locate elements, read
visible text, and read (never write) localStorage.
"""
import base64, json, os, socket, struct, sys, time, urllib.request

PORT = 9333
SHOTS = os.environ.get("SHOTS", ".")


class WS:
    def __init__(self, url):
        assert url.startswith("ws://")
        hostport, path = url[5:].split("/", 1)
        host, port = hostport.split(":")
        self.s = socket.create_connection((host, int(port)), timeout=30)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\n"
               f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
        self.s.sendall(req.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.s.recv(4096)
        head, self.rest = buf.split(b"\r\n\r\n", 1)
        assert b" 101 " in head.split(b"\r\n")[0], head

    def _read(self, n):
        while len(self.rest) < n:
            chunk = self.s.recv(1 << 20)
            if not chunk:
                raise ConnectionError("closed")
            self.rest += chunk
        out, self.rest = self.rest[:n], self.rest[n:]
        return out

    def send(self, text):
        data = text.encode()
        hdr = bytearray([0x81])
        n = len(data)
        if n < 126:
            hdr.append(0x80 | n)
        elif n < 65536:
            hdr.append(0x80 | 126); hdr += struct.pack(">H", n)
        else:
            hdr.append(0x80 | 127); hdr += struct.pack(">Q", n)
        mask = os.urandom(4)
        hdr += mask
        self.s.sendall(bytes(hdr) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def recv(self):
        msg = b""
        while True:
            b1, b2 = self._read(2)
            op, n = b1 & 0x0F, b2 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._read(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._read(8))[0]
            payload = self._read(n)
            if op == 0x9:  # ping
                continue
            msg += payload
            if b1 & 0x80:
                return msg.decode()


class Browser:
    def __init__(self):
        targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
        page = next(t for t in targets if t["type"] == "page")
        self.ws = WS(page["webSocketDebuggerUrl"])
        self.i = 0
        self.events = []
        for d in ("Page", "Runtime", "Log"):
            self.call(d + ".enable")
        self.call("Emulation.setDeviceMetricsOverride",
                  {"width": 1280, "height": 900, "deviceScaleFactor": 1, "mobile": False})

    def call(self, method, params=None):
        self.i += 1
        my = self.i
        self.ws.send(json.dumps({"id": my, "method": method, "params": params or {}}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == my:
                if "error" in m:
                    raise RuntimeError(m["error"])
                return m.get("result", {})
            self.events.append(m)

    def errors(self):
        out = []
        for e in self.events:
            if e.get("method") == "Runtime.exceptionThrown":
                out.append("EXCEPTION " + json.dumps(e["params"]["exceptionDetails"])[:300])
            elif e.get("method") == "Runtime.consoleAPICalled" and e["params"]["type"] in ("error", "warning"):
                out.append("CONSOLE " + json.dumps(e["params"]["args"])[:300])
            elif e.get("method") == "Log.entryAdded" and e["params"]["entry"]["level"] in ("error", "warning"):
                out.append("LOG " + e["params"]["entry"]["text"][:300])
        return out

    def viewport(self, width, height=900, mobile=False, scheme=None):
        self.call("Emulation.setDeviceMetricsOverride",
                  {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": mobile})
        if scheme:
            self.call("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-color-scheme", "value": scheme}]})
        time.sleep(0.3)

    # ---- read-only inspection ----
    def js(self, expr):
        r = self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        if "exceptionDetails" in r:
            raise RuntimeError(r["exceptionDetails"])
        return r["result"].get("value")

    def text(self, sel="#campus-stores"):
        return self.js(f"document.querySelector({json.dumps(sel)}).innerText")

    def status(self):
        return self.text("[data-status]")

    def saved(self):
        return self.js("localStorage.getItem('campus-stores.shift.v1')")

    # ---- navigation ----
    def goto(self, url):
        self.call("Page.navigate", {"url": url})
        self._wait_load()

    def reload(self):
        self.call("Page.reload", {"ignoreCache": True})
        self._wait_load()

    def _wait_load(self):
        time.sleep(0.4)
        for _ in range(50):
            if self.js("document.readyState") == "complete":
                break
            time.sleep(0.1)
        time.sleep(0.3)

    # ---- user input ----
    def _center(self, finder):
        r = self.js(f"""(() => {{ const el = {finder}; if (!el) return null;
            el.scrollIntoView({{block:'center'}}); const b = el.getBoundingClientRect();
            return [b.x + b.width/2, b.y + b.height/2]; }})()""")
        if r is None:
            raise LookupError("element not found: " + finder)
        return r

    def click_el(self, finder):
        x, y = self._center(finder)
        for t in ("mouseMoved", "mousePressed", "mouseReleased"):
            p = {"type": t, "x": x, "y": y}
            if t != "mouseMoved":
                p.update(button="left", clickCount=1)
            self.call("Input.dispatchMouseEvent", p)
        time.sleep(0.25)

    def click(self, label, scope="#campus-stores", nth=0):
        """Click the nth visible button/summary whose text is exactly `label`."""
        finder = (f"[...document.querySelector({json.dumps(scope)}).querySelectorAll('button,summary')]"
                  f".filter(b => b.offsetParent !== null && b.innerText.trim() === {json.dumps(label)})[{nth}]")
        self.click_el(finder)

    def click_in_row(self, row_text, label):
        finder = (f"[...document.querySelectorAll('#campus-stores .row')]"
                  f".find(r => r.innerText.includes({json.dumps(row_text)}))"
                  f"?.querySelector('button')")
        lab = self.js(f"({finder})?.innerText")
        assert lab and lab.strip() == label, (row_text, lab)
        self.click_el(finder)

    def key(self, key, code=None, vk=None):
        code = code or key
        vk = vk or {"ArrowDown": 40, "ArrowUp": 38, "Enter": 13, "Escape": 27, "Home": 36, "Tab": 9}.get(key, 0)
        base = {"key": key, "code": code, "windowsVirtualKeyCode": vk}
        if key == "Enter":
            base["text"] = "\r"
        self.call("Input.dispatchKeyEvent", {"type": "keyDown", **base})
        self.call("Input.dispatchKeyEvent", {"type": "keyUp", **base})
        time.sleep(0.08)

    def choose(self, select_finder, option_text):
        """Pick an option the way a keyboard user would: click the select, arrow to the option, Enter."""
        opts = self.js(f"[...({select_finder}).options].map(o => o.text)")
        if option_text not in opts:
            raise LookupError(f"option {option_text!r} not offered; options are {opts}")
        self.click_el(select_finder)
        cur = self.js(f"({select_finder}).selectedIndex")
        target = opts.index(option_text)
        for _ in range(abs(target - cur)):
            self.key("ArrowDown" if target > cur else "ArrowUp")
        self.key("Enter")
        time.sleep(0.2)
        got = self.js(f"({select_finder}).selectedOptions[0].text")
        if got != option_text:
            raise RuntimeError(f"wanted {option_text!r}, select shows {got!r}")
        return opts

    def type_into(self, finder, text):
        self.click_el(finder)
        self.call("Input.insertText", {"text": text})
        time.sleep(0.1)

    def shot(self, name):
        self.js("scrollTo(0,0)")
        h = self.js("Math.ceil(document.documentElement.scrollHeight)")
        w = self.js("innerWidth")
        r = self.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True,
                                                  "clip": {"x": 0, "y": 0, "width": w, "height": h, "scale": 1}})
        path = os.path.join(SHOTS, name + ".png")
        with open(path, "wb") as f:
            f.write(base64.b64decode(r["data"]))
        return path


def sel_named(name):
    return f"document.querySelector('#campus-stores select[name={name}]')"
