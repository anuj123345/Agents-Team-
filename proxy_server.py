"""
Agent Teams UI — Local proxy server
- Serves the HTML/CSS/JS files at http://localhost:8080
- Proxies POST /api/chat  →  https://integrate.api.nvidia.com/v1/chat/completions
  (server-to-server, so CORS is bypassed entirely)
"""

import http.server
import urllib.request
import urllib.error
import json
import os
import sys
import mimetypes

PORT = 8080
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
DIR = os.path.dirname(os.path.abspath(__file__))


class ProxyHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        # Quiet logging — only show errors
        if args and str(args[1]) not in ("200", "304"):
            print(f"  {args[0]}  →  {args[1]}")

    # ── CORS preflight ───────────────────────────────────────────────────────
    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    # ── Static files ─────────────────────────────────────────────────────────
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/" or path == "":
            path = "/agent-teams-ui.html"

        file_path = os.path.join(DIR, path.lstrip("/"))
        if os.path.isfile(file_path):
            mime, _ = mimetypes.guess_type(file_path)
            mime = mime or "application/octet-stream"
            with open(file_path, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(data)))
            self._cors()
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self._cors()
            self.end_headers()
            self.wfile.write(b"Not found")

    # ── Proxy API calls ───────────────────────────────────────────────────────
    def do_POST(self):
        if self.path != "/api/chat":
            self.send_response(404)
            self._cors()
            self.end_headers()
            return

        # Read request body
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        # Forward Authorization header from client
        auth = self.headers.get("Authorization", "")

        req = urllib.request.Request(
            NVIDIA_URL,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": auth,
                "Accept": "text/event-stream",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                self.send_response(resp.status)
                # Forward relevant headers
                for key, val in resp.headers.items():
                    if key.lower() in ("content-type", "transfer-encoding", "cache-control"):
                        self.send_header(key, val)
                self._cors()
                self.end_headers()
                # Stream response back to browser
                while True:
                    chunk = resp.read(4096)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    self.wfile.flush()

        except urllib.error.HTTPError as e:
            err_body = e.read()
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
            self.wfile.write(err_body)
        except Exception as ex:
            self.send_response(502)
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(ex)}).encode())

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")


if __name__ == "__main__":
    os.chdir(DIR)
    server = http.server.HTTPServer(("", PORT), ProxyHandler)
    print(f"\n  Agent Teams UI  →  http://localhost:{PORT}/agent-teams-ui.html")
    print(f"  API proxy       →  /api/chat  →  {NVIDIA_URL}")
    print(f"  Press Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
