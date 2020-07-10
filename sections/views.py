from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import *
from django.http import JsonResponse
from .filters import ProductFilter
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout 
import json

# Create your views here.
filtered_data = ''
u_n = ''
def product(request):
	global filtered_data
	global u_n

	print(filtered_data)

	if u_n != 'AnonymousUser':
		
		orderitem = Orderitem.objects.filter(guest = False)
		
		total = 0
		total_quantity = 0
		#gets total price of Cart items
		for i in orderitem:
			total = total + i.get_total_price()

		cart = Cart.objects.filter(guest = False)
		#gets total quantity of items in the cart
		for i in cart:
			total_quantity += i.quantity

		wish = Wishlist.objects.filter(guest = False)

		fil = ProductFilter(request.GET, queryset=Product.objects.all())
		if request.GET:
			item = fil.qs
		else:
			if filtered_data == "freshness":
				item = Product.objects.all()
			elif filtered_data == "low to high":
				item = Product.objects.all().order_by('price')
			else:
				item = Product.objects.all().order_by('-price')

		
		try:
			user = User.objects.get(username = request.user)
		except:
			user = None

		context = {'product':item , 'wishlist':wish, 'cart':cart, 'orderitem':orderitem, 'total':total, 'total_quantity':total_quantity, 'filter':fil, 'user':user}
	else:
		
		orderitem = Orderitem.objects.filter(guest = True)
		
		total = 0
		total_quantity = 0
		#gets total price of Cart items
		for i in orderitem:
			total = total + i.get_total_price()

		cart = Cart.objects.filter(guest = True)
		#gets total quantity of items in the cart
		for i in cart:
			total_quantity += i.quantity

		wish = Wishlist.objects.filter(guest = True)

		fil = ProductFilter(request.GET, queryset=Product.objects.all())
		if request.GET:
			item = fil.qs
		else:
			if filtered_data == "freshness":
				item = Product.objects.all()
			elif filtered_data == "low to high":
				item = Product.objects.all().order_by('price')
			else:
				item = Product.objects.all().order_by('-price')

		
		try:
			user = User.objects.get(username = request.user)
		except:
			user = None

		context = {'product':item , 'wishlist':wish, 'cart':cart, 'orderitem':orderitem, 'total':total, 'total_quantity':total_quantity, 'filter':fil, 'user':user}

	return render(request,'product1.html',context)

def product_detail(request,product_name):
	global u_n

	if u_n != 'AnonymousUser':
		orderitem = Orderitem.objects.filter(guest = False)
		total = 0
		total_quantity = 0
		#gets total price of Cart items
		for i in orderitem:
			total = total + i.get_total_price()
		
		cart = Cart.objects.filter(guest = False)
		#gets total quantity of items in the cart
		for i in cart:
			total_quantity += i.quantity

		wish = Wishlist.objects.filter(guest = False)


		item = get_object_or_404(Product,name = product_name)
		related_product = Product.objects.filter(category = item.category)
		desc = item.des.all()

		try:
			user = User.objects.get(username = request.user)
		except:
			user = None

		context =	{'product':item,'related' : related_product, 'desc' : desc, 'wishlist':wish, 'cart':cart, 'orderitem':orderitem, 'total':total, 'total_quantity':total_quantity, 'user':user}
	else:
		orderitem = Orderitem.objects.filter(guest = True)
		total = 0
		total_quantity = 0
		#gets total price of Cart items
		for i in orderitem:
			total = total + i.get_total_price()
		
		cart = Cart.objects.filter(guest = True)
		#gets total quantity of items in the cart
		for i in cart:
			total_quantity += i.quantity

		wish = Wishlist.objects.filter(guest = True)


		item = get_object_or_404(Product,name = product_name)
		related_product = Product.objects.filter(category = item.category)
		desc = item.des.all()

		try:
			user = User.objects.get(username = request.user)
		except:
			user = None

		context =	{'product':item,'related' : related_product, 'desc' : desc, 'wishlist':wish, 'cart':cart, 'orderitem':orderitem, 'total':total, 'total_quantity':total_quantity, 'user':user}

	return render(request,'product-detail.html',context)

