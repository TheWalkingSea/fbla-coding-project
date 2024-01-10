from django.db import models

class Contact(models.Model):
    name = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
