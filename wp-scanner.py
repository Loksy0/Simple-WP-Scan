import argparse
import requests
import re
import subprocess
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def get_plugin_names_from_html(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', src=True)
        plugins = {}

        for script in scripts:
            src = script['src']
            match = re.search(r'/wp-content/plugins/([^/]+)/', src)
            if match:
                plugin_name = match.group(1)
                # Jeśli plugin jeszcze nie jest w słowniku, dodajemy go
                if plugin_name not in plugins:
                    plugins[plugin_name] = src

        # Zwracamy listę krotek (plugin_name, src)
        return list(plugins.items())

    except Exception as e:
        return [(f"[!] Error fetching URL: {e}", "")]


def get_plugin_version(url, plugin_name):
    readme_url = urljoin(url, f"/wp-content/plugins/{plugin_name}/readme.txt")
    try:
        resp = requests.get(readme_url, timeout=10)
        if resp.status_code == 200:
            match = re.search(r'Stable tag:\s*([0-9a-zA-Z\.-]+)', resp.text)
            if match:
                return match.group(1)
        return None
    except Exception:
        return None

def search_exploit(plugin_name):
    base_name = plugin_name.split('-')[0]
    try:
        result = subprocess.run(['searchsploit', base_name], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"[!] Error running searchsploit: {e}"

def save_output(lines, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + "\n")
        print(f"\n[+] Results saved to {filename}")
    except Exception as e:
        print(f"[!] Failed to save results: {e}")

def main():
    parser = argparse.ArgumentParser(description="WordPress plugin recon tool")
    parser.add_argument('--url', '-u', required=True, help='Target WordPress site URL (e.g., https://example.com)')
    parser.add_argument('--get-plugin', '-gp', action='store_true', help='Find plugins from HTML')
    parser.add_argument('--version-plugin', '-vp', action='store_true', help='Fetch plugin versions from readme.txt')
    parser.add_argument('--searchsploit', '-se', action='store_true', help='Search for known exploits using searchsploit')
    parser.add_argument('-d', '--display-src', action='store_true', help='Display full src line before searchsploit output')
    parser.add_argument('--save', '-s', nargs='?', const='results.txt', help='Save output to file (default: results.txt)')

    args = parser.parse_args()

    output_lines = []

    if args.get_plugin:
        print(f"[+] Scanning for plugins on {args.url} ...")
        plugins = get_plugin_names_from_html(args.url)
        if not plugins:
            print("[!] No plugins found.")
            return

        print(f"[+] Found {len(plugins)} plugin(s):\n")
        for plugin_name, src in plugins:
            line = plugin_name
            if args.version_plugin:
                version = get_plugin_version(args.url, plugin_name)
                version_str = version if version else "Unknown"
                line += f" | Version: {version_str}"

            # Jeśli jest -d, wyświetlamy src bez względu na searchsploit
            if args.display_src:
                print(f"[src] {src}")
                output_lines.append(f"[src] {src}")

            print(line)
            output_lines.append(line)

            if args.searchsploit:
                exploit_result = search_exploit(plugin_name)
                print(exploit_result)
                output_lines.append(exploit_result)


    if args.save:
        save_output(output_lines, args.save)

if __name__ == "__main__":
    main()
