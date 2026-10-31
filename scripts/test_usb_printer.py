#!/usr/bin/env python3
"""
Brother DCP-T236 USB Diagnostic Tool
Checks whether the Brother DCP-T236 (or other USB printer) is properly enumerated
on the system (Windows or Linux/Raspberry Pi) and displays device descriptors.
"""

import sys
import subprocess
import platform

def check_windows():
    print("[*] Detected Platform: Windows")
    try:
        cmd = ["powershell", "-Command", "Get-PnpDevice -Class 'Printer','USB' -Status OK | Select-Object FriendlyName, InstanceId | Format-Table -AutoSize"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("\n--- Active USB / Printer Devices ---")
        print(res.stdout)
    except Exception as e:
        print(f"[-] Error querying Windows PnP devices: {e}")

def check_linux():
    print("[*] Detected Platform: Linux (Raspberry Pi)")
    try:
        lsusb = subprocess.run(["lsusb"], capture_output=True, text=True)
        print("\n--- lsusb Output ---")
        print(lsusb.stdout)
        
        brother_devices = [line for line in lsusb.stdout.splitlines() if "brother" in line.lower()]
        if brother_devices:
            print("[✓] Found Brother hardware:")
            for dev in brother_devices:
                print(f"    -> {dev}")
        else:
            print("[!] No Brother devices found in lsusb. Check cable and power.")

        # Check lpinfo
        print("\n--- CUPS Detected Devices (lpinfo -v) ---")
        lpinfo = subprocess.run(["lpinfo", "-v"], capture_output=True, text=True)
        print(lpinfo.stdout or "None")

    except Exception as e:
        print(f"[-] Error querying Linux USB/CUPS: {e}")

def main():
    print("=" * 60)
    print(" USB Printer Connectivity & Diagnostic Check")
    print("=" * 60)
    os_name = platform.system()
    if os_name == "Windows":
        check_windows()
    elif os_name == "Linux":
        check_linux()
    else:
        print(f"[*] Platform: {os_name}")

if __name__ == "__main__":
    main()

