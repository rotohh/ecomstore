#344
from django.db import models
from django.db.models.signals import post_save, post_delete
from caching.caching import cache_update, cache_evict
import tagging
# Create your models here.

class ActiveCategoryManager(models.Manager):
	def get_query_set(self):
		return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)

class Category(models.Model):
	@property
	def cache_key(self):
		return self.get_absolute_url()
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, unique=True,
		help_text='Unique value for product page URL, created from name.')
	description = models.TextField()
	is_active = models.BooleanField(default=True)
	meta_keywords = models.CharField("Meta Keywords", max_length=255, 
		help_text='Comma-delimited set of SEO keywords for meta tag')
		
	meta_description = models.CharField("Meta Description", max_length=255, 
		help_text='Content for description meta tag')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()
	active = ActiveCategoryManager()
	class Meta:
		db_table = 'categories'
		ordering = ['-created_at']
		verbose_name_plural = 'Categories'
	def __str__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('catalog_category', (), { 'category_slug': self.slug })

class ActiveProductManager(models.Manager):
	def get_query_set(self):
		return super(ActiveProductManager, self).get_query_set().filter(is_active=True)
		
class FeaturedProductManager(models.Manager):
	def all(self):
		return super(FeaturedProductManager, self).all().filter(is_active=True).filter(is_featured=True)
		
class Product(models.Model):
	# Product model class definition here
	#try:
	#	tagging.register(Product)
	#except tagging.AlreadyRegistered:
	#	pass
	@property
	def cache_key(self):
		return self.get_absolute_url()
	name = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(max_length=255, unique=True, 
		help_text='Unique value for product page URL, created from name.')
	brand = models.CharField(max_length=50)
	sku = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=9,decimal_places=2)
	old_price = models.DecimalField(max_digits=9,decimal_places=2, 
		blank=True,default=0.00)
	#image = models.ImageField(upload_to="static/images/products/main")
	image = models.ImageField(upload_to='images/products/main')
	thumbnail = models.ImageField(upload_to='images/products/thumbnails', default='DEFAULT VALUE')
	image_caption = models.CharField(max_length=200, default='DEFAULT VALUE')
	is_active = models.BooleanField(default=True)
	is_bestseller = models.BooleanField(default=False)
	is_featured = models.BooleanField(default=False)
	quantity = models.IntegerField()
	description = models.TextField()
	meta_keywords = models.CharField(max_length=255, 
		help_text='Comma-delimited set of SEO keywords for meta tag')
	meta_description = models.CharField(max_length=255, 
		help_text='Content for description meta tag')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	categories = models.ManyToManyField(Category)
	objects = models.Manager()
	active = ActiveProductManager()
	featured = FeaturedProductManager()
	class Meta:
		db_table = 'products'
		ordering = ['-created_at']
	def __str__(self):
		return self.name
	@models.permalink
	def get_absolute_url(self):
		return ('catalog_product', (), { 'product_slug': self.slug })
	def sale_price(self):
		if self.old_price > self.price:
			return self.price
		else:
			return None
			
	def cross_sells_hybrid(self):
		from checkout.models import Order, OrderItem
		from django.contrib.auth.models import User
		from django.db.models import Q
		orders = Order.objects.filter(orderitem__product=self)
		users = User.objects.filter(order__orderitem__product=self)
		items = OrderItem.objects.filter( Q(order__in=orders) |
		Q(order__user__in=users)
		).exclude(product=self)
		products = Product.active.filter(orderitem__in=items).distinct()
		return products
		
from django.contrib.auth.models import User

class ActiveProductReviewManager(models.Manager):
	def all(self):
		return super(ActiveProductReviewManager, self).all().filter(is_approved=True)

class ProductReview(models.Model):
	RATINGS = ((5,5),(4,4),(3,3),(2,2),(1,1),)
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	title = models.CharField(max_length=50)
	date = models.DateTimeField(auto_now_add=True)
	rating = models.PositiveSmallIntegerField(default=5, choices=RATINGS)
	is_approved = models.BooleanField(default=True)
	content = models.TextField()
	objects = models.Manager()
	approved = ActiveProductReviewManager()
	
post_save.connect(cache_update, sender=Product)
post_delete.connect(cache_evict, sender=Product)
post_save.connect(cache_update, sender=Category)
post_delete.connect(cache_evict, sender=Category)