def ApiCall(request):
	global u_n

	data = json.loads(request.body) #changes json data into python dict
	user_n = data['user']
	u_n = user_n

	if user_n != 'AnonymousUser':
		
		productId = data['productId']
		action = data['action']
		

		try:
			customer = Customer.objects.get(username = User.objects.get(username = user_n))
		except:
			customer_create = Customer.objects.get_or_create(username = User.objects.get(username = user_n))
			customer = Customer.objects.get(username = User.objects.get(username = user_n))

		print(productId,action,user_n)
		if action == 'add':
			product = Product.objects.get(id = productId)
			
			wishlist = Wishlist.objects.get_or_create(customer = customer, guest = False, product = product)
		else:
			removewishlist = Wishlist.objects.get(id = productId) 
			removewishlist.delete()

	else:
		data = json.loads(request.body) #changes json into python dict
		productId = data['productId']
		action = data['action']
		

		print(productId,action)
		if action == 'add':
			product = Product.objects.get(id = productId)

			wishlist = Wishlist.objects.get_or_create(guest = True, product = product)
		else:
			removewishlist = Wishlist.objects.get(id = productId) 
			removewishlist.delete()

	return JsonResponse('added to wishlist...', safe = False)

def ApiCart(request):
	global u_n

	data = json.loads(request.body) #changes json data into python dict
	user_n = data['user']
	u_n = user_n

	if user_n != 'AnonymousUser':
		
		try:
			customer = Customer.objects.get(username = User.objects.get(username = user_n))
		except:
			customer_create = Customer.objects.get_or_create(username = User.objects.get(username = user_n))
			customer = Customer.objects.get(username = User.objects.get(username = user_n))

		try:
			productId = data['productId']
			action = data['action']
			
			if action == 'add':

				size = data['size']
				product = Product.objects.get(id = productId)
				try:

					cart_get = Cart.objects.get(product = product , size = size)
					print(cart_get)
					cart_get.quantity += 1
					cart_get.save()

				except:

					orderitem = Orderitem.objects.get_or_create(customer = customer, guest = False, product = product , name = product.name)
					item = Orderitem.objects.get(name = product.name )
					cart = Cart.objects.get_or_create(customer = customer, guest = False, product = product, orderitem = item, size = size)

			elif action == 'remove':

				cart = Cart.objects.get(id = productId)
				cart.delete()
		except :
			operator = data['operator']
			cartId = data['id']
			if operator == 'plus':

				cart = Cart.objects.get(id = cartId)
				print(cart.product.name)
				cart.quantity +=1
				cart.save()

			elif operator == 'minus':

				 cart = Cart.objects.get(id = cartId)
				 cart.quantity -=1
				 cart.save()

				 if cart.quantity == 0:
				 	cart.delete()
	else:
		data = json.loads(request.body) #changes json data into python dict

		try:
			productId = data['productId']
			action = data['action']
			
			if action == 'add':

				size = data['size']
				product = Product.objects.get(id = productId)
				try:

					cart_get = Cart.objects.get(product = product , size = size)
					print(cart_get)
					cart_get.quantity += 1
					cart_get.save()

				except:

					orderitem = Orderitem.objects.get_or_create(guest = True, product = product , name = product.name)
					item = Orderitem.objects.get(name = product.name )
					cart = Cart.objects.get_or_create(guest = True, product = product, orderitem = item, size = size)

			elif action == 'remove':

				cart = Cart.objects.get(id = productId)
				cart.delete()
		except :
			operator = data['operator']
			cartId = data['id']
			if operator == 'plus':

				cart = Cart.objects.get(id = cartId)
				print(cart.product.name)
				cart.quantity +=1
				cart.save()

			elif operator == 'minus':

				 cart = Cart.objects.get(id = cartId)
				 cart.quantity -=1
				 cart.save()

				 if cart.quantity == 0:
				 	cart.delete()
	

	return JsonResponse('added to cart...', safe = False)

def shoppingcart(request):
	global u_n

	if u_n != 'AnonymousUser':
 		orderitem = Orderitem.objects.filter(guest = False)
 		total = 0
 		total_quantity = 0
 		#gets total price of Cart items
 		for i in orderitem:
 			total = total + i.get_total_price()

 		cart = Cart.objects.filter(guest = False)
 		#gets total quantity of items in the cart
 		for i in cart:
 			total_quantity += i.quantity

 		wish = Wishlist.objects.filter(guest = False)

 		try:
 			user = User.objects.get(username = request.user)
 		except:
 			user = None

 		context = {'cart':cart, 'total':total, 'orderitem':orderitem, 'wish':wish, 'total_quantity':total_quantity, 'user':user}
	else:
 		orderitem = Orderitem.objects.filter(guest = True)
 		total = 0
 		total_quantity = 0
 		#gets total price of Cart items
 		for i in orderitem:
 			total = total + i.get_total_price()

 		cart = Cart.objects.filter(guest = True)
 		#gets total quantity of items in the cart
 		for i in cart:
 			total_quantity += i.quantity

 		wish = Wishlist.objects.filter(guest = True)

 		try:
 			user = User.objects.get(username = request.user)
 		except:
 			user = None

 		context = {'cart':cart, 'total':total, 'orderitem':orderitem, 'wish':wish, 'total_quantity':total_quantity, 'user':user}

	return render(request, 'shoping-cart.html', context)

