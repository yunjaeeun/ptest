from django.urls import path
from . import views

urlpatterns = [
  path('bank/', views.bank_list),
  path('bank/save/', views.save_banks),
  path('product/', views.prdt_list),
  path('product/save/', views.save_prdt),
  path('product/detail/<int:pk>/', views.prdt_detail),
  path('savings/', views.savings_list),
  path('savings/save/', views.save_savings),
  path('savings/detail/<int:pk>/', views.savings_detail),
  path('recommend/', views.recommend),
  path('exchange/', views.get_exchange),
  path('user-product/', views.user_products),
  path('option/<int:pk>/', views.option_detail),
]
