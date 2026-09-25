from __future__ import annotations

import html
import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

LAB_DIR = Path(os.environ.get("OBT_LAB_DIR", "/tmp/obt-scorpion-range"))
EVENTS = LAB_DIR / "portal_events.jsonl"
LAB_TOKEN = os.environ.get("OBT_LAB_TOKEN", "OBT-LAB-2026")

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>OBT SCORPION Training Portal</title>
<style>
body{margin:0;background:#050708;color:#e8f6ef;font-family:system-ui,Arial,sans-serif}
.wrap{max-width:620px;margin:8vh auto;padding:24px}
.card{background:#0b1113;border:1px solid #17332a;border-radius:20px;padding:28px;box-shadow:0 0 40px #001b1222}
.logo{font-size:44px}.title{font-weight:800;letter-spacing:.18em}
.muted{color:#8aa49a}.warn{background:#16120b;border:1px solid #4b3519;padding:12px;border-radius:12px}
input,button{width:100%;box-sizing:border-box;padding:14px;border-radius:12px;margin-top:12px}
input{background:#080d0f;color:white;border:1px solid #29433a}
button{background:#16a36a;border:0;color:white;font-weight:800;cursor:pointer}
.small{font-size:12px}
</style>
</head>
<body>
<div class="wrap">
<div class="card">
<div class="logo">🦂</div>
<div class="title">OBT SCORPION</div>
<p class="muted">OMAR BEN TALEB · isolated wireless training portal</p>
<div class="warn"><b>Training mode.</b> Do not enter a real password. Use the lab token supplied by the exercise.</div>
<form method="post" action="/submit">
<input name="identity" maxlength="32" placeholder="Training identity (e.g. student-01)" required>
<input name="token" maxlength="64" placeholder="Lab token" required>
<button type="submit">Validate training session</button>
</form>
<p class="small muted">This portal intentionally rejects and does not request real credentials.</p>
</div></div>
</body></html>"""


def _append_event(event: dict) -> None:
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


class Handler(BaseHTTPRequestHandler):
    server_version = "OBTScorpionLab/1.0"

    def log_message(self, fmt: str, *args) -> None:
        _append_event({
            "time_utc": datetime.now(timezone.utc).isoformat(),
            "type": "http",
            "client": self.client_address[0],
            "message": fmt % args,
        })

    def _send(self, code: int, body: str, content_type: str = "text/html; charset=utf-8") -> None:
        raw = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        self._send(200, PAGE)

    def do_POST(self) -> None:
        if self.path != "/submit":
            self._send(404, "not found", "text/plain")
            return
        length = min(int(self.headers.get("Content-Length", "0") or 0), 2048)
        form = parse_qs(self.rfile.read(length).decode("utf-8", errors="replace"))
        identity = (form.get("identity") or [""])[0][:32]
        token = (form.get("token") or [""])[0][:64]
        valid = token == LAB_TOKEN

        # Only training metadata is stored. Never persist the submitted token.
        _append_event({
            "time_utc": datetime.now(timezone.utc).isoformat(),
            "type": "training_submission",
            "client": self.client_address[0],
            "identity": identity,
            "valid_lab_token": valid,
        })

        status = "VALID" if valid else "INVALID"
        body = f"""<!doctype html><meta charset="utf-8">
        <body style="background:#050708;color:#e8f6ef;font-family:system-ui;padding:40px">
        <h1>🦂 SCORPION LAB</h1>
        <h2>Training token: {status}</h2>
        <p>Identity: {html.escape(identity)}</p>
        <p>No submitted token was stored.</p>
        </body>"""
        self._send(200, body)


def main() -> None:
    bind = os.environ.get("OBT_PORTAL_BIND", "10.77.0.1")
    port = int(os.environ.get("OBT_PORTAL_PORT", "80"))
    server = ThreadingHTTPServer((bind, port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
