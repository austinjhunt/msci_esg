import requests,json
from selenium import webdriver 
from selenium.webdriver.support.select import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
import warnings 
warnings.filterwarnings("ignore")


# To get ESG Rating, parse HTML for 
# https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool?p_p_id=esgratingsprofile&p_p_lifecycle=20&p_p_state=normal&p_p_mode=view&p_p_resource_id=searchEsgRatingsProfiles&p_p_cacheability=cacheLevelPage&_esgratingsprofile_keywords={SYMBOL}/issuer/{encodedTitle}/{issuerID}

class MSCI_ESG_RateFinder:
    def __init__(self): 
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
                response = requests.get(url).json()[0]
                # returns: {encodedTitle, title, url}(url is issuerid)
            except Exception as e:
                print(e)
                response = {
                    'error': str(e)
                }
        return response 
    def get_esg_rating(self, symbol=None):
        """ Function to get ESG rating information for a given stock
        Params: 
        symbol : the symbol for which you want ESG rating information 
        Returns :
        dict : dictionary of ESG rating information pulled from HTML parsing of MSCI corporate search page 
        """
        # First get the stock MSCI properties 
        props = self.get_stock_msci_properties(symbol=symbol) 

        # Initialize Response Dictionary 
        response = {}

        # Build URL with properties and symbol 
        url = self.MSCI_ESG_URL.format(props['encodedTitle'],props['url'])
       
        # Build Selenium web driver 
        driver = webdriver.PhantomJS()
        driver.get(url)  
        delay = 1
        try:
            data = [div for div in wait(driver, delay).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="esg-rating-paragraph-distr"]'))
                    )]
        except TimeoutException: 
            driver.save_screenshot('screenshot.png')
                
        rating_paragraph = driver.find_element_by_class_name(
            name="esg-rating-paragraph-distr"
        ).text
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

        # build history 
        history = {}
        # Get the history graph
        history_graph = driver.find_element_by_id(
            id_="_esgratingsprofile_esg-rating-history"
        )
        date_labels = history_graph.find_element_by_class_name(
            name="highcharts-xaxis-labels"
        ).find_elements_by_xpath(".//*") # these are the historical rating
        # dates formatted as Month-Day
 
        # Get the rating history (the rating values for the respective dates)
        rating_labels = history_graph.find_element_by_class_name(
            name="highcharts-data-labels"
        ).find_elements_by_class_name("highcharts-label")  
         
        for i in range(len(rating_labels)):  
            history[date_labels[i].text.lower()] = \
                rating_labels[i].text.lower()

        response['history'] = history 

        return response

# Example Code 
rate_finder = MSCI_ESG_RateFinder()
rating_info = rate_finder.get_esg_rating(symbol="TSLA")
print(rating_info)