def Home(request):
	global u_n

	if u_n != 'AnonymousUser':
		orderitem = Orderitem.objects.filter(guest = False)
		
		total = 0
		total_quantity = 0
		#gets total price of Cart items
		for i in orderitem:
			total = total + i.get_total_price()

		cart = Cart.objects.filter(guest = False)
		#gets total quantity of items in the cart
		for i in cart:
			total_quantity += i.quantity

		wish = Wishlist.objects.filter(guest = False)

		try:
			user = User.objects.get(username = request.user)
		except:
			user = None

		context = {'wishlist':wish, 'cart':cart, 'orderitem':orderitem, 'total':total, 'total_quantity':total_quantity, 'user':user}
	else:
		orderitem = Orderitem.objects.filter(guest = True)
		
		total = 0
		total_quantity = 0
		#gets total price of Cart items
		for i in orderitem:
			total = total + i.get_total_price()

		cart = Cart.objects.filter(guest = True)
		#gets total quantity of items in the cart
		for i in cart:
			total_quantity += i.quantity

		wish = Wishlist.objects.filter(guest = True)

		try:
			user = User.objects.get(username = request.user)
		except:
			user = None

		context = {'wishlist':wish, 'cart':cart, 'orderitem':orderitem, 'total':total, 'total_quantity':total_quantity, 'user':user}

	return render(request, 'index.html', context)

def item(request, item):
	global u_n

	if u_n != 'AnonymousUser':

		itemlist = Product.objects.filter( category = item )

		orderitem = Orderitem.objects.filter(guest = False)
		
		total = 0
		total_quantity = 0
		#gets total price of Cart items
		for i in orderitem:
			total = total + i.get_total_price()

		cart = Cart.objects.filter(guest = False)
		#gets total quantity of items in the cart
		for i in cart:
			total_quantity += i.quantity

		wish = Wishlist.objects.filter(guest = False)
		Category = Product.objects.filter( category = item )[:1]

		try:
			user = User.objects.get(username = request.user)
		except:
			user = None

		context = {'wishlist':wish, 'cart':cart, 'orderitem':orderitem, 'total':total, 'total_quantity':total_quantity, 'item':itemlist, 'category':Category, 'user':user}
	else:
		itemlist = Product.objects.filter( category = item )

		orderitem = Orderitem.objects.filter(guest = True)
		
		total = 0
		total_quantity = 0
		#gets total price of Cart items
		for i in orderitem:
			total = total + i.get_total_price()

		cart = Cart.objects.filter(guest = True)
		#gets total quantity of items in the cart
		for i in cart:
			total_quantity += i.quantity

		wish = Wishlist.objects.filter(guest = True)
		Category = Product.objects.filter( category = item )[:1]

		try:
			user = User.objects.get(username = request.user)
		except:
			user = None

		context = {'wishlist':wish, 'cart':cart, 'orderitem':orderitem, 'total':total, 'total_quantity':total_quantity, 'item':itemlist, 'category':Category, 'user':user}

	return render(request, 'item.html', context)

