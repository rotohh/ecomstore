from django.conf.urls import *
from django.contrib.auth import views as auth_views
from catalog import views as catalog_views
	
urlpatterns = [
	url(r'^$', catalog_views.index, { 'template_name':'catalog/index.html'}, name='catalog_home'),
	url(r'^category/(?P<category_slug>[-\w]+)/$', 
		catalog_views.show_category, {
'template_name':'catalog/category.html'},name='catalog_category'),
	url(r'^product/(?P<product_slug>[-\w]+)/$', 
		catalog_views.show_product, {
'template_name':'catalog/product.html'},name='catalog_product'),
	url(r'^review/product/add/$', catalog_views.add_review, { 'template_name':'catalog/product_review.html'}, name='catalog_review'),
	url(r'^tag/product/add/$', catalog_views.add_tag, {'template_name': 'catalog/tag_link.html'}, name='category_tag'),
	url(r'^tag_cloud/$', catalog_views.tag_cloud, {'template_name': 'catalog/tag_cloud.html'}, name='tag_cloud'),
	url(r'^tag/(?P<tag>[-\w]+)/$', catalog_views.tag, {'template_name': 'catalog/tag.html'}, name='tag'),

	#url(r'^$', catalog_views.get_json_products, { 'template_name':'catalog/index.html'}, name='catalog_json'),
]