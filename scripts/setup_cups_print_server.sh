#!/usr/bin/env bash
# ==============================================================================
# Brother DCP-T236 Raspberry Pi Print Server (CUPS + AirPrint) Auto-Installer
# ==============================================================================
# Usage:
#   chmod +x setup_cups_print_server.sh
#   sudo ./setup_cups_print_server.sh
# ==============================================================================

set -euo pipefail

echo "=========================================================="
echo " Starting Brother DCP-T236 CUPS Print Server Installation"
echo "=========================================================="

if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run as root (use: sudo ./setup_cups_print_server.sh)"
  exit 1
fi

CURRENT_USER="${SUDO_USER:-pi}"
echo "[+] Target user for lpadmin permissions: ${CURRENT_USER}"

echo "[+] Updating apt repositories..."
apt-get update -y

echo "[+] Installing CUPS, print filters, Brother brlaser driver, and Avahi..."
apt-get install -y \
  cups \
  cups-client \
  cups-filters \
  printer-driver-brlaser \
  printer-driver-all \
  foomatic-db-compressed-ppds \
  avahi-daemon \
  avahi-discover \
  libnss-mdns \
  sane \
  sane-utils \
  usbutils

echo "[+] Adding ${CURRENT_USER} to 'lpadmin' group..."
usermod -a -G lpadmin "${CURRENT_USER}"

echo "[+] Enabling remote web administration on CUPS (port 631)..."
cupsctl --remote-admin --remote-any --share-printers

echo "[+] Enabling and restarting services..."
systemctl enable cups
systemctl restart cups
systemctl enable avahi-daemon
systemctl restart avahi-daemon

# Detect connected Brother printer
echo "[+] Checking for USB-connected printer..."
if lsusb | grep -i "Brother"; then
  echo "[✓] Brother printer detected on USB!"
else
  echo "[!] Brother printer not detected yet. Ensure USB-A to USB-B cable is securely plugged in."
fi

IP_ADDR=$(hostname -I | awk '{print $1}')

echo "=========================================================="
echo " Installation Complete!"
echo "=========================================================="
echo " Web Admin Console: https://${IP_ADDR}:631/admin"
echo " Local Network URL: https://$(hostname).local:631/admin"
echo " Login Username:    ${CURRENT_USER}"
echo " Next Step:         Open the web console, click 'Add Printer',"
echo "                    select Brother DCP-T236, and check 'Share'."
echo "=========================================================="

