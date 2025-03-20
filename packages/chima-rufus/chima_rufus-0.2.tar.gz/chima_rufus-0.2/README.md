# IntelligentWebCrawler - Chima Rufus

An intelligent web crawler that can fetch information from a given URL based on a text prompt. It is designed to navigate through dense websites, checking all the nested links to gather relevant data as per the user’s input.

## Features

- **Text Prompt-based Crawling**: Crawl a website based on your specific text prompt.
- **Recursive Navigation**: Navigate through dense websites by checking all the nested links for the required information.
- **Customizable Output**: The fetched data can be stored in a customizable output file.

## Installation

You can install the package using pip:

```bash
pip install chima_rufus
```

## Usage
```bash
from chima_rufus import IntelligentAgent

# Initialize the crawler
agent = IntelligentAgent()
agent.fetch_info(url="https://www.example.com", prompt="Find information about example", filename="info.json", verbose=True, token_limit=1024)

# The crawler will start fetching data from the provided URL based on the prompt and save the fetched info in a JSON file.
```

## Parameters
- **URL**: The URL of the website to crawl
- **prompt**: A text prompt that specifies the information to fetch
- **filename**: (Optional, Default='output.json') Set custom output filename
- **verbose**: (Optional, Default=False) Set True to enable logging
- **token_limit**: (Optional, Default=1024) Set custom token limit for the output

