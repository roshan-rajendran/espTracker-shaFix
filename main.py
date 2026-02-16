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


def _open_browser():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ather Tag Locator – track locations in browser or CLI.")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Use terminal instead of web UI (e.g. to register new ESP32 with 'r').",
    )
    args = parser.parse_args()

    if args.cli:
        from NovaApi.ListDevices.nbe_list_devices import list_devices
        list_devices()
        sys.exit(0)

    print("Starting Ather Tag Locator at http://127.0.0.1:5000")
    print("Select a tracker and click 'Get location' to see it on the map.")
    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=False)
