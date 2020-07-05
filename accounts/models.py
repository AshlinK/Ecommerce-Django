from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=10,null=True)
    email=models.EmailField(max_length=200,null=True)    
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY=(
        ('IN','Indoor'),
        ('O','Outdoor'),
        
    )
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)    
    description=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS=(
        ('P','Pending'),
        ('OFD','Out for delivery'),
        ('D','Delivered'),
    )
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    date_created=models.DateTimeField(auto_now_add=True)
    

