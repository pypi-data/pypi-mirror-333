from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from chima_rufus.logger import Logger
from chima_rufus.extractor import IntelligentExtractor

#Web Crawler Class
class IntelligentWebCrawler:
    def __init__(self, url, verbose=False, token_limit=1024):
        self.driver = self._setup_driver(headless=True)
        self.extractor = IntelligentExtractor(verbose)
        self.logger = Logger(verbose)
        self.visited = []
        self.relevant_info = ''
        self.relevant_links = {}
        self.url = url
        self.token_limit = token_limit

    # Set ups the selenium driver to run headless
    def _setup_driver(self, headless):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    # Fetches the information from the given URL.
    # If high is True, the function extracts more information from the URL.
    def _fetch(self, url, prompt, high=False):
        if url[-1] == '/':
            url = url[:-1]
        if url not in self.visited:
            self.logger._log_info(f"Fetching URL: {url}")
            self.visited.append(url)
            try:
                self.driver.get(url)
            except Exception as e:
                self.logger._log_error("An error occured while fetching the URL", e, bypass=True)
                return
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            extracted_links = self.extractor._extract_links(soup)
            extracted_info = self.extractor._extract_relevant_info(soup, prompt, high)

            if extracted_info:
                self.relevant_info += extracted_info

            if self.extractor._check_extracted_info(self.relevant_info, prompt, self.token_limit):
                if len(self.relevant_info) > self.token_limit:
                    words = self.relevant_info.split()
                    self.relevant_info = ' '.join(words[:self.token_limit])
                return self.relevant_info, self.relevant_links
            
            high_relevant_links = None
            low_relevant_links = None
            if len(extracted_links) > 0:
                high_relevant_links, low_relevant_links = self.extractor._extract_relevant_links(extracted_links, prompt)

            if high_relevant_links:
                for link in high_relevant_links:
                    if 'mailto' in high_relevant_links[link]:
                        self.relevant_links['email'] = high_relevant_links[link][7:]
                    else:
                        self.relevant_links[self.extractor._clean_text(link)] = url + high_relevant_links[link]

                if len(high_relevant_links) > 0:
                    self._fetch_from_links(url, high_relevant_links, prompt, True)

            if low_relevant_links:
                if len(low_relevant_links) > 0:
                    self._fetch_from_links(url, low_relevant_links, prompt)

            return self.relevant_info, self.relevant_links

    
    # Helper function to fetch relevant info from a list of links
    def _fetch_from_links(self, url, links, prompt, high=False):
        for link in links:
            link_url = links[link]
            if 'http' in link_url:
                self._fetch(link_url, prompt, high)
            elif 'mailto' in link_url or 'maps.google' in link_url:
                continue
            else:
                self._fetch(self.url + link_url, prompt, high)

