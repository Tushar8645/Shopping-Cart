from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name.title()

    def get_all_category():
        return Category.objects.all()

    def save(self, force_insert=False, force_update=False):
        self.name = self.name.lower()
        super(Category, self).save(force_insert, force_update)


class Product(models.Model):
    name = models.CharField(max_length=80)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(
        max_length=200,
        default="",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="media/products/")

    def __str__(self):
        return self.name

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(pk__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


class Customer(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def full_name(self):
        return self.first_name + " " + self.last_name

    def isExists(self):
        return Customer.objects.filter(email=self.email)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=180, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    date = models.DateField(default=timezone.now())
    status = models.BooleanField(default=False)

    def get_orders_by_customer(customer_id):
        return Order\
            .objects\
            .filter(customer=customer_id)\
            .order_by('-date')
