from django.db import models

class Contracts(models.Model):
    name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100, null=True)
    min_money=models.IntegerField()
    max_money=models.IntegerField()
    percent_for_day=models.FloatField()
    term=models.IntegerField()
    show_to_all = models.BooleanField(default=True)



