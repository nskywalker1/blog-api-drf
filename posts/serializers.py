import os

from rest_framework import serializers
from django.conf import settings
from rest_framework.fields import SerializerMethodField

from .models import Comment, Post, Category, Tag


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            "description",
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
            "author",
            "image",
            "description",
            "category",
            "tags",
        ]

    def get_url(self, obj):
        return obj.get_api_url()


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
            "description",
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


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name'
        ]


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name'
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "body",
            "created_at",
            "updated_at",
        ]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "body"
        ]
