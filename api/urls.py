from django.urls import path, include
from rest_framework import routers

from api import views
from api.views import UserViewSet, PostViewSet, TagViewSet, CategoryViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('posts/<int:pk>/like', views.PostLikeAPIView.as_view(), name='post-detail'),
    path('', include(router.urls)),
]
