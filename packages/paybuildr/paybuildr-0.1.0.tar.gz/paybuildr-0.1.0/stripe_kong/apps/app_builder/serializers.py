# apps/page_builder/serializers.py
from rest_framework import serializers
from .models import Page

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'content', 'published', 'updated_at']