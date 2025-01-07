import requests
from bs4 import BeautifulSoup
import threading
import queue

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.valid_proxies = []

    def fetch_proxies(self):
        url = 'https://www.wongnai.com/_api/businesses.json?_v=6.126&locale=th&regions=9681&categoryGroupId=9&rerank=false&domain=1&featured=true&featuredSize=2&page.size=1&wref=sr'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", {"class": "spy1xx"})
        if table:
            for row in table.find_all("tr")[2:]:
                cols = row.find_all("td")
                if cols and len(cols) > 1:
                    ip_port = cols[0].text.split()[0]
                    self.proxies.append(ip_port)
        else:
            print("Proxy list table not found.")
        return self.proxies

    def save_proxies(self, filename="proxy_list.txt"):
        with open(filename, 'w') as file:
            for proxy in self.valid_proxies:
                file.write(f"{proxy}\n")

    def validate_proxy(self, proxy, q):
        try:
            response = requests.get("http://ipinfo.io/json", proxies={"http": proxy, "https": proxy}, timeout=5)
            if response.status_code == 200:
                self.valid_proxies.append(proxy)
        except:
            pass
        q.get()
        q.task_done()

    def validate_proxies(self):
        q = queue.Queue()
        for proxy in self.proxies:
            q.put(proxy)
            threading.Thread(target=self.validate_proxy, args=(proxy, q)).start()
        q.join()
        return self.valid_proxies

if __name__ == "__main__":
    manager = ProxyManager()
    proxies = manager.fetch_proxies()
    if proxies:
        valid_proxies = manager.validate_proxies()
        if valid_proxies:
            manager.save_proxies()
            print(f"Saved {len(valid_proxies)} valid proxies to proxy_list.txt")
        else:
            print("No valid proxies found.")
    else:
        print("No proxies found.")