# LLM Learnings

I am learning how i can create a LLM based on Linux Man files which I can use with Ollama 
I'm 100% not a developer, and am coming at this from using various AI Chatbots and reading articles.. 

## Project Structure

### Data Collection
To get started, you'll need to crawl the URL and extract relevant information from the HTML pages. Here's a high-level overview of the steps you can take:

1.  **Crawl the URL**: Use a web scraping library (e.g., BeautifulSoup in Python) to fetch the HTML pages from the given URL. You might want to use a recursive approach to crawl all sub-pages that are linked to the main page.
2.  **Extract relevant sections**: Within each HTML page, you'll need to identify the sections that contain information about Linux man files (e.g., NAME, SYNOPSIS, DESCRIPTION, etc.). This can be done using CSS selectors or regular expressions.
3.  **Parse and store the data**: Once you've extracted the relevant sections, use a parsing library (e.g., json) to convert the HTML content into structured data (e.g., JSON objects). Store this data in a suitable format for further processing.

### Build a Model
Create an Ollama-like database that can be queried using natural language questions. 
define a schema and implement an API or query interface.

suggested approach:

1.  **Define the schema**: Design a schema that captures the essential information from the Linux man files (e.g., commands, options, flags). This might involve creating classes or tables for:
    -   Commands
    -   Options
    -   Flags
    -   Description
2.  **Implement an API or query interface**: Use a library like Flask or Django to create a RESTful API that allows you to interact with the database. You can also use a query language like GraphQL or Cypher (for graph databases).

### Train and fine-tune a model

    -   Using natural language processing techniques (e.g., NLTK, spaCy) to parse and analyze user queries
    -   Implementing a question-answering system using knowledge graph-based approaches


## Files
webcrawler.py - python code which crawls https://www.man7.org/linux/man-pages/ and pulls out the various headings then outputs them in a JSON file
man_pages_data.json - resulting json file
