from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field, user_username
from finances.models import Bank
# Create your models here.
# dev
class UserRank(models.Model):
    user_rank = models.CharField(max_length=255)

class User(AbstractUser):
    nickname = models.CharField(max_length=255)
    birth_date = models.DateField()
    user_monthly_income = models.BigIntegerField(default=0)
    user_monthly_expenses = models.BigIntegerField(default=0)
    user_point = models.BigIntegerField(default=0)
    rank = models.ForeignKey(UserRank, on_delete=models.CASCADE, default = 1)
    # 마이페이지
    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True, blank=True)

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        birth_date = data.get("birth_date")
        user_monthly_income = data.get("user_monthly_income")
        user_monthly_expenses = data.get("user_monthly_expenses")
        nickname = data.get("nickname")
        bank = data.get("bank")
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if nickname:
            user_field(user, "nickname", nickname)
        if birth_date:
            user_field(user, "birth_date", str(birth_date))
        if user_monthly_income:
            user_field(user, "user_monthly_income", str(user_monthly_income))
        if user_monthly_expenses:
            user_field(user, "user_monthly_expenses", str(user_monthly_expenses))
        if "password1" in data:
            user.set_password(data["password1"])
        if bank:
            try:
                bank_instance = Bank.objects.get(pk=bank)  # Bank 인스턴스 가져오기
                user.bank = bank_instance
            except Bank.DoesNotExist:
                raise ValueError("Invalid bank ID")
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user
    