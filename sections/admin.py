from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.sites.models import Site

class SiteAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'domain')
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'domain')
    list_display_links = ('name',)
    search_fields = ('name', 'domain')



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
admin.site.register(Site, SiteAdmin)