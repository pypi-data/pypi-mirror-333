import spacy
from chima_rufus.crawler import IntelligentWebCrawler
from chima_rufus.logger import Logger
import json

class IntelligentAgent:
    def __init__(self, ):
        pass
        
    # Removes stop words and extracts the nouns and pronouns from the prompt
    def _process_prompt(self, prompt):
        model = spacy.load("en_core_web_sm")
        prompt = model(prompt)
        tokens = [token.text for token in prompt if token.pos_ in ["NOUN", "PROPN"]]
        return ' '.join(tokens)
    
    def _check_(self, url, prompt, logger):
        if prompt == None or prompt.strip() == '':
            logger.log_error("No prompt provided")
            return False
        if url == None or url.strip() == '':
            logger.log_error("No URL provided")
            return False
        return True

    def fetch_info(self, url, prompt, filename=None, verbose=False, token_limit=1024):
        logger = Logger(verbose)
        if self._check_(url, prompt, logger):
            crawler = IntelligentWebCrawler(url, verbose, token_limit)
            prompt = self._process_prompt(prompt)
            relevant_info, relevant_links = crawler._fetch(url, prompt)
            self._save_to_json(relevant_info, relevant_links, filename)

    # Saves the extracted info and links to a JSON file
    def _save_to_json(self, relevant_info, relevant_links, filename):
        if filename == None:
            filename = 'output.json'
        try:
            data = {
                "relevant_info": relevant_info,
                "relevant_links": relevant_links
            }
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)
        except Exception as e:
            self.logger._log_error("Error occured when writing the info to JSON", e, bypass=True)