from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("results", views.searching, name="searching"),
    path("random", views.randompage, name="randompage"),
    path("newentry", views.newentry, name="newentry"),
    path("saveentry", views.save_new, name="save_entry")
]
