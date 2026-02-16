#
#  GoogleFindMyTools - Web UI to view tracker location on phone
#  Serves a single HTML page with map + metadata; run after selecting a device in main.py
#

import threading
from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder=None)

# Updated by location_request when location response is received
_device_name = ""
_locations = []
_server_thread = None
_app_ref = None

HTML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_ui_html")


def set_locations(device_name: str, locations: list):
    global _device_name, _locations
    _device_name = device_name or ""
    _locations = list(locations) if locations else []


def get_locations():
    return _device_name, _locations


@app.route("/")
def index():
    return send_from_directory(HTML_DIR, "index.html")


@app.route("/api/location")
def api_location():
    device_name, locations = get_locations()
    # Latest geo location (with lat/lon) for map; fallback to first
    latest = None
    for loc in reversed(locations):
        if not loc.get("semantic") and loc.get("latitude") is not None:
            latest = loc
            break
    return jsonify({
        "device_name": device_name,
        "locations": locations,
        "latest": latest,
    })


def _run_server(port: int):
    global _app_ref
    _app_ref = app
    app.run(host="0.0.0.0", port=port, threaded=True, use_reloader=False)


def start_web_server(port: int = 5000):
    """Start the web UI server in a background thread. Call before requesting location."""
    global _server_thread
    if _server_thread is not None and _server_thread.is_alive():
        return
    _server_thread = threading.Thread(target=_run_server, args=(port,), daemon=True)
    _server_thread.start()
    import socket
    host = "localhost"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host = s.getsockname()[0]
        s.close()
    except Exception:
        pass
    print("")
    print("-" * 50)
    print("Web UI: Open in your browser:")
    print(f"  On THIS device (e.g. phone):  http://127.0.0.1:{port}")
    if host != "localhost":
        print(f"  From another device (same Wi‑Fi): http://{host}:{port}")
    print("-" * 50)
    print("")
