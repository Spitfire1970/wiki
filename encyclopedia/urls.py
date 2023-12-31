from django.urls import path

from . import views

urlpatterns = [
    path("home_page", views.index, name="index"),
    path("wiki/<str:name>", views.show_entry, name = "show_entry"),
    path("search_result", views.process_search, name = "search"),
    path("add_page", views.add_page, name = "add"),
    path("random_page", views.random_page, name = "rand"),
    path("edit_page/<str:title>", views.edit_page, name = "edit_page"),
    path("edited_page/<str:name>", views.edited_page, name = "edited")
]
