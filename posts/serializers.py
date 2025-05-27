import os
from rest_framework import serializers
from django.conf import settings
from rest_framework.reverse import reverse
from .models import Comment, Post, Category, Tag


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            "body",
            "image",
            "tags",
            "category"
        ]

    def validate_title(self, value):
        if len(value) > 255:
            return serializers.ValidationError(
                "Max description is 200 characters"
            )
        return value

    def clean_image(self, value):
        initial_path = value.path
        new_path = settings.MEDIA_ROOT + value.name
        os.rename(initial_path, new_path)
        return value


class PostListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "url",
            "title",
            "body",
            "author",
            "image",
            "category",
            "tags",
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return reverse('posts_api:posts-detail', kwargs={'slug': obj.slug}, request=request)


class PostDetailSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "slug",
            "title",
            "body",
            "body",
            "category",
            "author",
            "image",
            "created_at",
            "updated_at",
            "comments"
        ]

    def get_slug(self, obj):
        return obj.slug

    def get_comments(self, obj):
        qs = Comment.objects.filter(post=obj)
        try:
            serializer = CommentSerializer(qs, many=True)
        except Exception as e:
            print(e)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "body",
            "created_at",
            "updated_at",
        ]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["body"]
