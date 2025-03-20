import logging
import json
import numpy as np
import spacy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from sklearn.feature_extraction.text import TfidfVectorizer
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
import re
from html import unescape

logging.basicConfig(level=logging.INFO)

class IntelligentWebCrawler:
    def __init__(self, url, prompt, headless=True, max_workers=5):
        self.setup_driver(headless)
        self.url = url
        self.links = {}
        self.soup = None
        self.prompt = self.process_prompt(prompt)
        self.relevant_info = ''
        self.relevant_links = {}
        self.visited = []
        self.max_workers = max_workers
        self.fetch(self.url)

    def clean_text(self, text):
        text = unescape(text)  
        text = re.sub(r'\s+', ' ', text)  
        text = text.strip()  
        return text

    def setup_driver(self, headless):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def process_prompt(self, prompt):
        model = spacy.load("en_core_web_sm")
        prompt = model(prompt)
        tokens = [token.text for token in prompt if token.pos_ in ["NOUN", "PROPN"]]
        return ' '.join(tokens)

    def dynamic_threshold(self, size):
        return 1 / np.log1p(size + 1)

    def fetch(self, url, high=False):
        if url[-1] == '/':
            url = url[:-1]
        if url not in self.visited:
            logging.info(f"Fetching URL: {url}")
            self.visited.append(url)
            try:
                self.driver.get(url)
            except Exception as e:
                logging.error(f"Couldn't load the page")
                return
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            self.extract_links()
            self.extract_relevant_info(high)

    def extract_links(self):
        links = self.soup.find_all('a')
        for link in links:
            if link.has_attr('href') and '#' not in link['href']:
                self.links[link.text] = link['href']

    def extract_relevant_info(self, high):
        try:
            text = self.soup.text
            documents = [text, self.prompt]
            tfidf_vectorizer = TfidfVectorizer(stop_words='english').fit_transform(documents)
            cosine_similarities = (tfidf_vectorizer * tfidf_vectorizer.T).toarray()
            similarity_score = cosine_similarities[0][1]
            if similarity_score > 0:
                chunk_size = 100
                chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
                tfidf_vectorizer = TfidfVectorizer(stop_words='english').fit_transform(chunks + [self.prompt])
                scores = (tfidf_vectorizer[:-1] * tfidf_vectorizer[-1].T).toarray()[:, -1]

                relevant_sentences = self.get_relevant_sentences(chunks, scores, high)
                self.relevant_info += ' '.join(relevant_sentences).strip()

                if len(self.links) > 0:
                    self.extract_relevant_links()
        except Exception as e:
            logging.error(f"Error extracting relevant info: {e}")

    def get_relevant_sentences(self, chunks, scores, high):
        try:
            if high:
                if len(scores) > 10:
                    return np.array(chunks)[np.argsort(scores)[-10:]]
                else:
                    return chunks
            else:
                if len(scores) > 5:
                    return np.array(chunks)[np.argsort(scores)[-5:]]
                else:
                    return chunks
        except Exception as e:
            logging.error(f"Error getting relevant sentences: {e}")
            return chunks

    def extract_relevant_links(self):
        try:
            link_texts = list(self.links.keys())
            link_vectorizer = TfidfVectorizer(stop_words='english').fit_transform(link_texts + [self.prompt])
            link_scores = (link_vectorizer[:-1] * link_vectorizer[-1].T).toarray()[:, -1]

            relevant_link_indices = np.argsort(link_scores)[-3:]
            highly_relevant_links = {link_texts[i]: self.links[link_texts[i]] for i in relevant_link_indices if link_scores[i] >= self.dynamic_threshold(len(self.prompt))}
            relevant_links = {link_texts[i]: self.links[link_texts[i]] for i in relevant_link_indices if link_scores[i] > 0 and link_scores[i] < self.dynamic_threshold(len(self.prompt))}

            if self.check_extracted_info():
                return

            if len(highly_relevant_links) > 0:
                for link in highly_relevant_links:
                    if 'mailto' in highly_relevant_links[link]:
                        self.relevant_links['email'] = highly_relevant_links[link][7:]
                    else:
                        self.relevant_links[self.clean_text(link)] = self.url + highly_relevant_links[link]
                for link in highly_relevant_links.items():
                    self.fetch_from_links(link, True)

            if len(relevant_links) > 0:
                for link in relevant_links.items():
                    self.fetch_from_links(link, False)
        except Exception as e:
            logging.error(f"Error extracting relevant links: {e}")

    def fetch_from_links(self, link, high):
        try:
            link_text, link_url = link
            if 'http' in link_url:
                self.fetch(link_url, high)
            elif 'mailto' in link_url or 'maps.google' in link_url:
                return
            else:
                self.fetch(self.url + link_url, high)
        except Exception as e:
            logging.error(f"Error fetching from links: {e}")

    def check_extracted_info(self):
        try:
            info = self.relevant_info.split()
            self.relevant_info = ' '.join(info)
            text = self.relevant_info
            documents = [text, self.prompt]
            tfidf_vectorizer = TfidfVectorizer(stop_words='english').fit_transform(documents)
            cosine_similarities = (tfidf_vectorizer * tfidf_vectorizer.T).toarray()
            similarity_score = cosine_similarities[0][1]
            return similarity_score > 0.5 and len(text) > 300
        except Exception as e:
            logging.error(f"Error checking extracted info: {e}")
            return False

    def save_to_json(self, filename):
        try:
            data = {
                "relevant_info": self.relevant_info,
                "relevant_links": self.relevant_links
            }
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)
        except Exception as e:
            logging.error(f"Error saving to JSON: {e}")

url = "https://www.boston.gov"
prompt = "Fetch me information about Michelle Wu"
crawler = IntelligentWebCrawler(url, prompt)
crawler.save_to_json('output1.json')
crawler.driver.quit()

