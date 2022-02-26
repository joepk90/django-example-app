from rest_framework import serializers
from . models import Post


class PostSerializer(serializers.ModelSerializer):

    last_update = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'last_update']
