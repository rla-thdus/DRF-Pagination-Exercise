from django.urls import path

from api import views


urlpatterns = [
    path('posts/', views.PostListAPIView.as_view(), name='post-list'),
]
