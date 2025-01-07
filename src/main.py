from src.proxy_manager import ProxyManager
from src.proxy_scraper import fetch_proxies, save_proxies
from src.url_utils import export_url

def main():
    # Fetch and save proxies
    proxies = fetch_proxies()
    save_proxies(proxies)

    # Export URL to a text file
    url = 'https://www.wongnai.com/_api/businesses.json?_v=6.126&locale=th&regions=9681&categoryGroupId=9&rerank=false&domain=1&featured=true&featuredSize=2&page.size=1&wref=sr'
    export_url(url)

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
