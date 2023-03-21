from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from api.models import Post
from api.serializers import PostListSerializer

class PostPageNumberPagination(PageNumberPagination):
    page_size = 3


class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 4


class PostPageNumberListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination


class PostLimitOffsetListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostLimitOffsetPagination

