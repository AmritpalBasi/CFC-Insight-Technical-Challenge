# CFC Insight Technical Challenge
'''
Instructions : 
The Challenge
Produce a program that:
    1. Scrape the index webpage hosted at `cfcunderwriting.com`
    2. Writes a list of *all externally loaded resources* (e.g. images/scripts/fonts not hosted
    on cfcunderwriting.com) to a JSON output file.
    3. Enumerates the page's hyperlinks and identifies the location of the "Privacy Policy"
    page
    4. Use the privacy policy URL identified in step 3 and scrape the pages content.
    Produce a case-insensitive word frequency count for all of the visible text on the page. Your frequency count should also be written to a JSON output file..
'''

# Importing Modules

# scraping modules
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# type hint module
from typing import List, Tuple, Dict

# data manipulation modules
import json
import re
from collections import Counter


# TASK 1 FUNCTIONS : Scrape all Externally Loaded Resources


def scrape_page(url: str) -> str:
    '''
    Scrape the contents of a given URL and returns contents as a string

        Parameters:
            url (str) : The URL of the webpage to be scraped

        Returns: 
            str : The contents of the webpage in a string format

    '''
    # Send a GET request to a given URL and store the response
    response = requests.get(url)

    # Return the response as a string
    return response.text


def is_external_resource(url: str, internal_url: str = "https://www.cfcunderwriting.com/"):
    '''
    Checks if a given URL is external.

        Parameters: 
            url (str) : The URL to check 
            internal_url (url) : The internal URL to be compared. For this task the default value is: "https://www.cfcunderwriting.com/"

        Returns: 
            bool : Returns True is URL provided is an external resource
    '''
    # Storing the network location for both arguments
    parsed_url_location = urlparse(url).netloc
    parsed_internal_url_location = urlparse(internal_url).netloc

    # Returning a bool based on if the resource is external
    return parsed_url_location != parsed_internal_url_location


def extract_external_resources(internal_url: str = "https://www.cfcunderwriting.com/") -> List[str]:
    '''
    Extract all external resources for a given URL and return as a list

        Parameters:
            url (str) : The URL to the webpage for all external resources to be extracted. Default value is : = "https://www.cfcunderwriting.com/"

        Returns :
            List[Str] : List of all external resources in the webpage
    '''

    # initialise an empty list to store external resources
    external_resources = []

    # scrape webpage and instantiate a BeautifulSoap Class to obtain tags
    web_page = scrape_page(internal_url)
    soup = BeautifulSoup(web_page, 'html.parser')

    # iterate through all tags in 'soup'
    for tag in soup.find_all(src=True):
        # convert each tag into a link
        link = tag['src']
        # verify if network location of link is different to internal link
        if is_external_resource(link, internal_url):
            external_resources.append(link)

    return external_resources


def export_to_json(obj: object, output_name: str = 'json_output') -> None:
    '''
    converts a list object into a JSON file and outputs the file in the current directory 

        Parameters:
            obj [Object] : Python object to be exported into JSON
            output_name [str] : The name of the file to be exported. Default value is 'json_output'

        Returns: 
            None : JSON file exported in current directory 
    '''

    # Open the .json file in write mode
    with open(f'{output_name}.json', 'w') as json_file:
        # Export list as json file
        json.dump(obj, json_file)


# TASK 2 FUNCTIONS : Scraping the Private Policy page

def find_url(phrase_to_find: str = 'Privacy', url: str = "https://www.cfcunderwriting.com/") -> str:
    '''
    Finds the URL containing the specified phrase on a given webpage.

        Parameters:
            phrase_to_find [str] : Phrase to search for on a given web page. The default value is "Privacy" as this tasks asks us to find the private policy page 
            url [str] : the webpage which will be searched for a given phrase

        Returns:
            str : containing the URL of a given phrase
    '''

    url_from_phrase = None

    # scrape webpage and instantiate a BeautifulSoap Class to obtain Tags
    web_page = scrape_page(url)
    soup = BeautifulSoup(web_page, 'html.parser')

    # Iterate through links in 'soap'
    for link in soup.find_all('a', href=True):
        href = link['href']
        # check if phrase matches href
        if phrase_to_find.lower() in href.lower():
            url_from_phrase = urljoin(url, href)

            # stop loop if phrase has been found
            break

    # Raise an Exception if the URL can not be found
    if url_from_phrase is None:
        raise Exception(f"{url_from_phrase} URL not found.")

    return url_from_phrase


def page_word_count(url: str) -> dict:
    '''
    Counts all case-insensitive words on a given webpage and returns result in a dictionary

        Parameters:
            url [str] : the URL of the webpage which the word count will be performed on

        Returns:
            dict : containing the case-insensitive word and frequency
    '''

    # scrape webpage and instantiate a BeautifulSoap Class to obtain Tags
    web_page = scrape_page(url)
    soup = BeautifulSoup(web_page, 'html.parser')

    # convert soup into string so that it can be used by the regular expression module
    soup_str = str(soup)

    # obtain and clean text from webpage
    text = re.sub('<[^<]+?>', ' ', soup_str).strip().lower()

    # create a list of unique case-insensitive words
    words = re.findall(r'\b\w+\b', text)

    # store frequency of words in Counter object
    word_frequency = Counter(words)

    # return word frequency as dictionary
    return dict(word_frequency)

# Carrying Out Final Analysis
# I have written out the default arguments in these functions just to showcase that any url can be provided


# Extract all external resources
external_resources = extract_external_resources(
    internal_url="https://www.cfcunderwriting.com/")

# export external resources as a JSON file in working directory
export_to_json(obj=external_resources, output_name='external_resources')

# Find the privacy policy page
privacy_policy_url = find_url(
    phrase_to_find='privacy', url="https://www.cfcunderwriting.com/")

# Get a word count of the privacy page
privacy_policy_word_count = page_word_count(privacy_policy_url)

# export the privacy policy word count as a JSON file to current working directory
export_to_json(obj=privacy_policy_word_count,
               output_name='privacy_policy_word_count')
