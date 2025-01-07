import requests

url = 'https://www.wongnai.com/_api/businesses.json?_v=6.126&locale=th&regions=9681&categoryGroupId=9&rerank=false&domain=1&featured=true&featuredSize=2&page.size=1&wref=sr'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"}

def check_wongnai_status():
    try:
        response = requests.get(url, headers=headers)
        print(f"URL status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error checking URL status: {e}")

if __name__ == "__main__":
    check_wongnai_status()
