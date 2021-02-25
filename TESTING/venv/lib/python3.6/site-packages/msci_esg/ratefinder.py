import requests
from selenium import webdriver 
from selenium.webdriver.support.select import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
import warnings 
warnings.filterwarnings("ignore")


# To get ESG Rating, parse HTML for 
# https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool?p_p_id=esgratingsprofile&p_p_lifecycle=20&p_p_state=normal&p_p_mode=view&p_p_resource_id=searchEsgRatingsProfiles&p_p_cacheability=cacheLevelPage&_esgratingsprofile_keywords={SYMBOL}/issuer/{encodedTitle}/{issuerID}

class ESGRateFinder:
    def __init__(self,debug=False):
        self.debug = debug 

        self.MSCI_GET_STOCK_ID_URL = (
            "https://www.msci.com/our-solutions/esg-investing/"
            "esg-ratings/esg-ratings-corporate-search-tool?"
            "p_p_id=esgratingsprofile&p_p_lifecycle=2&"
            "p_p_state=normal&p_p_mode=view&p_p_resource_id="
            "searchEsgRatingsProfiles&p_p_cacheability=cacheLevelPage"
            "&_esgratingsprofile_keywords={}" 
        ) # Format with symbol
        self.MSCI_ESG_URL = (
            "https://www.msci.com/our-solutions/esg-investing/"
            "esg-ratings/esg-ratings-corporate-search-tool/"
            "issuer/{}/{}"
        )
         # Format with encodedTitle, IssuerID (pulled from GET_STOCK_ID_URL json response) 
    def get_stock_msci_properties(self, symbol=None):
        response = None 
        if symbol: 
            try:
                url = self.MSCI_GET_STOCK_ID_URL.format(symbol)
                response = requests.get(url)
                if self.debug:
                    print(response.content)
                    print("Getting props as JSON...")
                response = response.json()[0]
                if self.debug:
                    print(response)
                # returns: {encodedTitle, title, url}(url is issuerid)
            except Exception as e:
                print(e)
                response = {
                    'error': str(e)
                }
        return response 
    def get_esg_rating(self, symbol=None, js_timeout=1):
        """ Function to get ESG rating information for a given stock
        Params: 
        symbol : string : the symbol for which you want ESG rating information 
        js_timeout : int : how long should web driver wait for JS to build the page before retrieving content? (seconds)
        Returns :
        dict : dictionary of ESG rating information pulled from HTML parsing of MSCI corporate search page 
        """
        # First get the stock MSCI properties 
        props = self.get_stock_msci_properties(symbol=symbol) 
        if self.debug:
            print(f'Props are: {props}')

        # Initialize Response Dictionary 
        response = {}

        # Build URL with properties and symbol 
        url = self.MSCI_ESG_URL.format(props['encodedTitle'],props['url'])
        if self.debug: 
            print(f'URL built: {url}')
        # Build Selenium web driver 
        driver = webdriver.PhantomJS()
        if self.debug:
            print(f"Built PhantomJS driver {driver}")
        driver.get(url)  
        if self.debug:
            print(f"Got URL") 
        try:
            if self.debug:
                print(f'Waiting for JS to build page to get content...')
            data = [div for div in wait(driver, js_timeout).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="esg-rating-paragraph-distr"]'))
                    )]
            if self.debug:
                print(f'Got content successfully!')
        except TimeoutException: 
            if self.debug:
                print('Timeout reached for WebDriver Wait')
                
        rating_paragraph = driver.find_element_by_class_name(
            name="esg-rating-paragraph-distr"
        ).text
        if self.debug:
            print(f'Rating paragraph: {rating_paragraph}')
        response['rating-paragraph'] = rating_paragraph

        rating_icon = driver.find_element_by_class_name(
            name="ratingdata-company-rating"
        )
        # get its other class name, that will tell the rating
        other_class = rating_icon.get_attribute("class")
        # class that tells rating formatted as esg-rating-circle-<RATING>
        # Build a map of ratings to categories (laggard is bad, leader is good)
        rating_map = {
            'ccc': 'laggard',
            'b': 'laggard',
            'bb': 'average',
            'bbb': 'average',
            'a': 'average',
            'aa': 'leader',
            'aaa': 'leader'
        }
        rating = other_class.split("esg-rating-circle-")[-1].lower()
        response['current'] = {}
        response['current']['esg_rating'] = rating
        response['current']['esg_category'] = rating_map[rating] 
        if self.debug: 
            print(f'ESG rating and category for {symbol}: {rating}/{rating_map[rating]}')

        # build history 
        history = {}
        # Get the history graph
        history_graph = driver.find_element_by_id(
            id_="_esgratingsprofile_esg-rating-history"
        )
        if self.debug:
            print(f"Got history graph HTML element")
        date_labels = history_graph.find_element_by_class_name(
            name="highcharts-xaxis-labels"
        ).find_elements_by_xpath(".//*") # these are the historical rating
        # dates formatted as Month-Day
        if self.debug:
            print(f"Got date labels for rating history!")
 
        # Get the rating history (the rating values for the respective dates)
        rating_labels = history_graph.find_element_by_class_name(
            name="highcharts-data-labels"
        ).find_elements_by_class_name("highcharts-label")  
        if self.debug:
            print(f"Got rating labels for rating history")

        for i in range(len(rating_labels)):  
            history[date_labels[i].text.lower()] = \
                rating_labels[i].text.lower()
        if self.debug:
            print(f"History: {history}")

        response['history'] = history 

        if self.debug:
            print(f"Full response: {response}")

        return response

if __name__ == "__main__": 
    # Example Code 
    rate_finder = ESGRateFinder()
    rating_info = rate_finder.get_esg_rating(symbol="TSLA")
    print(rating_info)