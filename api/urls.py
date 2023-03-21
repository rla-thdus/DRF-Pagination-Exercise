from django.urls import path

from api import views


urlpatterns = [
    path('posts-page/', views.PostPageNumberListAPIView.as_view(), name='post-list'),
    path('posts-limit/', views.PostLimitOffsetListAPIView.as_view(), name='post-list'),
    path('posts-cursor/', views.PostCursorListAPIView.as_view(), name='post-list'),
]
