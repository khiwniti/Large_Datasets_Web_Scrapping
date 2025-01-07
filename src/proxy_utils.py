def export_proxies(proxies, output_file="exported_proxies.txt"):
    try:
        with open(output_file, 'w') as file:
            for proxy in proxies:
                file.write(proxy + "\n")
        print(f"Proxies exported to {output_file}")
    except Exception as e:
        print(f"Error exporting proxies: {e}")

def import_proxies(input_file="exported_proxies.txt"):
    try:
        with open(input_file, 'r') as file:
            proxies = [line.strip() for line in file.readlines()]
        print(f"Proxies imported from {input_file}")
        return proxies
    except Exception as e:
        print(f"Error importing proxies: {e}")
        return []
