from django.db import models
from accounts.models import User


class Company(models.Model):
    name = models.CharField(max_length=255)
    url = models.TextField()

# Create your models here.
class CardCategory(models.Model):
    card_category = models.CharField(max_length=255)

class OptionCategory(models.Model):
    option_category = models.CharField(max_length=255)

class Card(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=255)
    performance = models.IntegerField()
    card_category = models.ForeignKey(CardCategory, on_delete=models.CASCADE)

class CardOption(models.Model):
    option_category = models.ForeignKey(OptionCategory, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    detail = models.CharField(max_length=255)

class UserCards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)