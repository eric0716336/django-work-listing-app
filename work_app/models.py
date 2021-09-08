from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class jobs(models.Model):
    level_choices = [
        ('E', 'Entry-Level'),
        ('S', 'Senior-Level'),
        ('V', 'VP-Level'),
    ]

    user  = models.ForeignKey(User, on_delete= models.CASCADE,null=False)
    position= models.CharField(max_length=100)
    level= models.CharField(max_length=30 , choices=level_choices)
    salary = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=50)
    contact_email =models.CharField(max_length=50)

    def __str__(self):
        return self.position
    