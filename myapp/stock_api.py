import requests

# Sandbox API - FOR TESTING
BASE_URL = 'https://sandbox.iexapis.com'
PUBLIC_TOKEN = 'Tpk_c818732500c24764801eb121fa658bb6'

# Real API - FOR PRODUCTION
# YOU NEED TO CREATE AN ACCOUNT TO RECEIVE YOUR OWN API KEYS (its free)
# BASE_URL = '<MAKE_AN_ACCOUNT>'
# PUBLIC_TOKEN = '<MAKE_AN_ACCOUNT>'

# For general info for all symbols
# https://cloud.iexapis.com/stable/ref-data/symbols?token=pk_dd07f5a1aaea4a039cfe8118f3d9727a


# For all symbols with prices (*free weight*)
# https://cloud.iexapis.com/stable/tops/last?token=pk_dd07f5a1aaea4a039cfe8118f3d9727a
def _request_data(url, filter='', additional_parameters={}):
	final_url = BASE_URL + url

	query_strings = {
		'token': PUBLIC_TOKEN
	}
	query_strings.update(additional_parameters)

	if filter:
		query_strings['filter'] = filter

	response = requests.get(final_url, params=query_strings)

	if not response.ok:
		raise Exception('Unexpected response: ', response.__dict__)
	return response.json()


def _get_top_stocks():
	return _request_data('/stable/stock/market/list/mostactive',
							  filter='symbol,companyName,latestVolume,change,changePercent,primaryExchange,marketCap,latestPrice,calculationPrice',
							  additional_parameters={'displayPercent': 'true', 'listLimit': '20'})


def get_stock_info(symbol):
	# 'symbol,companyName,marketcap,totalCash,primaryExchange,latestPrice,latestSource,change,changePercent'
	return _request_data('/stable/stock/{symbol}/quote'.format(symbol=symbol),
							  additional_parameters={'displayPercent': 'true'})


def get_stock_historic_prices(symbol, time_range='1m'):
	return _request_data('/stable/stock/{symbol}/chart/{time_range}'.format(symbol=symbol, time_range=time_range))



def get_financial_info(symbol):

	return _request_data('/stable/stock/{symbol}/financials/'.format(symbol=symbol),
							  additional_parameters={'displayPercent': 'true'})


def get_financial_report(symbol):

	return _request_data('/stable/stock/{symbol}/financials/'.format(symbol=symbol),
							  additional_parameters={'displayPercent': 'true'})

def get_currency():
	"""This function returns the currency for a specific stock.
	"""
	
	return _request_data('/beta/ref-data/symbols')