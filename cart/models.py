from django.db import models

# Create your models here.

from django.db import models
from catalog.models import Product

class CartItem(models.Model):
	cart_id = models.CharField(max_length=50)
	date_added = models.DateTimeField(auto_now_add=True)
	quantity = models.IntegerField(default=1)
	product = models.ForeignKey('catalog.Product', unique=False, on_delete = models.PROTECT)

	class Meta:
		db_table = 'cart_items'
		ordering = ['date_added']
	
	#@property
	def total(self):
		return self.quantity * self.product.price
	
	#@property
	def name(self):
		return self.product.name
	
	#@property
	def price(self):
		return self.product.price
	
	#@property
	def get_absolute_url(self):
		return self.product.get_absolute_url()
	
	#@property
	def augment_quantity(self, quantity):
		self.quantity = self.quantity + int(quantity)
		self.save()
