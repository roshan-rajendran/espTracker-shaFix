# GoogleFindMyTools

This repository includes some useful tools that reimplement parts of Google's Find My Device Network (now called Find Hub Network). Note that the code of this repo is still very experimental.

### What's possible?
Currently, it is possible to query Find My Device / Find Hub trackers and Android devices, read out their E2EE keys, and decrypt encrypted locations sent from the Find My Device / Find Hub network. You can also send register your own ESP32- or Zephyr-based trackers, as described below.

### How to use

> [!CAUTION]
> Before starting, ensure you have Chrome and Python updated.
> 
> **If Chrome is not up to date, the script will NOT work, guaranteed!**

- Clone this repository: `git clone` or download the ZIP file
- Change into the directory: `cd GoogleFindMyTools`
- Optional: Create venv: `python -m venv venv`
- Optional: Activate venv: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux & macOS)
- Install all required packages: `pip install -r requirements.txt`
- Install the latest version of Google Chrome: https://www.google.com/chrome/
- Start the program by running [main.py](main.py): `python main.py` or `python3 main.py`

### Run fully on your phone (no laptop)

You can run the whole app **on your Android phone** and open the map in the phone’s browser. No computer needed after one-time setup.

**One-time setup (do once on a computer):**

1. On a PC/Mac: run `python main.py`, go through the Google login (Chrome required). After it works, copy the **`Auth`** folder (with `secrets.json` and any cache) to your phone (e.g. via USB, cloud, or messaging yourself). You need this because the first-time Google auth needs Chrome and can’t be done inside Termux.

**On your Android phone:**

1. Install **Termux** from [F-Droid](https://f-droid.org/en/packages/com.termux/) (recommended) or from the [GitHub releases](https://github.com/termux/termux-app/releases). Avoid the Play Store version (often outdated).
2. Open Termux and run:
   ```bash
   pkg update && pkg install python git
   cd ~
   git clone https://github.com/leoboe/GoogleFindMyTools.git
   cd GoogleFindMyTools
   # (Or download the project ZIP and extract it to ~/GoogleFindMyTools, then cd there.)
   pip install -r requirements.txt
   ```
3. Copy the **`Auth`** folder from your computer into `~/GoogleFindMyTools/Auth` (so `Auth/secrets.json` exists). Use Termux’s shared storage or `termux-setup-storage` and copy from Download.
4. Run:
   ```bash
   python main.py
   ```
5. When the tracker list appears, type the number of your tracker and press Enter.
6. The script will print: **Open in your browser: http://127.0.0.1:5000**
7. On the **same phone**, open Chrome (or any browser) and go to **http://127.0.0.1:5000**. You’ll see the map and metadata (lat, lon, time, altitude). Everything runs on the phone.

**Notes:**

- Registering a new ESP32 tracker (`r`) and the first-time Google auth still need a computer with Chrome. After that, use the copied `Auth` folder on the phone.
- If you don’t have a computer at all, you could run the first-time auth in a desktop-style environment on the phone (e.g. UserLAnd with a desktop), but that’s more involved; the usual path is one-time auth on laptop, then phone-only.

### View location on your phone (from a laptop)

If you run `main.py` on a laptop and want to see the map on your phone: when you select a tracker, the script prints a URL like `http://192.168.x.x:5000`. Open that URL on your phone (same Wi‑Fi). The page shows **lat/lon, time, altitude** and a **map** that refreshes every few seconds.

### Authentication

On the first run, an authentication sequence is executed, which requires a computer with access to Google Chrome.

The authentication results are stored in `Auth/secrets.json`. If you intend to run this tool on a headless machine, you can just copy this file to avoid having to use Chrome.

### Known Issues
- "Your encryption data is locked on your device" is shown if you have never set up Find My Device on an Android device. Solution: Login with your Google Account on an Android device, go to Settings > Google > All Services > Find My Device > Find your offline devices > enable "With network in all areas" or "With network in high-traffic areas only". If "Find your offline devices" is not shown in Settings, you will need to download the Find My Device app from Google's Play Store, and pair a real Find My Device tracker with your device to force-enable the Find My Device network.
- No support for trackers using the P-256 curve and 32-Byte advertisements. Regular trackers don't seem to use this curve at all - I can only confirm that it is used with Sony's WH1000XM5 headphones.
- No support for the authentication process on ARM Linux
- If you receive "ssl.SSLCertVerificationError" when running the script, try to follow [this answer](https://stackoverflow.com/a/53310545).
- Please also consider the issues listed in the [README in the ESP32Firmware folder](ESP32Firmware/README.md) if you want to register custom trackers.

### Firmware for custom ESP32-based trackers
If you want to use an ESP32 as a custom Find My Device tracker, you can find the firmware in the folder ESP32Firmware. To register a new tracker, run main.py and press 'r' if you are asked to. Afterward, follow the instructions on-screen.

For more information, check the [README in the ESP32Firmware folder](ESP32Firmware/README.md).

### Firmware for custom Zephyr-based trackers
If you want to use a Zephyr-supported BLE device (e.g. nRF51/52) as a custom Find My Device tracker, you can find the firmware in the folder ZephyrFirmware. To register a new tracker, run main.py and press 'r' if you are asked to. Afterward, follow the instructions on-screen.

For more information, check the [README in the ZephyrFirmware folder](ZephyrFirmware/README.md).

### iOS App
You can also use my [iOS App](https://testflight.apple.com/join/rGqa2mTe) to access your Find My Device trackers on the go.
