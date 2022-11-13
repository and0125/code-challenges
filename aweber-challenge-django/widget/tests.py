import unittest
from django.test import TestCase
from rest_framework.test import APIClient

from .serializers import WidgetSerializer
from .views import WidgetListView, WidgetDetailView
from .models import Widget


class ModelTest(TestCase):
    def test_widget_model(self):
        widget = Widget(name="test", number_of_parts=31)
        widget.save()
        assert widget.name == "test"
        assert widget.number_of_parts == 31
        assert widget.created_date
        assert widget.updated_date


class DocsTestCases(TestCase):
    def test_swagger_status_code(self) -> None:
        response = self.client.get("/api/docs/swagger/")
        self.assertEqual(response.status_code, 200)

    def test_redoc_status_code(self) -> None:
        response = self.client.get("/api/docs/redocs/")
        self.assertEqual(response.status_code, 200)

    def test_spectacular_status_code(self) -> None:
        response = self.client.get("/api/docs/spectacular/")
        self.assertEqual(response.status_code, 200)


class EndpointTestCases(TestCase):
    def setUp(self) -> None:
        names = ["Rand Corporation", "E Corp", "Veidt Industries", "Geist Group"]
        number_of_parts = [x + 12 for x in range(3, 7)]
        for name, parts in zip(names, number_of_parts):
            Widget.objects.create(name=name, number_of_parts=parts).save()

        self.client = APIClient()

    def test_list__get(self) -> None:
        widgets = Widget.objects.all()
        assert len(widgets) == 4

        resp = self.client.get("")
        assert resp.status_code == 200
        assert len(resp.data) == 4

    def test_list__post(self) -> None:
        widgets = Widget.objects.all()
        assert len(widgets) == 4

        resp = self.client.post("", {"name": "Post Test", "number_of_parts": 33})
        assert resp.status_code == 201
        assert resp.data["name"] == "Post Test"
        assert resp.data["number_of_parts"] == 33

        widget_added = Widget.objects.all()
        assert len(widget_added) == 5

    def test_detail__get(self) -> None:
        resp = self.client.get("/1")
        assert resp.status_code == 200
        assert resp.data["name"] == "Rand Corporation"
        assert resp.data["number_of_parts"] == 15

    def test_detail__patch_name(self) -> None:
        resp = self.client.patch("/1", {"name": "Ayn Rand Corporation"})
        assert resp.status_code == 200
        assert resp.data["name"] == "Ayn Rand Corporation"
        assert resp.data["number_of_parts"] == 15
        assert resp.data["created_date"]
        assert resp.data["updated_date"]

    def test_detail__patch_number_of_parts(self) -> None:
        resp = self.client.patch("/1", {"number_of_parts": 57})
        assert resp.status_code == 200
        assert resp.data["name"] == "Rand Corporation"
        assert resp.data["number_of_parts"] == 57
        assert resp.data["created_date"]
        assert resp.data["updated_date"]

    def test_detail__delete(self) -> None:
        widgets = Widget.objects.all()
        assert len(widgets) == 4

        resp = self.client.delete("/1")
        print(resp.status_code)
        assert resp.status_code == 204

        widget_added = Widget.objects.all()
        assert len(widget_added) == 3
