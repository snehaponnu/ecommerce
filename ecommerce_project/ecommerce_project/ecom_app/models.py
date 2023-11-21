from django.contrib.auth.models import User
from django.db import models

# Create your models here.
CATEGORY_CHOICES=(
    ('CR','CURD'),
    ('ML','MILK'),
    ('LS','LASSI'),
    ('PN','PANEER'),
    ('MS','MILK SHAKE'),
    ('GH','GHEE'),
    ('CZ','CHEESE'),
    ('IC','ICE-CREAM'),
    ('KF','KULFI'),
    )

STATE_CHOICES=(
    ('kerala','kerala'),
    ('karnataka','karnataka'),
    ('maharashtra','maharashtra'),
    ('mizhoram','mizhoram'),
    ('thamilnadu','thamilnadu'),
    ('Andra pradesh','Andra pradesh'),
)
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    composition=models.TextField(default='')
    prodapp=models.TextField(default='')
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='product')
    def __str__(self):
        return self.title

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)


STATUS_CHOICE=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('cancel','Cancel'),
    ('pending','pending')

)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICE,default='pending')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Whishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)