from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	username = models.OneToOneField(User, on_delete = models.CASCADE)
	
	def __str__(self):
		return str(self.username)
		
class Product(models.Model):
	CATEGORY_CHOICES = [
		('men','men'),
		('female','female'),
		('bag','bag'),
		('shoes','shoes'),
		('watch','watch'),
	]
	name = models.CharField(max_length = 500)
	image = models.ImageField()
	price = models.FloatField()
	category = models.CharField(max_length = 100, choices = CATEGORY_CHOICES)
	description = models.CharField(max_length = 500, null = True, blank = True )
	active = models.BooleanField(default = False)

	def __str__(self):
		return self.name
	

	@property
	def imageUrl(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Description(models.Model):
	product=models.ForeignKey(Product, on_delete = models.CASCADE, related_name="des")
	desc=models.CharField(max_length = 500)

	def __str__(self):
		return self.desc

class Wishlist(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank =True)
	guest = models.BooleanField(default = False)
	product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True, blank = True)
	quantity = models.IntegerField(default = 0)
	date = models.DateTimeField(auto_now_add = True, null = True, blank = True)

	def __str__(self):
		return str(self.product)


class Orderitem(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank =True)
	guest = models.BooleanField(default = False)
	product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
	name = models.CharField(max_length = 500, null = True, blank = True)
	date_added = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return str(self.product)

	def get_total_price(self):
		total_items = self.cart_set.all()
		total = sum([item.get_quantity_amount for item in total_items])
		return total

class Cart(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank =True)
	guest = models.BooleanField(default = False)
	product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
	orderitem = models.ForeignKey(Orderitem, on_delete = models.SET_NULL, null = True)
	quantity = models.IntegerField(default = 1)
	size = models.CharField(max_length = 500 , null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add = True)


	def __str__(self):
		return str(self.product)

	@property	
	def get_quantity_amount(self):
		price_quantity =  self.product.price * self.quantity 
		return price_quantity

	
class Shipping(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank =True)
	guest = models.BooleanField(default = False)
	cart = models.ForeignKey(Cart, on_delete = models.SET_NULL, null = True, blank =True)
	country = models.CharField(max_length = 500)
	address = models.CharField(max_length = 500)
	state = models.CharField(max_length = 500)
	postalcode = models.CharField(max_length = 500)
	card_name = models.CharField(max_length = 500)
	card_number = models.CharField(max_length = 500)
	expires = models.DateTimeField()
	date_added = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.country
