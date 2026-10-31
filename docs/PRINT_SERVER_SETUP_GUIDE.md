# Brother DCP-T236 Wireless Print Server Setup Guide

This guide walks through configuring your **Raspberry Pi 4 Model B (4GB)** as a headless, network-attached print server for the **Brother DCP-T236**, enabling wireless printing from Windows, macOS, Linux, iOS (AirPrint), and Android (Mopria).

---

## 🛠️ Required Hardware from Inventory

1. **Brother DCP-T236 Printer** with power cable.
2. **Raspberry Pi 4 Model B (4GB)**.
3. **USB-A to USB-B Printer Cable** ([images/04_cables_adapters/02_usba_to_usbb_printer_cable_full.jpg](file:///d:/Desktop/Printer/images/04_cables_adapters/02_usba_to_usbb_printer_cable_full.jpg)).
4. **SanDisk Ultra MicroSD Card** (32GB or 64GB).
5. **Power Supply**: 5V 3A USB-C adapter (or the Portronics 10,000 mAh power bank for portable testing).
6. Home Wi-Fi network credentials.

---

## ⚙️ Step 1: Prepare the Raspberry Pi OS

1. Download and run **Raspberry Pi Imager** on your PC.
2. Choose OS: `Raspberry Pi OS (other)` -> `Raspberry Pi OS Lite (64-bit)`.
3. Choose Storage: Select your SanDisk MicroSD card.
4. Click **Next** and click **Edit Settings**:
   - Hostname: `printserver.local`
   - Set Username (e.g., `pi`) and a secure password.
   - Configure Wireless LAN: Enter your Wi-Fi SSID and Password. Set Wireless LAN country.
   - Services tab: Check **Enable SSH** (use password authentication or public key).
5. Click **Save** and flash the MicroSD card.
6. Insert the card into the Raspberry Pi 4 card slot ([images/02_raspberry_pi/02_raspberry_pi_4b_bottom_sandisk_32gb.jpg](file:///d:/Desktop/Printer/images/02_raspberry_pi/02_raspberry_pi_4b_bottom_sandisk_32gb.jpg)).

---

## 🔌 Step 2: Physical Connections

1. Connect the square **USB-B plug** of the printer cable to the Brother DCP-T236 rear port.
2. Connect the flat **USB-A plug** to one of the black USB 2.0 ports on the Raspberry Pi 4.
3. Power on the Brother DCP-T236.
4. Plug the USB-C power into the Raspberry Pi 4. Wait ~60 seconds for it to boot and join your Wi-Fi.

---

## 💻 Step 3: Install CUPS and Print Drivers

Open PowerShell or terminal on your PC and connect to the Pi via SSH:

```bash
ssh pi@printserver.local
```

### Option A: Run the Automated Script
We have prepared a complete automated script in `scripts/`:

```bash
# Transfer or clone scripts/setup_cups_print_server.sh to the Pi, then run:
chmod +x setup_cups_print_server.sh
sudo ./setup_cups_print_server.sh
```

### Option B: Manual Installation
If you prefer running commands manually:

```bash
# 1. Update package lists
sudo apt update && sudo apt upgrade -y

# 2. Install CUPS, print drivers, and Avahi (Bonjour/AirPrint discovery)
sudo apt install -y cups cups-client cups-filters printer-driver-brlaser avahi-daemon

# 3. Add user to print admin group
sudo usermod -a -G lpadmin $USER

# 4. Allow remote web management on port 631
sudo cupsctl --remote-admin --remote-any --share-printers

# 5. Restart CUPS service
sudo systemctl restart cups
```

---

## 🌐 Step 4: Add the Brother DCP-T236 in CUPS

1. Open your web browser and go to:
   ```
   https://printserver.local:631/admin
   ```
   *(Accept the self-signed SSL security warning).*
2. Click **Add Printer** (log in using your Raspberry Pi credentials).
3. Under **Local Printers**, you will see:
   `Brother DCP-T236 series (Brother DCP-T236 series)`
4. Select it and click **Continue**.
5. Check the box **Share This Printer**.
6. Model Selection:
   - If Brother DCP-T236 is listed under Brother models, select it.
   - Alternatively, select **Generic** -> **Generic IPP Everywhere Printer** or **Raw Queue** / **Brother brlaser generic driver**.
7. Click **Add Printer** and set default media to `A4` or `Letter`.
8. Print a test page from the **Maintenance** drop-down menu!

---

## 📱 Step 5: Wireless Printing from All Devices

### 🍎 iOS (iPhone / iPad) & macOS
No setup required! Because `avahi-daemon` is installed, your iOS device will automatically discover the printer via AirPrint:
- Open any document or photo -> Tap **Share** -> **Print** -> Choose **Brother DCP-T236 @ printserver**.

### 🤖 Android
- Ensure the **Default Print Service** or **Mopria Print Service** app is active in Android Settings -> Connected Devices -> Printing.
- The printer will appear automatically on the local Wi-Fi.

### 🪟 Windows 10 / 11
1. Go to **Settings** -> **Bluetooth & devices** -> **Printers & scanners**.
2. Click **Add device**.
3. Windows will search the network and display `Brother DCP-T236 @ printserver`.
4. Click **Add device**. Windows installs the IPP driver automatically.

