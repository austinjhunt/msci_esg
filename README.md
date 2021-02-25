# MSCI ESG (Environment, Social, Governance) Corporate Search Tool Scraper
---
MSCI Inc., is an American finance company headquartered in New York City and serving as a global provider of equity, fixed income, hedge fund stock market indexes, multi-asset portfolio analysis tools and ESG products. It publishes the MSCI BRIC, MSCI World and MSCI EAFE Indexes. 

ESG Risk Ratings provided by MSCI are designed to measure a company's resilience to long-term, industry material environmental, social and governance (ESG) risks. MSCI uses a rules-based methodology to identify industry leaders and laggards according to their exposure to ESG risks and how well they manage those risks relative to peers.

---
## What is it?
This is a simple package that uses Selenium to scrape content from the MSCI.com [ESG (Environment, Social, Governance) Risk Corporate Search Tool](https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool/issuer/tesla-inc/IID000000002594878). 

---
## Why was this created?
ESG risk ratings play an important role in stock market analysis, and previously, the only way of obtaining this data from MSCI was to open the Search Tool in a browser, search for a symbol, and click on one of the autosuggested results. This automates the collection of the important ESG risk rating data, both historical and current, and returns it in JSON format. 
This project was built as a supplemental tool for [StockScope](https://github.com/austinjhunt/stockscope), which is a Django web application in development for providing AI-driven Stock Market querying and alerting capabilities. 

--- 
## How to Use
The following is a sample Python code snippet that uses this package.
```
from msci_esg.ratefinder import ESGRateFinder

# Create an ESGRateFinder object, optionally passing in debug=True for more print statements
ratefinder = ESGRateFinder()

# Call the ratefinder object's get_esg_rating method, passing in the Apple stock symbol and 
# a JS timeout of 5 seconds (this is how long the Selenium web driver should wait for JS to execute 
# before scraping content)
response = ratefinder.get_esg_rating(
    symbol="AAPL",
    js_timeout=5
)
# The response is a dictionary; print it
print(response)
# Will look like: 
# {'rating-paragraph': 'Apple is average among 52 companies in the technology hardware, storage & peripherals industry.', 'current': {'esg_rating': 'bbb', 'esg_category': 'average'}, 'history': {'oct-16': 'a', 'aug-17': 'a', 'sep-18': 'a', 'nov-19': 'a', 'dec-20': 'bbb'}}
```