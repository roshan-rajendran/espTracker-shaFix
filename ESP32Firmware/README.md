# Find My Device ESP32 Firmware

This code enables you to use an ESP32-device as a custom Google Find My Device tracker. Note that the firmware is very experimental. 

The firmware works differently to regular Find My Device trackers. It is made to be as simple as possible. It has no Fast Pair support, MAC rotation, advertisement rotation, etc.

Currently known working devices include the ESP32 (Dev Module V1), the ESP32-CAM, and ESP32-C3. If you use a different board and it works/doesn't work, feel free to message me, I'll update this README then.

---

**Don’t want to install ESP-IDF?** You can build and flash with **Arduino IDE** instead (smaller install). See **[Arduino/README.md](Arduino/README.md)** and open the sketch in `Arduino/ESPFindMy/`. Works for **ESP32** and **ESP32-CAM**; for **ESP32-C3** you still need the ESP-IDF project below.

---

## How to use (ESP-IDF / VS Code)

- Run the Python Script [`main.py`](../main.py) in the parent folder. Follow the instructions of the [README of the parent folder](../README.md).
- When the device list is displayed, press 'r' to register a new ESP32/Zephyr device in your account. Copy the displayed advertisement key.
- Install Visual Studio Code [here](https://code.visualstudio.com/download)
- Go to Visual Studio Code Extensions, search, install and open 'ESP-IDF' by Espressif
- **Open only the ESP32 firmware folder in VS Code**: use **File → Open Folder** and choose the `ESP32Firmware` folder (the one that contains this README). Do not open the parent repo `GoogleFindMyTools`—the ESP-IDF extension expects the project root to be the ESP-IDF app (where `CMakeLists.txt` and `main/` live).
- Navigate to the folder main, select the file [`main.c`](main/main.c)
- Edit Line 15, and insert the advertisement key retrieved from the Python Script
- Connect your ESP32 to your system with USB
- On the bottom left of Visual Studio Code, click the 'plug' icon and select your ESP32, it should be named '/dev/tty.usbserial-0001' or similar
- **Build first**: click the **wrench** icon (or **ESP-IDF: Build your project** from the Command Palette) and wait until you see "Project build complete". Do not use the Fire icon until the build has finished successfully.
- **Then flash**: click the 'Fire' icon to flash the firmware. If you flash without building, you will get "flasher_args.json file is missing".
- If asked, use UART as flash method
- After flashing, the ESP32 will restart and start advertising as the Find My Device tracker previously registered


## Troubleshooting (VS Code / ESP-IDF extension)

### "flasher_args.json file is missing from the build directory"
- You tried to **flash** without **building** first. The build step creates `build/flasher_args.json`.
- **Fix**: Run **ESP-IDF: Build your project** (wrench icon or Command Palette), wait for "Project build complete", then use the Fire icon to flash.

### "ENOENT: no such file or directory, stat '/components/esptool_py/esptool/esptool.py'"
- The extension is looking for ESP-IDF tools in the wrong place. This usually happens if you opened the **parent repo** (e.g. `GoogleFindMyTools`) in VS Code instead of the **ESP32Firmware** folder.
- **Fix**: Close VS Code, then **File → Open Folder** and select only the **ESP32Firmware** folder (the one that contains this README and `main/`). Rebuild and flash from there.
- If you must keep the whole repo open, use **File → Add Folder to Workspace** and add `ESP32Firmware`, then use **File → Open Folder** on `ESP32Firmware` in the sidebar so the ESP-IDF extension treats it as the project root. Alternatively, in the ESP-IDF extension config, ensure **IDF_PATH** (or `idf.espIdfPath`) points to your real ESP-IDF install (e.g. `~/esp/esp-idf`), not to this project.

### "Something went wrong while trying to build the project"
Try these in order:

1. **Set the target chip**  
   The project supports both **ESP32** and **ESP32-C3**. You must pick one:
   - **Command Palette** (Ctrl+Shift+P / Cmd+Shift+P) → **ESP-IDF: Set Espressif device target**
   - Choose **esp32** (Dev Module, ESP32-CAM) or **esp32c3** (ESP32-C3), then run **Build** again.

2. **Check ESP-IDF is configured**  
   - **Command Palette** → **ESP-IDF: Configure ESP-IDF extension** and complete the setup (IDF path, Python, tools).  
   - **Command Palette** → **ESP-IDF: Show ESP-IDF doctor output** and fix any reported errors (missing IDF_PATH, Python, or tools).

3. **Use the right folder**  
   - Build only works when the **project root** is `ESP32Firmware` (the folder that contains this README and `main/`).  
   - **File → Open Folder** → select `ESP32Firmware`, then build again.

4. **Full clean and reconfigure**  
   - Delete the `build` folder inside `ESP32Firmware`.  
   - **Command Palette** → **ESP-IDF: Set Espressif device target** → choose your board.  
   - **Command Palette** → **ESP-IDF: Build your project**.

5. **Build from a terminal (to see the real error)**  
   In a terminal where ESP-IDF is active (e.g. after running the ESP-IDF export script), run:
   ```bash
   cd /path/to/GoogleFindMyTools/ESP32Firmware
   idf.py set-target esp32        # or esp32c3
   idf.py build
   ```
   The last command will print the actual compiler/CMake error so you can fix it or search for it.

### Build from command line (optional)
From the `ESP32Firmware` directory, with ESP-IDF environment sourced (e.g. `. $HOME/esp/esp-idf/export.sh`), run:
```bash
idf.py set-target esp32           # or esp32c3 for ESP32-C3 boards
idf.py build
idf.py -p /dev/tty.usbserial-0001 flash
```
Replace the port with your actual serial device.

## Known Issues

- You need to run [`main.py`](../main.py) every 4 days to keep receiving location reports from the server. This is because the advertisements have to be "announced" to Google. 
- Might not work with 'fresh' Google accounts: "Your encryption data is locked on your device" is shown if you have never paired a Find My Device tracker with an Android device. Solution: See ion in vs code 

[README of the parent folder](../README.md).
- You cannot view locations for the ESP32 in the Google Find My Device app. You will need to use the Python script to do so.
- No privacy features such as rotating MAC addresses are implemented
- The firmware was built to receive as many network reports as possible. Therefore, it might consume more power than necessary. To fix this, you can tweak the parameters (TX Power and advertising interval) in [`main.c`](main/main.c)
