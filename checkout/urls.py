from django.conf.urls import *
from django.conf.urls import url,include 
from ecomstore import settings
from checkout import views as checkout_views

urlpatterns = [
	url(r'^$', checkout_views.show_checkout, {'template_name': 'checkout/checkout.html' }, name='checkout'),
	url(r'^receipt/$', checkout_views.receipt, {'template_name': 'checkout/receipt.html'}, name='checkout_receipt'),
	]
	
#,'SSL': settings.ENABLE_SSL ,	'SSL': settings.ENABLE_SSL 