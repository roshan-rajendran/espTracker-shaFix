#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import argparse
import sys
import threading
import time
import webbrowser

from web_ui import app


def _open_browser(port):
    # Wait for server to be listening before opening browser
    time.sleep(3)
    webbrowser.open("http://127.0.0.1:{}".format(port))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ather Tag Locator – track locations in browser or CLI.")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Use terminal instead of web UI (e.g. to register new ESP32 with 'r').",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port for the web UI (default: 5000). Use e.g. 6000 if 5000 is in use.",
    )
    args = parser.parse_args()

    if args.cli:
        from NovaApi.ListDevices.nbe_list_devices import list_devices
        list_devices()
        sys.exit(0)

    port = args.port
    url = "http://127.0.0.1:{}".format(port)
    print("")
    print("=" * 60)
    print("  Ather Tag Locator")
    print("=" * 60)
    print("  Open in your browser (copy if needed):")
    print("  ")
    print("    " + url)
    print("  ")
    print("  Or try:  http://localhost:{}".format(port))
    print("=" * 60)
    print("  If 'site can't be reached': check firewall, or run with  --port 8080")
    print("  Leave this window open while using the app.")
    print("=" * 60)
    print("")
    threading.Thread(target=_open_browser, args=(port,), daemon=True).start()
    app.run(host="0.0.0.0", port=port, threaded=True, use_reloader=False)
