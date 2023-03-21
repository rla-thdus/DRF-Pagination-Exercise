from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from api.models import Post
from api.serializers import PostListSerializer

class PostPageNumberPagination(PageNumberPagination):
    page_size = 3


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

