# Wi-Fi Bruteforce Tool

A Wi-Fi brute-forcing tool developed in Python. This script leverages advanced techniques, including multithreading, to speed up the process of testing passwords against Wi-Fi networks. The tool is intended for educational purposes, network security testing, and research only. **Ensure you have permission to test any network before using this tool**.

## Features

- **Multithreading**: Utilizes multiple threads to speed up password testing.
- **SSID Availability Check**: Checks if the target Wi-Fi network (SSID) is available.
- **Connection Check**: Verifies the connection status after attempting to connect using a password.
- **Progress Tracking**: Saves the last tested password index to resume the process from where it left off.
- **Found Password Logging**: Records successfully found passwords in a file with timestamps.

## Prerequisites

To use this tool, you need the following:

- **Python 3.x** installed on your system.
- **pywifi** library: Install it via pip:
  ```bash
  pip install pywifi
