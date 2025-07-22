import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

# ANSI escape codes for colors and formatting
GREEN = '\033[92m'
YELLOW_BOLD = '\033[1;33m'
LIGHT_BLUE = '\033[94m'
RED_BOLD = '\033[1;31m'
RESET = '\033[0m'

# Base URL
base_url = "https://www.man7.org/linux/man-pages/"

# Sections to scrape
sections = ["dir_section_1.html", "dir_section_2.html", "dir_section_3.html",
            "dir_section_4.html", "dir_section_5.html", "dir_section_6.html",
            "dir_section_7.html", "dir_section_8.html"]

# Headers to extract
headers_to_extract = ["PROLOG", "NAME", "SYNOPSIS", "DESCRIPTION", "OPTIONS", "OPERANDS", 
                      "STDIN", "INPUT_FILES", "ENVIRONMENT_VARIABLES", "ASYNCHRONOUS_EVENTS",
                      "STDOUT", "STDERR", "OUTPUT_FILES", "EXTENDED_DESCRIPTION", 
                      "EXIT_STATUS", "CONSEQUENCES_OF_ERRORS", "APPLICATION_USAGE", 
                      "EXAMPLES", "RATIONALE", "FUTURE_DIRECTIONS", "SEE_ALSO", "COPYRIGHT"]

# Initialize a list to store man page data
man_pages_data = []

# Define a function to extract specific sections from the man page
def extract_section(soup, section_title):
    normalized_title = section_title.upper()
    header = soup.find('a', id=normalized_title)
    
    if header:
        print(f"{YELLOW_BOLD}Found header: {section_title} at {header.get('id')}{RESET}")
        section_content = []
        for sibling in header.find_parent('h2').find_next_siblings():
            if sibling.name == 'h2':  # Stop at the next header
                break
            if sibling.name in ['pre', 'p', 'div']:  # Consider different tags for content
                section_content.append(sibling.get_text(strip=True))
        return "\n".join(section_content).strip()
    else:
        print(f"{RED_BOLD}Header not found: {section_title}{RESET}")
    return None

def print_all_ids(soup):
    print("Available IDs on the page:")
    ids = [a.get('id') for a in soup.find_all('a', id=True)]
    for id in ids:
        print(f"- {id}")

def save_to_json(data, filename):
    """ Save the given data to a JSON file. """
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Loop through each section
for section in sections:
    section_url = urljoin(base_url, section)
    print(f"{GREEN}Starting to scrape section: {section_url}{RESET}")
    response = requests.get(section_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links to individual man pages
        man_page_links = [urljoin(base_url, a['href']) for a in soup.select('table a')]

        # Parse each man page
        for man_page_url in man_page_links:
            print(f"{GREEN}Scraping URL: {man_page_url}{RESET}")
            man_page_response = requests.get(man_page_url, allow_redirects=True)
            if man_page_response.status_code == 200:
                man_page_soup = BeautifulSoup(man_page_response.content, 'html.parser')

                # Print all IDs for debugging
                print_all_ids(man_page_soup)

                # Extract sections
                man_page_data = {
                    "url": man_page_url
                }

                extracted_sections = []  # To store which sections were successfully scraped
                missing_sections = []  # To store sections that were not found

                for header in headers_to_extract:
                    section_content = extract_section(man_page_soup, header)
                    man_page_data[header.lower().replace(" ", "_")] = section_content
                    if section_content:
                        extracted_sections.append(header)
                        print(f"{YELLOW_BOLD}{header}:{RESET} {LIGHT_BLUE}{section_content}\n{RESET}")
                    else:
                        missing_sections.append(header)

                # Append the man page data to the list
                man_pages_data.append(man_page_data)

                # Save the data to JSON after processing each URL
                save_to_json(man_pages_data, 'man_pages_data.json')

                # Verbose output for extracted and missing sections
                if extracted_sections:
                    print(f"Extracted the following sections from {man_page_url}: {', '.join(extracted_sections)}")
                if missing_sections:
                    print(f"{RED_BOLD}Missing sections from {man_page_url}: {', '.join(missing_sections)}{RESET}")
            else:
                print(f"{RED_BOLD}Failed to scrape URL: {man_page_url} (status code: {man_page_response.status_code}){RESET}")
            print(f"{GREEN}Finished scraping URL: {man_page_url}{RESET}")

    print(f"{GREEN}Finished scraping section: {section_url}{RESET}")

print(f"{GREEN}Man pages data has been saved to 'man_pages_data.json'.{RESET}")
