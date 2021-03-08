from msci_esg.ratefinder import ESGRateFinder

ratefinder = ESGRateFinder()
response = ratefinder.get_esg_rating(
    symbol="TSLA",
    js_timeout=5
)
cat = ratefinder.get_esg_category(rating="a")
print(cat)
print(response)
