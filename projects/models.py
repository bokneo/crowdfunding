# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    username = models.ForeignKey(User, models.DO_NOTHING, db_column='id')
    name = models.CharField(primary_key=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    start = models.DateField()
    end = models.DateField()
    image = models.ImageField(upload_to = 'images/')
    pledged = models.DecimalField(max_digits=12, decimal_places=2, blank=True, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, default=0)