from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from myapp import stock_api
from myapp.models import Stock
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from myapp.models import Comment,FollowedStocks,Notification
from django.template import RequestContext
from django.http import HttpResponseRedirect
from myapp.forms import  EditProfileForm, ProfileForm
from myapp.models import Comment
from myapp.models import Stock
from django import utils
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db.models import Q
from myapp import notifications
import json
from django.views.generic import View
from celery.decorators import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task


def get_notifications_for_user():

	s = []
	followed_stocks = FollowedStocks.objects.filter(user_id='majd')

	for obj in followed_stocks:
		s.append(obj.stock_id)
	
	notifications = Notification.objects.filter(stock_id__in=s,read=0)
	return notifications

# View for the home page - a list of 20 of the most active stocks
def index(request):
	"""This function returns the top 20 most active stocks or returns stocks based on
	the search field

	**Template:**

	:template:'myapp/templates/index.html'

	"""
	notifs = get_notifications_for_user()
	
	if request.GET.get('search'): # this will be GET now      
		search_text = request.GET.get('search') # do some research what it does

		items = Stock.objects.filter(Q(symbol__icontains=search_text)
		| Q(name__icontains=search_text))
		return render(request,"index.html",{'page_title': 'Main', 'data': items ,'notifs': notifs})
	else:
		data = Stock.objects.filter(top_rank__isnull=False).order_by('top_rank')
		return render(request, 'index.html', {'page_title': 'Main', 'data': data ,'notifs': notifs })
	
def single_stock(request, symbol):
	"""Returns stock's info and the related comments for this stock.

	**Template:**

	:template:'myapp/templates/signle_stock.html'
	"""

	with open('myapp/static/currencies.json', 'r') as f:
		currency_json_obj = json.load(f)
    
	data = stock_api.get_stock_info(symbol)
	comments = Comment.objects.filter(stock_id = symbol)

	#Getting stock's currency 
	currency = currency_json_obj[symbol]
	#adding currency key to data
	data['currency'] = currency

	return render(request, 'single_stock.html', {'page_title': 'Stock Page - %s' % symbol, 'data': data, 'comments':comments})

@login_required
def profile(request):
	""" the user's profile view """
	return render(request, 'profile.html')

def register(request):
	""" the registration view of the project for creating users using UI """
	# If post -> register the user and redirect to main page
	if request.method == 'POST':
		username = request.POST.get('username')
		firstname = request.POST.get('firstname')
		lastname = request.POST.get('lastname')
		email = request.POST.get('email')
		password = request.POST.get('password')

		newuser = User.objects.create_user(username=username, email=email, password=password)
		newuser.first_name = firstname
		newuser.last_name = lastname
		newuser.save()
		return redirect('index')
	else:
		# If not post (regular request) -> render register page
		return render(request, 'register.html', {'page_title': 'Register'})

@login_required
def edit_profile(request):
	""" for editing the user's profile(in db) and updating his info depending on the entered values"""
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)  # request.FILES is show the selected image or file

		if form.is_valid() and profile_form.is_valid():
			user_form = form.save()
			custom_form = profile_form.save(False)
			custom_form.user = user_form
			custom_form.save()
			return redirect('profile')
	else:
		form = EditProfileForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
		args = {}
		# args.update(csrf(request))
		args['form'] = form
		args['profile_form'] = profile_form
		return render(request, 'edit_profile.html', args)

def logout_view(request):
	""" log the user out from his account and return him the home page"""
	logout(request)
	return redirect('index')

def single_stock_historic(request, symbol):
	"""
	Returns JSON object for a specific stock.
	"""
	data = stock_api.get_stock_historic_prices(symbol, time_range='1m')
	return JsonResponse({'data': data})

@csrf_protect
def add_stock_comment(request):
	"""This function adds comments to Comments table for a specific stock .

	**Template:**

	:template:'myapp/templates/signle_stock.html'
	"""
	if request.method == 'POST':

		if request.POST.get('name') and request.POST.get('content'):
			comment= Comment()
			comment.author = request.POST.get('name')
			comment.text= request.POST.get('content')
			comment.stock_id = request.POST.get('stock_symbol')
			symbol = request.POST.get('stock_symbol')
			comment.save()

			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# def get_stocks_gueryset(query=None):
# 	queryset = []
# 	queries = query.split(" ")
# 	for q in queries:
# 		stocks = Stock.objects.filter(
# 			Q(symbol__icontains=q),
# 			Q(name__icontains=q)
# 		).distinct()

# 		for stock in stocks:
# 			queryset.append(stock)

# 	return list(set(queryset))


def financial_using_ajax(request):
	return render(request, 'financial2.html', {'page_title': 'Register'})
class CompareView(View):
    def post(self, request):

        symbol1 = request.POST['symbol1']
        symbol2 = request.POST['symbol2']

        stock1 = stock_api.get_financial_report(symbol1)
        stock2 = stock_api.get_financial_report(symbol2)

        return JsonResponse([stock1, stock2])

    def get(self, request):
        return render(request, 'compare.html')