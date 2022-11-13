from django.test import TestCase, SimpleTestCase
from .serializers import WidgetSerializer
from .views import WidgetViewSet
from django.urls import reverse, resolve
from rest_framework.test import APIRequestFactory
from .models import Widget

# Create your tests here.
class URLTestCases(TestCase):
    def test_homepage_status_code(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_swagger_status_code(self):
        response = self.client.get('/api/docs/swagger/')
        self.assertEqual(response.status_code,200)
    
    def test_redoc_status_code(self):
        response = self.client.get('/api/docs/redocs/')
        self.assertEqual(response.status_code,200)
    
    def test_spectacular_status_code(self):
        response = self.client.get('/api/docs/spectacular/')
        self.assertEqual(response.status_code,200)

class ViewSetTest(TestCase):
    def test_list_view(self):
        api_request = APIRequestFactory().get("")

        widget1 = Widget.objects.create(name="widget", number_of_parts=3)
        widget2 = Widget.objects.create(name="test", number_of_parts=13)
        widget3 = Widget.objects.create(name="done", number_of_parts=322)

        list_view = WidgetViewSet.as_view({'get': 'list'})
        response = list_view(api_request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data), 1)

    def test_detail_view(self):
        pass

    def test_update_view(self):
        pass 

    def test_delete_view(self):
        pass



    # def test_create_view_set(self):
    #     response = APIRequestFactory().post("", {"name":"widget", "number_of_parts":3} )
    #     create_view = WidgetViewSet.as_view({'post': 'create'})
    #     self.assertEqual(response.status_code, 201)
    #     self.assertTrue(len(response.data), 1)
