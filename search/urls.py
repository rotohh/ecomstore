#from django.conf.urls.defaults import *
from django.conf.urls import url, include
from search import views as search_views

urlpatterns = [
	url(r'^results/$',search_views.results,{'template_name': 'search/results.html'}, 'search_results'),
]