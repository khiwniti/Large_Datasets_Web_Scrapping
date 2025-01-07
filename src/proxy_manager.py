import requests

url = 'https://www.wongnai.com/_api/businesses.json?_v=6.126&locale=th&regions=9681&categoryGroupId=9&rerank=false&domain=1&featured=true&featuredSize=2&page.size=1&wref=sr'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

class ProxyManager:
    def __init__(self, proxy_file="proxy_list.txt"):
        self.proxies = self.import_proxies(proxy_file)
        self.index = 0
        self.url = self.import_url()

    def import_proxies(self, input_file="proxy_list.txt"):
        try:
            with open(input_file, 'r') as file:
                proxies = [line.strip() for line in file.readlines()]
            print(f"Proxies imported from {input_file}")
            return proxies
        except Exception as e:
            print(f"Error importing proxies: {e}")
            return []

    def export_proxies(self, output_file="exported_proxies.txt"):
        try:
            with open(output_file, 'w') as file:
                for proxy in self.proxies:
                    file.write(proxy + "\n")
            print(f"Proxies exported to {output_file}")
        except Exception as e:
            print(f"Error exporting proxies: {e}")

    def import_url(self, input_file="exported_url.txt"):
        try:
            with open(input_file, 'r') as file:
                url = file.readline().strip()
            print(f"URL imported from {input_file}")
            return url
        except Exception as e:
            print(f"Error importing URL: {e}")
            return None

    def get_proxy(self):
        if not self.proxies:
            return None
        proxy = self.proxies[self.index]
        self.index = (self.index + 1) % len(self.proxies)
        return proxy

    def check_proxy(self, proxy):
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def check_url_status(self):
        try:
            response = requests.get(self.url, headers=headers)
            return response.status_code
        except requests.RequestException as e:
            print(f"Error checking URL status: {e}")
            return None

    def check_target_link(self, target_url):
        for proxy in self.proxies:
            try:
                response = requests.get(target_url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
                if response.status_code == 200:
                    print(f"Proxy {proxy} returned status code 200 for {target_url}")
                else:
                    print(f"Proxy {proxy} returned status code {response.status_code} for {target_url}")
            except requests.RequestException as e:
                print(f"Error with proxy {proxy}: {e}")


