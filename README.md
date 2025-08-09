# Simple-WP-Scan

## Description
This is a command-line tool designed for reconnaissance on WordPress websites. It helps to identify active WordPress plugins by parsing the HTML of a given target site, fetches plugin versions from their `readme.txt` files, and optionally searches for known exploits related to these plugins using the `searchsploit` utility.

---

## Features

- **Find Plugins:** Scans the target WordPress site HTML to detect active plugins by extracting plugin names from script source URLs.
- **Fetch Plugin Versions:** Retrieves plugin versions by parsing the `readme.txt` file of each detected plugin.
- **Search Exploits:** Uses the `searchsploit` tool to search for publicly known vulnerabilities related to the identified plugins.
- **Display Plugin Script Source:** Optionally displays the full script source URL from which the plugin was detected.
- **Save Results:** Allows saving the output to a file for later analysis.

---

## Installation

1. Ensure Python 3.x is installed.
2. Install dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```
3. Make sure `searchsploit` is installed and available in your system PATH. It is part of the ExploitDB package:
   ```bash
   sudo apt install exploitdb
   ```

---

## Usage

```bash
python plugin_recon.py --url https://example.com [options]
```

### Options

| Option              | Description                                        |
|---------------------|--------------------------------------------------|
| `--url` or `-u`     | Target WordPress site URL (required)              |
| `--get-plugin` or `-gp` | Scan HTML to find plugins                        |
| `--version-plugin` or `-vp` | Fetch plugin versions from `readme.txt` files  |
| `--searchsploit` or `-se` | Search known exploits for each plugin           |
| `--display-src` or `-d` | Display the full script source URL                |
| `--save` or `-s`    | Save output to a file (default filename: results.txt) |

---

## Examples

- Scan a site for plugins:

  ```bash
  python plugin_recon.py -u https://example.com -gp
  ```

- Scan and fetch plugin versions:

  ```bash
  python plugin_recon.py -u https://example.com -gp -vp
  ```

- Scan, fetch versions, and search for exploits, displaying full source URLs:

  ```bash
  python plugin_recon.py -u https://example.com -gp -vp -se -d
  ```

- Save the output to a file named `plugins.txt`:

  ```bash
  python plugin_recon.py -u https://example.com -gp -s plugins.txt
  ```

---

## Notes

- The tool relies on the structure of WordPress sites and may not detect plugins if the site uses unusual methods or plugins are hidden.
- `searchsploit` must be installed and in your PATH for exploit searching to work.
- Internet connection is required for fetching plugin details and exploit data.

---

## License

This project is released under the MIT License.

## Donation
- **LTC**: ```ltc1qcylc450gq9nr2gspn3x905kvj6jesmnm0fj8p6```
- **BTC**: ```bc1qp52tyf9hykehc4mjexj5ep36asjr0qskywzxtj```
- **ETH**: ```0x73100e9DcA1C591d07AaDE2B61F30c00Dd6da379```

Thank you for using WP-SCAN
