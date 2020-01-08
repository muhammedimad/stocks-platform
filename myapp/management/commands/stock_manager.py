from myapp.models import Stock
from django.core.management.base import BaseCommand
from myapp import stock_api


# This class is Django's wy to implement managment commands
# You can run it with python manage.py stock_manager
# It will run 'handle' function
class Command(BaseCommand):
	def update_top_stocks(self):
		top_stocks = stock_api._get_top_stocks()

		index = 1
		for stock in top_stocks:
			# This searches for a stock with the given 'symbol' (the primary key)
			# and updates/create it with the values specified in the 'defaults' parameter
			stock_model, created = Stock.objects.update_or_create(symbol=stock['symbol'], defaults={
				'name': stock['companyName'],
				'top_rank': index,
				'price': stock['latestPrice'],
				'change': stock['change'],
				'change_percent': stock['changePercent'],
				'market_cap': stock['marketCap'],
				'primary_exchange': stock['primaryExchange'],
			})
			stock_model.save()
			index += 1

	# ** MAIN TASK **
	# Updates the db according to the IEX console stock API.
	def handle(self, *args, **kwargs):
		self.update_top_stocks()
