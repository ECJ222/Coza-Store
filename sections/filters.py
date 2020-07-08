from .models import *
from django import forms
import django_filters

class ProductFilter(django_filters.FilterSet):
	
	price__gt = django_filters.NumberFilter(field_name = 'price', lookup_expr = 'gt', label = '', widget = forms.NumberInput( attrs = {'class': 'min-form click'}))
	price__lt = django_filters.NumberFilter(field_name = 'price', lookup_expr = 'lt', label = '', widget = forms.NumberInput( attrs = {'class': 'max-form click'}))

	class Meta:
		model = Product
		fields = ['price']
		exclude = ['price']