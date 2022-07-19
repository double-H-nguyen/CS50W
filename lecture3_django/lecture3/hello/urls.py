from django.urls import path
from . import views

app_name = "hello"
urlpatterns = [
    path("", views.index, name="index"),
    path("page1", views.page1, name="page1"),
    path("<str:name>", views.greet, name="greet")
]