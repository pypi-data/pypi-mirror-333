from sklearn.feature_extraction.text import TfidfVectorizer
from chima_rufus.logger import Logger
import numpy as np
import re
from html import unescape

class IntelligentExtractor:
    def __init__(self, verbose=False):
        self.logger = Logger(verbose)
        self.links = {}
        self.relevant_info = ''
        self.relevant_links = {}

    # Extracts all the useful links inside a web page
    def _extract_links(self, soup):
        extracted_links = {}
        links = soup.find_all('a')
        for link in links:
            if link.has_attr('href') and '#' not in link['href']:
                extracted_links[link.text] = link['href']
        return extracted_links

    # Removes unnecessary symbols from the text
    def _clean_text(self, text):
        text = unescape(text)  
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\\u[0-9a-fA-F]+', ' ', text)
        text = re.sub(r'[^a-zA-Z0-9\s.,:;\'\"!?-]', ' ', text)
        text = ' '.join(text.split())
        text = text.strip()  
        return text

    # Extracts Relevant information from the extracted web data
    def _extract_relevant_info(self, soup, prompt, high):
        try:
            text = soup.text
            documents = [text, prompt]
            tfidf_vectorizer = TfidfVectorizer(stop_words='english').fit_transform(documents)
            cosine_similarities = (tfidf_vectorizer * tfidf_vectorizer.T).toarray()
            similarity_score = cosine_similarities[0][1]
            if similarity_score > 0:
                if high:
                    chunk_size = 500
                else:
                    chunk_size = 100
                chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
                tfidf_vectorizer = TfidfVectorizer(stop_words='english').fit_transform(chunks + [prompt])
                scores = (tfidf_vectorizer[:-1] * tfidf_vectorizer[-1].T).toarray()[:, -1]

                relevant_sentences = self._get_relevant_sentences(chunks, scores, high)
                return self._clean_text(' '.join(relevant_sentences).strip())
        except Exception as e:
            self.logger._log_error(f"Error extracting relevant info: {e}")

    # Helper function to extract relevant chunks from the info
    def _get_relevant_sentences(self, chunks, scores, high):
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
        
    # Returns a threshold based on the length of the prompt
    def _dynamic_threshold(self, size):
        return 1 / np.log1p(size + 1)
        
    # Helper function to extract relevant links from the entire pool of links
    def _extract_relevant_links(self, links, prompt):
        try:
            link_texts = list(links.keys())
            link_vectorizer = TfidfVectorizer(stop_words='english').fit_transform(link_texts + [prompt])
            link_scores = (link_vectorizer[:-1] * link_vectorizer[-1].T).toarray()[:, -1]

            relevant_link_indices = np.argsort(link_scores)[-3:]
            highly_relevant_links = {link_texts[i]: links[link_texts[i]] for i in relevant_link_indices if link_scores[i] >= self._dynamic_threshold(len(prompt))}
            low_relevant_links = {link_texts[i]: links[link_texts[i]] for i in relevant_link_indices if link_scores[i] > 0 and link_scores[i] < self._dynamic_threshold(len(prompt))}
            return highly_relevant_links, low_relevant_links
        except Exception as e:
            self.logger._log_error("Error extracting relevant links:", e)
            return {},{}

    # Calculates the similarity score between the extracted info and the prompt. 
    def _check_extracted_info(self, relevant_info, prompt, token_limit):
        try:
            info = relevant_info.split()
            relevant_info = ' '.join(info)
            text = relevant_info
            documents = [text, prompt]
            tfidf_vectorizer = TfidfVectorizer(stop_words='english').fit_transform(documents)
            cosine_similarities = (tfidf_vectorizer * tfidf_vectorizer.T).toarray()
            similarity_score = cosine_similarities[0][1]
            return similarity_score > 0.5 and len(text) > token_limit
        except Exception as e:
            if self.log:
                self.logger.log_error("Error checking extracted info:", e)
            return False