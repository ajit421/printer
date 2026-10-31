# 📝 Master Project Checklist: Raspberry Pi 4 to Low-Power Transition

Follow this checklist step-by-step. Check off each box (`- [x]`) as you complete each task.

---

## 🎯 Phase 1: Raspberry Pi 4 Setup (Local Wi-Fi Print Server)

### Step 1: Flash the MicroSD Card
- [x] Insert the **SanDisk Ultra MicroSD card** (32GB or 64GB) into your PC using a card reader.
- [x] Open **Raspberry Pi Imager** ([Download here](https://www.raspberrypi.com/software/)).
- [x] **Choose Device**: `Raspberry Pi 4`.
- [x] **Choose OS**: `Raspberry Pi OS (other)` ➔ `Raspberry Pi OS Lite (64-bit)`.
- [x] **Choose Storage**: Select your SanDisk MicroSD card.
- [x] Click **Next** and click **Edit Settings**:
  - [x] Set Hostname: `Pi`
  - [x] Set Username: `pi` and enter a password you will remember.
  - [x] Check **Configure wireless LAN**: Enter your Wi-Fi name (SSID) and Password.
  - [x] Go to **Services** tab ➔ Check **Enable SSH** (Use password authentication).
- [x] Click **Save** and **Yes** to write. Wait until verification completes.

---

### Step 2: Physical Connections & First Boot
- [x] Eject the MicroSD card from your PC and insert it into the **Raspberry Pi 4** underside slot.
- [x] Plug in the USB-C power supply (Portronics power bank) to the Raspberry Pi 4.
- [x] Pi booted and joined Wi-Fi (connected via Raspberry Pi Connect).
- [x] Connect the **USB-A to USB-B printer cable** to Brother DCP-T236 and Pi 4.
- [x] Turn ON the **Brother DCP-T236** printer.
- [x] Verified in terminal: `Bus 001 Device 003: ID 04f9:071c Brother Industries, Ltd DCP-T236`.
- [x] Raspberry Pi IP address identified: `192.168.1.64`.

---

### Step 3: Terminal Access & Driver Installation
- [x] Raspberry Pi Connect Remote Shell active in browser.
- [x] CUPS, `printer-driver-brlaser`, and Python dependencies installed.
- [x] Fixed `usblp` kernel conflict.
- [x] Printer detected by CUPS: `usb://Brother/DCP-T236?serial=E83666B6H322824`.

---

### Step 4: Add Brother DCP-T236 in CUPS
- [x] In CUPS Web UI, added **Brother DCP-T236** under Local Printers.
- [x] Set name: `Brother_DCP_T236`.
- [x] Enabled printer sharing.
- [x] Set default options (A4, 600 DPI, Color RGB).
- [x] Printer Status: **Brother_DCP_T236 (Idle, Accepting Jobs, Shared)**!
- [x] Connected to native driverless IPP-over-USB port: `ipp://localhost:60000/ipp/print`.
- [x] Printed official CUPS test page (`pwgrast.ppd` full color wheels).

---

### Step 5: Transfer & Launch GlassyPrint Web Hub
- [x] Transferred `web_app` to Pi from Windows via SCP.
- [x] Launched `python3 /home/pi/web_app/app.py`.
- [x] Opened `http://192.168.1.64:5000` in browser.
- [x] GlassyPrint Hub UI loaded successfully: `Brother_DCP_T236 • Idle / Ready`!
- [x] Uploaded document and clicked **Dispatch Print Job**.
- [x] **Physically verified printing on Brother DCP-T236! (100% SUCCESS!)** 🎉
- [ ] Configure auto-start on boot as a background service.

---

## 🌐 Phase 2: Run 24/7 & Global Remote Printing — [COMPLETED 🎉]
- [x] Configured systemd background service `printer-web.service` (runs on boot).
- [x] Installed Cloudflare Tunnel (`cloudflared`) on Raspberry Pi 4.
- [x] Verified mobile HTTPS tunnel: `https://generating-soma-liberty-perfume.trycloudflare.com`.
- [x] Successfully printed full-color photo (`comp.jpg`) from web app!
- [ ] Make Cloudflare Tunnel run automatically in background on boot.

---

## ⚡ Phase 3: Transition to Low-Power & Cost-Saving (Next Step)

### Option A: The $15 Raspberry Pi Zero 2 W (Recommended)
- [ ] Free up your expensive $60 Raspberry Pi 4 for other projects.
- [ ] Take the exact MicroSD card out of the Pi 4 and insert it into a Pi Zero 2 W.
- [ ] Connect the Brother printer using your official Raspberry Pi Micro-USB OTG cable.
- [ ] Instant 0.5 Watt power consumption (costs less than $1/year in electricity).

### Option B: ESP32 Smart Auto-Power Controller
- [ ] Connect your ESP32 DEVKITV1 to a 5V relay module on the AC mains.
- [ ] ESP32 stays connected to Wi-Fi at 0.05 Watts.
- [ ] When a print request arrives, ESP32 energizes the relay to boot the printer & Pi.
- [ ] Automatically cuts power after 10 minutes of idle time (0W idle standby power).

---

### Step 4: Transfer Project Files & Run Automated Installer
- [ ] On the Pi terminal, clone or copy the `Printer` folder to `/home/pi/Printer`.
  *(Or transfer it from your PC using SCP):*
  ```powershell
  # Run this on your Windows PC in PowerShell:
  scp -r D:\Desktop\Printer pi@printserver.local:/home/pi/
  ```
- [ ] On the Raspberry Pi SSH terminal, run the automated CUPS installer:
  ```bash
  cd /home/pi/Printer/scripts
  chmod +x setup_cups_print_server.sh
  sudo ./setup_cups_print_server.sh
  ```
- [ ] Verify the installer shows: `[✓] Brother printer detected on USB!`.

---

### Step 5: Configure Brother DCP-T236 in CUPS
- [ ] On your PC or phone browser, open:
  ```
  https://printserver.local:631/admin
  ```
  *(Accept the browser security warning since it uses a local self-signed certificate).*
- [ ] Click **Add Printer** and log in with username `pi` and your password.
- [ ] Select **Brother DCP-T236** under Local Printers and click **Continue**.
- [ ] Check the box: **Share This Printer**.
- [ ] Driver Selection: Select **Brother** ➔ **Brother DCP series (or Generic IPP Everywhere / brlaser)**.
- [ ] Click **Add Printer**, set default paper to **A4**, and print a test page!

---

### Step 6: Launch & Auto-Start GlassyPrint Web App
- [ ] Install web app dependencies on the Pi:
  ```bash
  pip install -r /home/pi/Printer/web_app/requirements.txt --break-system-packages
  ```
- [ ] Install the auto-start background service:
  ```bash
  sudo cp /home/pi/Printer/scripts/printer-web.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable printer-web.service
  sudo systemctl start printer-web.service
  ```
- [ ] Check service status:
  ```bash
  sudo systemctl status printer-web.service
  ```
- [ ] Open your phone or laptop browser to:
  👉 **`http://printserver.local:5000`**
- [ ] Upload a test PDF or photo and print it via the glassy web UI!

---

## 🌐 Phase 2: Global Remote Printing (Print from Anywhere via 4G/5G)

- [ ] On the Raspberry Pi terminal, install Cloudflare Tunnel (`cloudflared`):
  ```bash
  curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
  sudo dpkg -i cloudflared.deb
  ```
- [ ] Start a free instant secure tunnel:
  ```bash
  cloudflared tunnel --url http://localhost:5000
  ```
- [ ] Copy the generated public URL (e.g., `https://random-words.trycloudflare.com`).
- [ ] Turn OFF Wi-Fi on your phone (use mobile 4G/5G data).
- [ ] Open the Cloudflare URL on your phone:
  - [ ] GlassyPrint Hub opens cleanly over mobile data.
  - [ ] Upload a file from your phone and click **Dispatch Print Job**.
  - [ ] Verify the Brother printer prints your document at home!

---

## ⚡ Phase 3: Transition to Low-Power & Cost-Saving (Replacing / Freeing Pi 4)

Your motivation is: **Save power and money** (free up the $55+ Raspberry Pi 4 and reduce 24/7 idle electricity).

### Why the Standard ESP32 Cannot Drive the Brother USB Port Directly:
1. The **ESP32 DEVKITV1** has no hardware USB Host controller.
2. The Brother DCP-T236 requires a full **raster engine** (35 MB bitmap per page at 600 DPI); the ESP32 only has 320 KB RAM.
3. Brother inkjet drivers (`brlaser`) only exist for Linux.

### The 3 Paths to Save Power & Money:

#### Path A: The $15 Raspberry Pi Zero 2 W (Best & Easiest)
* **Cost**: ~$15 (frees your $55 Pi 4 for other projects).
* **Power**: Only **~0.5W** (idle) vs 3.5W–5W on Pi 4. Running 24/7 costs less than $1/year in electricity.
* **Size**: 65 mm × 30 mm (same footprint as the ESP32!).
* **Transition Tasks**:
  - [ ] Acquire a Raspberry Pi Zero 2 W.
  - [ ] Take the exact MicroSD card out of the Pi 4 and plug it into the Pi Zero 2 W.
  - [ ] Connect the printer to the Pi Zero 2 W using your **official Raspberry Pi Micro-USB OTG adapter** ([photo](file:///d:/Desktop/Printer/images/04_cables_adapters/07_raspberrypi_microusb_to_usba_otg_adapter.jpg)).
  - [ ] Zero code changes needed—CUPS, GlassyPrint Hub, and Cloudflare work identically.

#### Path B: Use ESP32 as an Auto-Power Switch (Zero Standby Power)
Keep the Raspberry Pi, but use the **ESP32 DEVKITV1** to eliminate 24/7 standby power entirely:
* **How it works**:
  - The ESP32 consumes only **0.05W**.
  - The ESP32 controls a **5V Relay Module** wired to the power input of the Brother Printer and Pi 4.
  - When you want to print, open the web app or hit an ESP32 webhook (`http://esp32-power.local/power-on`).
  - ESP32 powers ON the printer and Pi. The job prints, and 10 minutes later the ESP32 powers them OFF completely.
* **Transition Tasks**:
  - [ ] Connect ESP32 `GPIO 4` to a 5V relay module signal pin.
  - [ ] Flash ESP32 with relay control firmware (see [docs/ESP32_IOT_INTEGRATION.md](file:///d:/Desktop/Printer/docs/ESP32_IOT_INTEGRATION.md)).
  - [ ] Test remote power switching.

---

## 📂 Quick Links & Documentation

- [README.md](file:///d:/Desktop/Printer/README.md) - Project Architecture & Navigation
- [docs/HARDWARE_INVENTORY.md](file:///d:/Desktop/Printer/docs/HARDWARE_INVENTORY.md) - Serial numbers, credentials, and image map
- [docs/PRINT_SERVER_SETUP_GUIDE.md](file:///d:/Desktop/Printer/docs/PRINT_SERVER_SETUP_GUIDE.md) - Detailed CUPS setup instructions
- [docs/GLOBAL_PRINTING_AND_ESP32_ANALYSIS.md](file:///d:/Desktop/Printer/docs/GLOBAL_PRINTING_AND_ESP32_ANALYSIS.md) - Deep technical analysis of ESP32 vs Pi Zero 2 W
- [docs/PRINTER_SPECS_AND_MAINTENANCE.md](file:///d:/Desktop/Printer/docs/PRINTER_SPECS_AND_MAINTENANCE.md) - Printhead cleaning & maintenance procedures
- [web_app/](file:///d:/Desktop/Printer/web_app/) - GlassyPrint Hub Web Application

