# Flashing with Arduino IDE (no ESP-IDF)

Use this if you don’t want to install the full ESP-IDF. The Arduino ESP32 core is much smaller.

**Supported board:** **ESP32** (e.g. “ESP32 Dev Module”, ESP32-CAM).  
**ESP32-C3** is not supported in this Arduino sketch (it uses NimBLE); use the ESP-IDF project for ESP32-C3.

## Steps

1. **Install ESP32 in Arduino IDE**  
   - **Arduino IDE** → **Tools** → **Board** → **Boards Manager**  
   - Search for **“esp32”** → install **“esp32” by Espressif Systems**.

2. **Get your advertisement key**  
   - Run the Python script in the repo root: `python3 main.py`  
   - When the device list is shown, press **`r`** to register a new device.  
   - Copy the **advertisement key (EID)** (40 hex characters).

3. **Put the key in the sketch**  
   - Open **`ESP32Firmware/Arduino/ESPFindMy/ESPFindMy.ino`** in Arduino IDE.  
   - Find the line:  
     `const char* EID_STRING = "2f66bdf918dd862c7b6bcd67aba717fb97858f49";`  
   - Replace that string with your copied EID.

4. **Build and flash**  
   - **Tools** → **Board** → **ESP32 Dev Module** (or your exact board).  
   - **Tools** → **Port** → select your ESP32’s serial port.  
   - Click **Upload**.  
   - When upload finishes, the ESP32 will start advertising as your Find My Device tracker.

No ESP-IDF installation is required; only the Arduino IDE and the ESP32 board package are used.
