# Hardware Inventory Catalog & Image Mapping

This document provides a comprehensive hardware audit of all components photographed in the workspace, complete with electrical ratings, pinouts, serial numbers, credentials, and mapped file references.

---

## 1. Brother DCP-T236 All-in-One Ink Tank Printer

| Attribute | Specification |
|---|---|
| **Manufacturer** | Brother Industries, Ltd. |
| **Model** | DCP-T236 (Print, Scan, Copy) |
| **Serial Number** | `E83666B6H322824` |
| **Default Password** | `MkdxOpVJ` (printed on rear specification plate) |
| **Input Power** | 220V - 240V AC ~ 50/60 Hz, 0.25A |
| **Country of Origin** | Made in Philippines (D034VS001) |
| **Safety / Compliance** | BIS R-41010340 (IS 13252 Part 1 / IEC 60950-1) |
| **Ink System** | Refillable BTD100 4-color tank system (Black, Cyan, Magenta, Yellow) |
| **Rated Page Yield** | Up to 7,500 Black pages, 5,000 Colour pages |
| **Print Speed** | Up to 16.0 ipm (Mono) / 9.0 ipm (Colour) |
| **Paper Capacity** | 150 Sheets Default Front Loading Paper Tray |
| **Controls** | Stop/Power, Copy Shortcut, Mono Copy, Colour Copy |
| **Scan Shortcut** | Press `Mono Copy` + `Colour Copy` simultaneously |

