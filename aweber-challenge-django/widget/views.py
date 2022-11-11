from rest_framework import viewsets
from .models import Widget
from .serializers import WidgetSerializer

# Create your views here.


class WidgetViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing widget objects.
    """

    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
