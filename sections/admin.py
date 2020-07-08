from django.contrib import admin
from .models import *
# Register your models here.
class DescriptionInline(admin.TabularInline):
	model=Description
	extra=5

class ProductAdmin(admin.ModelAdmin):
	inlines=[DescriptionInline]
	
admin.site.register(Product,ProductAdmin)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Orderitem)
admin.site.register(Customer)
admin.site.register(Shipping)