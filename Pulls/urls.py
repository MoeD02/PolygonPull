from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/process_stock_query", views.process_stock_query, name="process_stock_query"),
]
