from msci_esg.ratefinder import ESGRateFinder

ratefinder = ESGRateFinder()
response = ratefinder.get_esg_rating(
    symbol="AAPL",
    js_timeout=5
)
print(response)