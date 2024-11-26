from django.db import models
from django.conf import settings


# Create your models here.
class Bank(models.Model):
    bank_name = models.CharField(max_length=255)
    bank_code = models.CharField(max_length=255)
    bank_url = models.CharField(max_length=255)

class ProductCategory(models.Model):
    product_category = models.CharField(max_length=255)


class Product(models.Model):
    fin_code = models.CharField(max_length=255)
    prdt_name = models.CharField(max_length=255)
    prdt_code = models.CharField(max_length=255)
    join_way = models.TextField()
    mtrt_int = models.TextField()
    spcl_cnd = models.TextField(null=True, blank=True)
    join_deny = models.CharField(max_length=255)
    join_member = models.TextField()
    etc_note = models.TextField()
    max_limit = models.IntegerField(null=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    product_category = models.ForeignKey(ProductCategory, on_delete = models.CASCADE)

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    rate_type = models.CharField(max_length=255)
    rsrv_type = models.CharField(max_length=255, null=True)
    save_trm = models.IntegerField()
    intr_rate = models.FloatField(null=True)
    max_intr_rate = models.FloatField()

class UserProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Exchange (models.Model):
    cur_unit = models.CharField(max_length=100)
    cur_nm = models.CharField(max_length=100)
    ttb = models.CharField(max_length=100)
    tts = models.CharField(max_length=100)
    deal_bas_r = models.CharField(max_length=100)
    bkpr = models.CharField(max_length=100)
    yy_efee_r = models.CharField(max_length=100)
    ten_dd_efee_r = models.CharField(max_length=100)
    kftc_deal_bas_r = models.CharField(max_length=100)
    kftc_bkpr = models.CharField(max_length=100)