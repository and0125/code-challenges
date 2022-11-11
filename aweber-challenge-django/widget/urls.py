from .views import WidgetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", WidgetViewSet, basename="widget")
urlpatterns = router.urls
