from proxy_manager import ProxyManager


def main():
    # Fetch and save proxies
    proxies = fetch_proxies()
    save_proxies(proxies)

    proxy_manager = ProxyManager()
    status_code = proxy_manager.check_url_status()
    if status_code:
        print(f"URL status code: {status_code}")
    else:
        print("Failed to check URL status.")

    # Export proxies to a text file
    proxy_manager.export_proxies()

    # Check target link using proxies
    proxy_manager.check_target_link(url)

if __name__ == "__main__":
    main()
