from myapp import stock_api
from myapp.models import Notification
import time


class Notifications:

    def __init__(self, symbol):
        self.symbol = symbol
    
    def save_notification(self, stock_symbol, message):

        notification = Notification()
        notification.stock_id = stock_symbol
        notification.message = message
        notification.read = False
        notification.save()

    def check_stock_price(self):
        #testing notification system 
    

        data = stock_api.get_stock_info(self.symbol)
        latest_price = int(data['latestPrice'])
        previous_close = int(data['previousClose'])

        difference = round(abs(((previous_close - latest_price)  / previous_close) * 100), 2)
        
        if previous_close > latest_price:
            message = self.symbol + " Stock's price decreased by " + str(difference) + " %"
            self.save_notification(self.symbol, message)

        elif previous_close < latest_price:
            message = self.symbol + " Stock's price increased by " + str(difference) + " %"
            self.save_notification(self.symbol, message)
            
            
            
            
        




	
	

	