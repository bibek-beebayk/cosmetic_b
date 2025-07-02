from rest_framework import serializers
from .models import Blog, BlogCategory


class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ("title", "slug", "cover_image", "created_at")
        read_only_fields = fields