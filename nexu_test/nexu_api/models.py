from django.db import models

class Models(models.Model):
    name = models.CharField(max_length = 20)
    avg_price = models.IntegerField( )
    brand_name = models.CharField(max_length = 20)
