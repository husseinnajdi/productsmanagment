from django.db import models

class Product(models.Model):
    product_name=models.CharField(max_length=50)
    product_description=models.CharField(max_length=250)
    product_price=models.IntegerField(max_length=20)
    stock=models.IntegerField(max_length=20)

    def __str__(self):
        return self.product_name
