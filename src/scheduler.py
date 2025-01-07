class Scheduler:
    def __init__(self, scraper, storage):
        self.scraper = scraper
        self.storage = storage

    def schedule_scraping(self, interval, get_proxy):
        import schedule
        import time

        self.get_proxy = get_proxy
        schedule.every(interval).minutes.do(self.run)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def run(self):
        while True:
            proxy = self.get_proxy()
            data = self.scraper.scrape_data(proxy)
            self.storage.upload_file(data)
            time.sleep(1)