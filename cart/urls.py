from django.conf.urls import *
from cart import views as cart_views
from django.contrib.auth import views as auth_views

urlpatterns = [
	
	url(r'^$', cart_views.show_cart, { 'template_name': 'cart/cart.html' }, name='show_cart'),

]