from django.conf.urls import *
from marketing.sitemap import SITEMAPS
from marketing import views as marketing_views

urlpatterns = [
	
	url(r'^$', marketing_views.robots, { 'template_name': 'cart/cart.html' }, name='robots'),
	url(r'^google_base\.xml$', 'google_base'),

] 
urlpatterns += patterns('',
	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': SITEMAPS }),
)