from django.urls import path
from . import views

urlpatterns = [
    # 질문 게시판
    path('help/', views.help_article_list, name='article_list_create'),
    path('help/<int:pk>/', views.help_article_detail, name='article_detail'),

    # 좋아요
    path('help/<int:pk>/like/', views.help_like_toggle, name='article_like_toggle'),

    # 댓글
    path('help/<int:pk>/comments/', views.help_comment_list_create, name='comment_list_create'),
    path('help/comments/<int:pk>/', views.help_comment_detail, name='comment_detail'),

    # 메인 페이지
    path('hot-articles/', views.hot_articles, name='hot-articles')
]
