from rest_framework import viewsets

from .filters import CommentFilter
from .models import Comment
from .serializers import CommentSerializer, TopCommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_class = CommentFilter


class TopCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.top()
    serializer_class = TopCommentSerializer
    filterset_class = CommentFilter
    http_method_names = ['get']
