from django.conf.urls import url, include
from ecomstore import settings
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^register/$', accounts_views.register,
	{'template_name': 'registration/register.html'},
	'register'),
	url(r'^my_account/$', accounts_views.my_account,
	{'template_name': 'registration/my_account.html'}, 'my_account'),
	url(r'^order_details/(?P<order_id>[-\w]+)/$', accounts_views.order_details,
	{'template_name': 'registration/order_details.html'}, 'order_details'),
	url(r'^order_info//$', accounts_views.order_details,
	{'template_name': 'registration/order_info.html'}, 'order_info'),
	]
urlpatterns += [
	url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html' }, 'login'),
]
#, 'SSL': settings.ENABLE_SSL 
#, 'SSL': settings.ENABLE_SSL	