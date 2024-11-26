from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.card_list),
    path('<int:pk>/', views.card_detail),
    path('recommend/', views.recommend),
    path('user-card/', views.user_card),
    path('best/', views.best_card),
]
