import requests
import time

from requests_html import HTML
from recipe_extractor_tools.logger_service import get_logger 

MAX_RETRIES = 5
logger = get_logger(name = "Scraper service")

def load_page(link:str, current_attempts:int = 0, sleep:int = 60) -> HTML:
    """
        Performs a request and returns the page_content as an HTML object if successful. 

        params:
            link(str): The link to be loaded. 
            current_attempts (int): The current number of attempts for the url to be scraped.
            sleep (int): The wait time in seconds before loading the page. This can be used as a way to prevent blockage. (default = 60 seconds)

        returns
            page_content(HTML): The page content as an HTML object.
    """
    
    logger.info(f"Loading url {link}")

    while current_attempts <= MAX_RETRIES:
        # Reduce de risk of being blocked since we are not using a proxy. 
        time.sleep(sleep)
        
        response = requests.get(link)

        if response.status_code == 200:
            logger.info("Request succeeded.")
            page_content = HTML(html=response.text)
            return page_content
        
        else:
            logger.error(f"An error occured while performing the request: status code ({response.status_code}), message ({response.text})")
            current_attempts += 1

    if not page_content:
        raise Exception(f"Could not load page {link}.") 