### Photographed References:
- [01_brother_dcpt236_front_overview.jpg](file:///d:/Desktop/Printer/images/01_brother_printer/01_brother_dcpt236_front_overview.jpg): Top-front perspective showing body, control buttons, and ink bay.
- [02_brother_dcpt236_ink_tanks.jpg](file:///d:/Desktop/Printer/images/01_brother_printer/02_brother_dcpt236_ink_tanks.jpg): Front viewing window displaying BTD100 Magenta, Cyan, Yellow, and Black levels.
- [03_brother_dcpt236_control_panel.jpg](file:///d:/Desktop/Printer/images/01_brother_printer/03_brother_dcpt236_control_panel.jpg): Button panel, LED indicator status lights, and QR code `B6H322824`.
- [04_brother_dcpt236_model_badge.jpg](file:///d:/Desktop/Printer/images/01_brother_printer/04_brother_dcpt236_model_badge.jpg): Model badge confirming `DCP-T236`.
- [05_brother_dcpt236_cleaning_troubleshooting_guide.jpg](file:///d:/Desktop/Printer/images/01_brother_printer/05_brother_dcpt236_cleaning_troubleshooting_guide.jpg): Instruction decal `D03948001` detailing Normal and Special head cleaning.
- [06_brother_dcpt236_serial_password_label.jpg](file:///d:/Desktop/Printer/images/01_brother_printer/06_brother_dcpt236_serial_password_label.jpg): Factory label with barcode, serial number, default password, and power specifications.
- [07_brother_dcpt236_retail_box.jpg](file:///d:/Desktop/Printer/images/01_brother_printer/07_brother_dcpt236_retail_box.jpg): Packaging box showing model details, speed, and bottle yields.

---

## 2. Raspberry Pi 4 Model B (4GB RAM)

| Attribute | Specification |
|---|---|
| **SoC** | Broadcom BCM2711, Quad-core Cortex-A72 (ARM v8) 64-bit @ 1.5 GHz / 1.8 GHz |
| **RAM** | 4GB LPDDR4-3200 SDRAM |
| **Networking** | 2.4 GHz and 5.0 GHz IEEE 802.11b/g/n/ac wireless, Bluetooth 5.0, BLE, Gigabit Ethernet |
| **USB Ports** | 2 × USB 3.0 ports (Blue), 2 × USB 2.0 ports (Black) |
| **Display Outputs** | 2 × Micro-HDMI ports (supporting up to 4kp60) |
| **Power Port** | 5V DC via USB-C (minimum 3.0A recommended) |
| **Storage in Board** | SanDisk Ultra 32GB MicroSD card installed in slot |
| **FCC ID / IC** | 2ABCB-RPI4B / 20953-RPI4B |

### Photographed References:
- [01_raspberry_pi_4b_4gb_top.jpg](file:///d:/Desktop/Printer/images/02_raspberry_pi/01_raspberry_pi_4b_4gb_top.jpg): Top layout showing Broadcom SoC, USB 3.0/2.0 controllers, Trxcom Ethernet jack, and 40-pin GPIO.
- [02_raspberry_pi_4b_bottom_sandisk_32gb.jpg](file:///d:/Desktop/Printer/images/02_raspberry_pi/02_raspberry_pi_4b_bottom_sandisk_32gb.jpg): Underside of PCB showing pre-inserted SanDisk Ultra 32GB MicroSD.
- [03_raspberry_pi_4b_retail_box.jpg](file:///d:/Desktop/Printer/images/02_raspberry_pi/03_raspberry_pi_4b_retail_box.jpg): Official Raspberry Pi retail carton indicating 4GB RAM capacity.

---

## 3. ESP32 Development Board (DEVKITV1)

| Attribute | Specification |
|---|---|
| **Module** | ESP-WROOM-32 (Espressif Systems) |
| **Core** | Dual-core Tensilica Xtensa 32-bit LX6 microprocessor @ up to 240 MHz |
| **Connectivity** | Wi-Fi: 802.11 b/g/n (up to 150 Mbps), Bluetooth v4.2 BR/EDR and BLE |
| **Board Label** | `ESP32 DEVKITV1` (30 pins) |
| **Interface** | Micro-USB connector for power and UART flashing |
| **Buttons** | `EN` (Reset) and `BOOT` (Flash / GPIO 0) |
| **Operating Voltage**| 3.3V logic; 5V supply input via VIN or Micro-USB |

### Photographed References:
- [01_esp32_devkit_v1_top.jpg](file:///d:/Desktop/Printer/images/03_esp32/01_esp32_devkit_v1_top.jpg): Front component layout, shielding can, antenna, and push buttons.
- [02_esp32_devkit_v1_bottom.jpg](file:///d:/Desktop/Printer/images/03_esp32/02_esp32_devkit_v1_bottom.jpg): Rear silkscreen identifying the board as `ESP32 DEVKITV1`.

---

## 4. Cables & Interfacing Adapters

| Item | Connectors | Application in this Setup | File Reference |
|---|---|---|---|
| **Printer Cable** | USB-A Male to USB-B Male | Connects Raspberry Pi USB port to Brother DCP-T236 rear port | [02_usba_to_usbb_printer_cable_full.jpg](file:///d:/Desktop/Printer/images/04_cables_adapters/02_usba_to_usbb_printer_cable_full.jpg)<br>[03_usbb_printer_connector_closeup.jpg](file:///d:/Desktop/Printer/images/04_cables_adapters/03_usbb_printer_connector_closeup.jpg)<br>[04_usba_connector_closeup.jpg](file:///d:/Desktop/Printer/images/04_cables_adapters/04_usba_connector_closeup.jpg) |
| **Type-C OTG Cable** | USB-C Male to USB-A Female (Red) | Allows connecting USB-A devices directly to USB-C host devices | [01_usbc_to_usba_otg_cable_red.jpg](file:///d:/Desktop/Printer/images/04_cables_adapters/01_usbc_to_usba_otg_cable_red.jpg) |
| **Pi Micro-USB OTG Adapter** | Micro-USB Male to USB-A Female (Official) | Official Raspberry Pi adapter with molded logo | [07_raspberrypi_microusb_to_usba_otg_adapter.jpg](file:///d:/Desktop/Printer/images/04_cables_adapters/07_raspberrypi_microusb_to_usba_otg_adapter.jpg)<br>[08_raspberrypi_otg_connectors_closeup.jpg](file:///d:/Desktop/Printer/images/04_cables_adapters/08_raspberrypi_otg_connectors_closeup.jpg) |
| **Micro-USB Cable** | USB-A Male to Micro-USB Male (White) | Power and serial communication for ESP32 board | [05_usba_to_microusb_cable.jpg](file:///d:/Desktop/Printer/images/04_cables_adapters/05_usba_to_microusb_cable.jpg)<br>[06_microusb_and_usba_connectors.jpg](file:///d:/Desktop/Printer/images/04_cables_adapters/06_microusb_and_usba_connectors.jpg) |

---

## 5. Power & Storage

| Item | Model / Specs | Role | File Reference |
|---|---|---|---|
| **Power Bank** | Portronics 10,000 mAh (Model '10') | Portable 5V power supply with integrated Type-C loop | [01_portronics_10000mah_powerbank.jpg](file:///d:/Desktop/Printer/images/05_power_storage/01_portronics_10000mah_powerbank.jpg) |
| **Primary MicroSD** | SanDisk Ultra 32GB (Inserted in Pi) | OS boot drive for Raspberry Pi OS Lite | [02_raspberry_pi_4b_bottom_sandisk_32gb.jpg](file:///d:/Desktop/Printer/images/02_raspberry_pi/02_raspberry_pi_4b_bottom_sandisk_32gb.jpg) |
| **Secondary MicroSD** | SanDisk Ultra 64GB MicroSDXC (Class 10, A1) | High-capacity backup storage / media expansion | [02_sandisk_ultra_64gb_microsd.jpg](file:///d:/Desktop/Printer/images/05_power_storage/02_sandisk_ultra_64gb_microsd.jpg) |

---

## 6. Original Raw Photo Mapping Table

For archival integrity, all original unrenamed smartphone files were transferred to [raw_camera_photos/](file:///d:/Desktop/Printer/raw_camera_photos/):

| Original Camera Filename | New Organized Path |
|---|---|
| `IMG_20261029_123402305.jpg` | `images/01_brother_printer/01_brother_dcpt236_front_overview.jpg` |
| `IMG_20261029_123409909.jpg` | `images/01_brother_printer/02_brother_dcpt236_ink_tanks.jpg` |
| `IMG_20261029_123417891.jpg` | `images/01_brother_printer/03_brother_dcpt236_control_panel.jpg` |
| `IMG_20261029_123422461.jpg` | `images/01_brother_printer/04_brother_dcpt236_model_badge.jpg` |
| `IMG_20261029_125339127.jpg` | `images/01_brother_printer/05_brother_dcpt236_cleaning_troubleshooting_guide.jpg` |
| `IMG_20261029_125418350.jpg` | `images/01_brother_printer/06_brother_dcpt236_serial_password_label.jpg` |
| `IMG_20261029_130333586_MP.jpg` | `images/01_brother_printer/07_brother_dcpt236_retail_box.jpg` |
| `IMG_20261031_130015055_HDR.jpg` | `images/02_raspberry_pi/01_raspberry_pi_4b_4gb_top.jpg` |
| `IMG_20261031_130020658_HDR.jpg` | `images/02_raspberry_pi/02_raspberry_pi_4b_bottom_sandisk_32gb.jpg` |
| `IMG_20261031_130029853_HDR.jpg` | `images/02_raspberry_pi/03_raspberry_pi_4b_retail_box.jpg` |
| `IMG_20261031_130049014_HDR.jpg` | `images/04_cables_adapters/01_usbc_to_usba_otg_cable_red.jpg` |
| `IMG_20261031_130058522_MP.jpg` | `images/04_cables_adapters/02_usba_to_usbb_printer_cable_full.jpg` |
| `IMG_20261031_130104536_HDR.jpg` | `images/04_cables_adapters/03_usbb_printer_connector_closeup.jpg` |
| `IMG_20261031_130109473_HDR.jpg` | `images/04_cables_adapters/04_usba_connector_closeup.jpg` |
| `IMG_20261031_130404079_HDR.jpg` | `images/03_esp32/01_esp32_devkit_v1_top.jpg` |
| `IMG_20261031_130407975_HDR.jpg` | `images/03_esp32/02_esp32_devkit_v1_bottom.jpg` |
| `IMG_20261031_130509974_HDR.jpg` | `images/04_cables_adapters/05_usba_to_microusb_cable.jpg` |
| `IMG_20261031_130528166_HDR.jpg` | `images/04_cables_adapters/06_microusb_and_usba_connectors.jpg` |
| `IMG_20261031_130535239_HDR.jpg` | `images/04_cables_adapters/07_raspberrypi_microusb_to_usba_otg_adapter.jpg` |
| `IMG_20261031_130553841_HDR.jpg` | `images/04_cables_adapters/08_raspberrypi_otg_connectors_closeup.jpg` |
| `IMG_20261031_130635728_HDR.jpg` | `images/05_power_storage/01_portronics_10000mah_powerbank.jpg` |
| `IMG_20261031_131312289.jpg` | `images/05_power_storage/02_sandisk_ultra_64gb_microsd.jpg` |

