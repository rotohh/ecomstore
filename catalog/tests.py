from django.test import TestCase, Client
#from django.core import urlresolvers
from django.urls import reverse
import http.client
from catalog.models import Category
from catalog.models import Product
	
class NewUserTestCase(TestCase):
	def setUp(self):
		self.client = Client()
	
	def test_view_homepage(self):
		home_url = reverse('catalog_home')
		response = self.client.get(home_url)
		# check that we did get a response
		self.failUnless(response)
		# check that status code of response was success
		self.assertEqual(response.status_code, http.client.OK)
		
	#def test_view_category(self):
	#	category = Category.active.all()#[0]
		#category_url = category.get_absolute_url()
		# get the template_name arg from URL entry
		#url_entry = urlresolvers.resolve(category_url)
		#template_name = url_entry[2]['template_name']
		# test loading of category page
		#response = self.client.get(category_url)
		# test that we got a response
		#self.failUnless(response)
		# test that the HTTP status code was "OK"
		#self.assertEqual(response.status_code, http.client.OK)
		# test that we used the category.html template in response
		#self.assertTemplateUsed(response, "catalog/category.html")
		#self.assertTemplateUsed(response, template_name)
		## test that category page contains category information
		#self.assertContains(response, category.name)
		#self.assertContains(response, category.description)
		
	def test_view_product(self):
		""" test product view loads """
		product = Product.active.all()[0]
		product_url = product.get_absolute_url()
		url_entry = resolve(product_url)
		template_name = url_entry[2]['template_name']
		response = self.client.get(product_url)
		self.failUnless(response)
		self.assertEqual(response.status_code, httplib.OK)
		self.assertTemplateUsed(response, template_name)
		self.assertContains(response, product.name)
		self.assertContains(response, product.description)

class MyTestCase(TestCase):
	#fixtures = ['products', 'categories']
	def test_delete_all(self):
		for p in Product.objects.all():
			p.delete()
		# check that the data
		self.assertEqual(Product.objects.all().count(),0)
	
	def test_products_exist(self):
		self.assertTrue(Product.objects.all().count() > 0)
		
class ActiveProductManagerTestCase(TestCase):
	def setUp(self):
		self.client = Client()
	def test_inactive_product_returns_404(self):
		""" test that inactive product returns a 404 error """
		inactive_product = Product.objects.filter(is_active=False)[0]
		inactive_product_url = inactive_product.get_absolute_url()
		# load the template file used to render the product page
		url_entry = resolve(inactive_product_url)
		template_name = url_entry[2]['template_name']
		# load the name of the default django 404 template file
		django_404_template = page_not_found.func_defaults[0]
		response = self.client.get(inactive_product_url)
		self.assertTemplateUsed(response, django_404_template)
		self.assertTemplateNotUsed(response, template_name)
		
from decimal import Decimal

class ProductTestCase(TestCase):
	def setUp(self):
		self.product = Product.active.all()[0]
		self.product.price = Decimal('199.99')
		self.product.save()
		self.client = Client()
	def test_sale_price(self):
		self.product.old_price = Decimal('220.00')
		self.product.save()
		self.failIfEqual(self.product.sale_price, None)
		self.assertEqual(self.product.sale_price, self.product.price)
	def test_no_sale_price(self):
		self.product.old_price = Decimal('0.00')
		self.product.save()
		self.failUnlessEqual(self.product.sale_price, None)
		
	def test_permalink(self):
		url = self.product.get_absolute_url()
		response = self.client.get(url)
		self.failUnless(response)
		self.assertEqual(response.status_code, httplib.OK)
	def test_unicode(self):
		self.assertEqual(self.product.__unicode__(), self.product.name)
		
class CategoryTestCase(TestCase):
	def setUp(self):
		self.category = Category.active.all()[0]
		self.client = Client()
	def test_permalink(self):
		url = self.category.get_absolute_url()
		response = self.client.get(url)
		self.failUnless(response)
		self.failUnlessEqual(response.status_code, httplib.OK)
	def test_unicode(self):
		self.assertEqual(self.category.__unicode__(), self.category.name)
		
from catalog.models import ProductReview, Product
from django.db import IntegrityError
from django.contrib.auth.models import User

class ProductReviewTestCase(TestCase):
	def test_orphaned_product_review(self):
		pr = ProductReview()
		self.assertRaises(IntegrityError, pr.save)
		
	def test_product_review_defaults(self):
		user = User.objects.all()[0]
		product = Product.active.all()[0]
		pr = ProductReview(user=user, product=product)
		pr.save()
		for field in pr._meta.fields:
		if field.has_default():
		self.assertEqual(pr.__dict__[field.name], field.default)