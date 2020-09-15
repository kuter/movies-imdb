from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TopCommentSerializer(serializers.Serializer):
    movie = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()
