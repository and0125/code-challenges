from .views import WidgetListView, WidgetDetailView
from django.urls import path

urlpatterns = [
    path("", WidgetListView.as_view(), name="widget-list"),
    path("<int:pk>", WidgetDetailView.as_view(), name="widget-detail"),
]
