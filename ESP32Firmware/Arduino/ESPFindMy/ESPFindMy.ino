/*
 * Find My Device (FMDN) - Arduino version for ESP32 (classic)
 * Same behavior as the ESP-IDF main.c; use Arduino IDE to build and flash.
 *
 * Board: ESP32 Dev Module (or ESP32-CAM). For ESP32-C3 use the ESP-IDF project.
 * 
 * 1. Get your advertisement key (EID) from the Python script (main.py -> press 'r').
 * 2. Paste it in EID_STRING below.
 * 3. Build & Upload in Arduino IDE.
 */

#include <Arduino.h>
#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_bt_main.h"
#include "esp_gap_ble_api.h"
#include "esp_err.h"

// -------- Paste your advertisement key (EID) from main.py here --------
const char* EID_STRING = "2f66bdf918dd862c7b6bcd67aba717fb97858f49";

// FMDN raw BLE advertisement (31 bytes). Bytes 8..27 are filled with EID at runtime.
uint8_t adv_raw_data[31] = {
    0x02, 0x01, 0x06,   // Flags
    0x19, 0x16,         // Length, Service Data type
    0xAA, 0xFE,         // 16-bit UUID 0xFEAA
    0x41,               // FMDN frame type (unwanted tracking protection)
    // 8..27: 20-byte EID (filled in setup)
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0x00                // Hashed flags
};

void hexStringToBytes(const char* hex, uint8_t* bytes, size_t len) {
    for (size_t i = 0; i < len; i++) {
        sscanf(hex + 2 * i, "%2hhx", &bytes[i]);
    }
}

void setup() {
    Serial.begin(115200);
    delay(500);
    Serial.println("ESP Find My Device (Arduino)");

    // NVS init (required for BLE)
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        nvs_flash_erase();
        ret = nvs_flash_init();
    }
    if (ret != ESP_OK) {
        Serial.printf("NVS init failed: 0x%x\n", ret);
        return;
    }

    // Fill EID into advertisement
    uint8_t eid_bytes[20];
    hexStringToBytes(EID_STRING, eid_bytes, 20);
    memcpy(&adv_raw_data[8], eid_bytes, 20);

    // BLE controller
    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    if (esp_bt_controller_init(&bt_cfg) != ESP_OK ||
        esp_bt_controller_enable(ESP_BT_MODE_BLE) != ESP_OK) {
        Serial.println("BT controller init failed");
        return;
    }

    if (esp_bluedroid_init() != ESP_OK || esp_bluedroid_enable() != ESP_OK) {
        Serial.println("Bluedroid init failed");
        return;
    }

    // TX power (optional, for range)
    esp_ble_tx_power_set(ESP_BLE_PWR_TYPE_DEFAULT, ESP_PWR_LVL_P9);
    esp_ble_tx_power_set(ESP_BLE_PWR_TYPE_ADV, ESP_PWR_LVL_P9);

    // Set raw advertisement data
    if (esp_ble_gap_config_adv_data_raw(adv_raw_data, sizeof(adv_raw_data)) != ESP_OK) {
        Serial.println("Failed to set adv data");
        return;
    }

    esp_ble_adv_params_t adv_params = {};
    adv_params.adv_int_min       = 0x20;
    adv_params.adv_int_max       = 0x20;
    adv_params.adv_type          = ADV_TYPE_NONCONN_IND;
    adv_params.own_addr_type     = BLE_ADDR_TYPE_PUBLIC;
    adv_params.channel_map       = ADV_CHNL_ALL;
    adv_params.adv_filter_policy = ADV_FILTER_ALLOW_SCAN_ANY_CON_ANY;

    if (esp_ble_gap_start_advertising(&adv_params) != ESP_OK) {
        Serial.println("Failed to start advertising");
        return;
    }

    Serial.println("BLE advertising started (Find My Device).");
}

void loop() {
    delay(1000);
}
