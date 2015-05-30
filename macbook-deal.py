import urllib2
import json
from bs4 import BeautifulSoup

def currencyConverter(currency_from,currency_to,currency_input):
	yql_base_url = "https://query.yahooapis.com/v1/public/yql"
	yql_query = 'select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20("'+currency_from+currency_to+'")'
	yql_query_url = yql_base_url + "?q=" + yql_query + "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
	try:
		yql_response = urllib2.urlopen(yql_query_url)
		try:
			yql_json = json.loads(yql_response.read())
			currency_output = currency_input * float(yql_json['query']['results']['rate']['Rate'])
			return currency_output
		except (ValueError, KeyError, TypeError):
			return "JSON format error"

	except IOError, e:
		if hasattr(e, 'code'):
			return e.code
		elif hasattr(e, 'reason'):
			return e.reason


def get_price_dollars(price, starting_currency):
    if starting_currency == 'EUR' or starting_currency == 'BRL':
        p = ''.join(c for c in price.split(',')[0] if c.isdigit())
    else:
        p = ''.join(c for c in price.split('.')[0] if c.isdigit())
    p_usd = currencyConverter(starting_currency, 'USD', int(p))
    return p_usd


def main():
    url_base = "http://store.apple.com/{0}/buy-mac/macbook-pro"
    header_format = "---------{0}---------"
    
    countries = {
        'us': ['USA', 'USD'],
        'it': ['Italy', 'EUR'],
        'ca': ['Canada', 'CAD'],
        'br': ['Brazil', 'BRL'],
        'fr': ['France', 'EUR'],
        'hk': ['Hong Kong', 'HKD'],
        'es': ['Spain', 'EUR'],
        'my': ['Malaysia','MYR'],
        'ru': ['Russia', 'RUB'],
        }
    cheapest_country = 'na'
    cheapest_price = 10000000000
    
    for country in countries.keys():
        url = url_base.format(country)
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        price_list = []
        table = soup.find("table",{"class" : "compare ns-buttons"})
        row_titles = table.find("tr",{"class" : "titles"})
        macs = row_titles.findAll("th")
        models = [x.text.strip('\t\n').replace('\n','').replace('\t','') for x in macs ]
        price_tags = table.findAll("span", {"class" : "current_price"})
        prices = [ p.text.strip("\n ") for p in price_tags]
        
        print header_format.format(countries[country][0])
        for pmap in zip(models,prices):
            price_dollar = get_price_dollars(pmap[1], countries[country][1])
            # To be able to print the unicode string in the tuple I split the print
            print pmap[0], pmap[1], '(USD ' + str(price_dollar) + ')'
            if cheapest_price > price_dollar:
                cheapest_price = price_dollar
                cheapest_country = countries[country][0]
    print header_format.format("--")
    print 'BEST DEAL is in {0} where you can get a Macbook for only {1} USD'.format(cheapest_country, cheapest_price)


if __name__ == '__main__':
    main()
