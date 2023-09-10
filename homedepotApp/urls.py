
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="app_home"),
    path("search/", views.search_by_keyword, name="search_by_keyword"),
    path("product/", views.search_by_product, name="search_by_product"),
    path("product/reviews", views.product_review, name="product_review"),

]
