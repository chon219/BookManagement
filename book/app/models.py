from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    press = models.CharField(max_length=256)
    year = models.CharField(max_length=16)
    username = models.CharField(max_length=256, null=True, blank=True)
    available = models.BooleanField(default=True)

    class Meta:
        db_table = "book"

class Log(models.Model):
    book = models.ForeignKey(Book)
    username = models.CharField(max_length=256)
    datetime = models.DateField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    class Meta:
        db_table = "log"
