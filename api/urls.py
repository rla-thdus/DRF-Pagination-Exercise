from django.urls import path, include
from rest_framework import routers

from api.views import UserViewSet, PostViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
