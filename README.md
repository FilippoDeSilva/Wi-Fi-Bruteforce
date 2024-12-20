
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
  ```

## Usage

### Running the Script

To run the tool, execute the following command in your terminal:

```bash
python wifi_bruteforce.py <SSID> <wordlist_file> --threads <number_of_threads> --start <start_index> --end <end_index>
```

### Arguments:

- `SSID`: The name of the Wi-Fi network you want to test (e.g., "MyWiFi").
- `wordlist_file`: Path to the wordlist (a file containing a list of potential passwords).
- `--threads`: The number of threads to use for the brute-forcing process (default: 4).
- `--start`: Start index in the wordlist (default: 0).
- `--end`: End index in the wordlist (default: None, which means use the entire wordlist).

### Example:

```bash
python wifi_bruteforce.py "MyWiFi" "passwords.txt" --threads 4 --start 0 --end 100
```

This will test the first 100 passwords from the `passwords.txt` file against the `MyWiFi` SSID using 4 threads.

## Disclaimer

**This tool is intended for educational purposes only.**

You are solely responsible for using this tool legally and ethically. You should only use this tool on networks that you own or have explicit permission to test. Unauthorized use on networks without consent is illegal and could lead to severe legal consequences.

By using this tool, you agree to do so at your own risk.

## License

This project is licensed under the **MIT License**.

**MIT License**:

```
MIT License

Copyright (c) [year] [your name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

### Disclaimer:

The use of this tool is strictly limited to educational purposes or for security testing on networks you own or have explicit permission to test. Unauthorized use on networks without permission is illegal and unethical.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request. Contributions are always welcome.

## Acknowledgments

- [pywifi](https://github.com/awkman/pywifi) for the Wi-Fi management and connection handling library.
- Special thanks to anyone who contributed ideas or feedback to make this tool better.

---

**Remember**: Always act responsibly when using this tool. Test only on networks you own or have explicit permission to test. Unauthorized access to networks is illegal.
