# apps/page_builder/views.py
from rest_framework import viewsets
from .models import Page
from .serializers import PageSerializer

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = 'slug'