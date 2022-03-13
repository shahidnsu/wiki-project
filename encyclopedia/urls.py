from django.urls import path

from . import views
app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entrypage, name="entrypage"),
    path("search", views.search, name="search"),
    path("newentry", views.newentry, name="newentry"),
    path("edit/<str:title>", views.editpage, name ="editpage"),
    path("random_title", views.random_title, name="random_title")
    
    
    
]
