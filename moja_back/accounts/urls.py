from django.urls import path, include
from . import views

urlpatterns = [
  path('dj-rest-auth/', include('dj_rest_auth.urls')),
  path('dj-rest-auth/registration', include('dj_rest_auth.registration.urls')),
  path('detail/<int:pk>/', views.user_detail),
  path('', views.user_list),
  # 마이페이지
  path('profile/', views.get_user_profile),
  path('profile/update/', views.update_profile)
]
