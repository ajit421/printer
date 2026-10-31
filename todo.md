# 📝 Master Project Checklist: Raspberry Pi 4 to Low-Power Transition

Follow this checklist step-by-step. Check off each box (`- [x]`) as you complete each task.

---

## 🎯 Phase 1: Raspberry Pi 4 Setup (Local Wi-Fi Print Server)

### Step 1: Flash the MicroSD Card
- [ ] Insert the **SanDisk Ultra MicroSD card** (32GB or 64GB) into your PC using a card reader.
- [ ] Open **Raspberry Pi Imager** ([Download here](https://www.raspberrypi.com/software/)).
- [ ] **Choose Device**: `Raspberry Pi 4`.
- [ ] **Choose OS**: `Raspberry Pi OS (other)` ➔ `Raspberry Pi OS Lite (64-bit)`.
- [ ] **Choose Storage**: Select your SanDisk MicroSD card.
- [ ] Click **Next** and click **Edit Settings**:
  - [ ] Set Hostname: `printserver`
  - [ ] Set Username: `pi` and enter a password you will remember.
  - [ ] Check **Configure wireless LAN**: Enter your Wi-Fi name (SSID) and Password.
  - [ ] Go to **Services** tab ➔ Check **Enable SSH** (Use password authentication).
- [ ] Click **Save** and **Yes** to write. Wait until verification completes.

---

### Step 2: Physical Connections
- [ ] Eject the MicroSD card from your PC and insert it into the **Raspberry Pi 4** underside slot ([photo](file:///d:/Desktop/Printer/images/02_raspberry_pi/02_raspberry_pi_4b_bottom_sandisk_32gb.jpg)).
- [ ] Connect the **USB-A to USB-B printer cable** ([photo](file:///d:/Desktop/Printer/images/04_cables_adapters/02_usba_to_usbb_printer_cable_full.jpg)):
  - Square USB-B plug ➔ Brother DCP-T236 rear port.
  - Flat USB-A plug ➔ Raspberry Pi 4 black USB 2.0 port.
- [ ] Turn ON the **Brother DCP-T236** printer.
- [ ] Plug in the USB-C power supply (5V 3A or Portronics power bank) to the Raspberry Pi 4.
- [ ] Wait 60–90 seconds for the Pi to boot and join your Wi-Fi network.

---

### Step 3: Connect via SSH
- [ ] Open PowerShell or Command Prompt on your PC and run:
  ```powershell
  ssh pi@printserver.local
  ```
  *(If `printserver.local` does not resolve, check your home router admin page for the Pi's IP address, e.g., `ssh pi@192.168.1.50`).*
- [ ] Type your password when prompted and press Enter.

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