def search(request):
	global filtered_data
	global u_n
	print(request.GET)
	if u_n != 'AnonymousUser':
		
		searched_word = request.GET.get('search', False)

		
		if filtered_data == "freshness":
				searchitem = Product.objects.filter(
					Q(name__icontains = searched_word) |
					Q(category__icontains = searched_word)
					)
				fil = ProductFilter(request.GET, queryset = searchitem)
				if 'price__gt' in request.GET:
					searchitem = fil.qs
		elif filtered_data == "low to high":
				searchitem = Product.objects.filter(
					Q(name__icontains = searched_word) |
					Q(category__icontains = searched_word)
					).order_by('price')
				fil = ProductFilter(request.GET, queryset = searchitem)
				if 'price__gt' in request.GET:
					searchitem = fil.qs
		else:
				searchitem = Product.objects.filter(
					Q(name__icontains = searched_word) |
					Q(category__icontains = searched_word)
					).order_by('-price')
				fil = ProductFilter(request.GET, queryset = searchitem)
				if 'price__gt' in request.GET:
					searchitem = fil.qs
		

		orderitem = Orderitem.objects.filter(guest = False)
		
		total = 0
		total_quantity = 0
		#gets total price of Cart items
		for i in orderitem:
			total = total + i.get_total_price()

		cart = Cart.objects.filter(guest = False)
		#gets total quantity of items in the cart
		for i in cart:
			total_quantity += i.quantity

		wish = Wishlist.objects.filter(guest = False)

		try:
			user = User.objects.get(username = request.user)
		except:
			user = None

		context = {'wishlist':wish, 'cart':cart, 'orderitem':orderitem, 'total':total, 'total_quantity':total_quantity, 'searchitem':searchitem, 'searched_word':searched_word, 'filter':fil, 'user':user}
	else:
		
		searched_word = request.GET.get('search', False)

		if filtered_data == "freshness":
				searchitem = Product.objects.filter(
					Q(name__icontains = searched_word) |
					Q(category__icontains = searched_word)
					)
				fil = ProductFilter(request.GET, queryset = searchitem)
				if 'price__gt' in request.GET:
					searchitem = fil.qs
					
		elif filtered_data == "low to high":
				searchitem = Product.objects.filter(
					Q(name__icontains = searched_word) |
					Q(category__icontains = searched_word)
					).order_by('price')
				fil = ProductFilter(request.GET, queryset = searchitem)
				if 'price__gt' in request.GET:
					searchitem = fil.qs
		else:
				searchitem = Product.objects.filter(
					Q(name__icontains = searched_word) |
					Q(category__icontains = searched_word)
					).order_by('-price')
				fil = ProductFilter(request.GET, queryset = searchitem)
				if 'price__gt' in request.GET:
					searchitem = fil.qs

		orderitem = Orderitem.objects.filter(guest = True)
		
		total = 0
		total_quantity = 0
		#gets total price of Cart items
		for i in orderitem:
			total = total + i.get_total_price()

		cart = Cart.objects.filter(guest = True)
		#gets total quantity of items in the cart
		for i in cart:
			total_quantity += i.quantity

		wish = Wishlist.objects.filter(guest = True)

		try:
			user = User.objects.get(username = request.user)
		except:
			user = None

		context = {'wishlist':wish, 'cart':cart, 'orderitem':orderitem, 'total':total, 'total_quantity':total_quantity, 'searchitem':searchitem, 'searched_word':searched_word, 'filter':fil, 'user':user}

	return render(request, 'search.html', context)

def feature(request):

	global filtered_data
	data = json.loads(request.body) #changes json data to dict
	filtered_data = data['choice']

	return JsonResponse('collecting data...', safe=False)


def createuser(request):
	if request.method == 'POST':
		try:
			username = request.POST['username']
			print(username)
			password = request.POST['password']
			email = request.POST['email']

			user = User.objects.create_user(username = username, password = password, email = email, is_staff=True, is_superuser=True)
			customer = Customer.objects.create(username = user)
			user_login = authenticate(request, username = username, password = password)
			if user_login.is_authenticated:
				auth_login(request,user_login)
				return redirect('home')
		except:
			pass

	return render(request, 'Signup.html')

def login(request):
	if request.method == 'POST':

		try:

			password = request.POST['password']
			email = request.POST['email']
			user_check = User.objects.get(email = email)

			user_login = authenticate(request, username = user_check.username, password = password)
			if user_login.is_authenticated:
				auth_login(request,user_login)
				return redirect('home')



		except Exception as e:
			user_check = 0
			return render(request, 'Signin.html', {'user_check':user_check})


	return render(request, 'Signin.html')

def logout_view(request):
	#logout user
	logout(request)
	return redirect('home')

def shipping(request):
	global u_n
	print(u_n)
	if request.method == 'POST':
			if request.user.is_authenticated:
				country = request.POST['time']
				postal = request.POST['postcode']
				address = request.POST['address']
				state = request.POST['state']
				account_name = request.POST['accountname']
				account_number = request.POST['accountnumber']
				account_date = request.POST['accountdate']
				user = User.objects.get(username = request.user)
				customer = Customer.objects.get(username = user)
				ship = Shipping.objects.get_or_create(customer = customer, guest = False, cart = Cart.objects.filter(customer = customer)[0], country = country, postalcode = postal, address = address, card_name = account_name, card_number = account_number, expires = account_date, state = state)
			else:
					country = request.POST['country']
					postal = request.POST['postcode']
					address = request.POST['address']
					state = request.POST['state']
					account_name = request.POST['accountname']
					account_number = request.POST['accountnumber']
					account_date = request.POST['accountdate']
					

					ship = Shipping.objects.get_or_create(guest = True, cart = Cart.objects.filter(guest = True)[0], country = country, postalcode = postal, address = address, card_name = account_name, card_number = account_number, expires = account_date, state = state)

	return render(request, 'checkout.html')