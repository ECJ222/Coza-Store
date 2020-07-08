from django.urls import path
from sections import views as v

urlpatterns = [
	path('shop/',v.product,name='shop'),
	path('product-detail/<str:product_name>', v.product_detail , name='product-detail'),
	path('api/', v.ApiCall , name='api'),
	path('apicart/', v.ApiCart , name='apicart'),
	path('shopping-cart/', v.shoppingcart, name="shopping-cart"),
	path('home/', v.Home, name="home"),
	path('product/<str:item>', v.item, name="item"),
	path('search/', v.search, name="search"),
	path('apifeature/', v.feature, name="feature"),
	path('identity/register', v.createuser, name="register"),
	path('identity/login', v.login, name="login"),
	path('logout/', v.logout_view, name="logout"),
	path('checkout/', v.shipping, name="checkout")
]