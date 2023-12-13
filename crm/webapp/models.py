from django.db import models

class Record(models.Model):
    # Campos existentes
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=200)
    country = models.CharField(max_length=150)

    def __str__(self):

        return f"{self.first_name} {self.last_name}"
