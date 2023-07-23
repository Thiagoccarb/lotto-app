import contextlib
import undetected_chromedriver as uc
from time import sleep

class SeleniumScraper:
    def __init__(self, url: str) -> None:
        self.url = url
        self._driver = self._initialize_driver()

    def _initialize_driver(self) -> None:
        if not hasattr(self, "_driver"):
            options = uc.ChromeOptions()
            # options.add_argument('-headless')
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")
            options.add_argument("--disable-blink-features=AutomationControlled")

            # Exclude the collection of enable-automation switches 
            self._driver = uc.Chrome(options=options)

    def _cleanup_driver(self) -> None:
        if hasattr(self, "_driver"):
            self._driver.quit()

    @contextlib.contextmanager
    def get_html(self, sleep_time: int) -> str:
        self._driver.get(self.url)

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Host": "httpbin.org",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        }

        self._driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': headers})
        sleep(sleep_time)
        html = self._driver.page_source

        try:
            yield html
        finally:
            self._cleanup_driver()
