import requests
from bs4 import BeautifulSoup

url = 'https://spys.one/free-proxy-list/TH/'
selector = 'spy14'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def fetch_proxies():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        proxy_elements = soup.find_all(class_=selector)
        proxies = []
        for element in proxy_elements:
            proxy = element.text.strip()
            proxies.append(f"http://{proxy}")
        return proxies
    except requests.RequestException as e:
        print(f"Error fetching proxies: {e}")
        return []

def save_proxies(proxies, output_file="exported_proxies.txt"):
    try:
        with open(output_file, 'w') as file:
            for proxy in proxies:
                file.write(proxy + "\n")
        print(f"Proxies exported to {output_file}")
    except Exception as e:
        print(f"Error exporting proxies: {e}")

if __name__ == "__main__":
    proxies = fetch_proxies()
    save_proxies(proxies)
