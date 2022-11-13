from rest_framework import generics
from .models import Widget
from .serializers import WidgetSerializer


class WidgetListView(generics.ListCreateAPIView):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer


class WidgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
