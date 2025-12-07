from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("add/", views.add_student, name="add"),
    path("edit/<int:id>/", views.edit_student, name="edit"),
    path("delete/<int:id>/", views.delete_student, name="delete"),

    # History
    path("history/", views.history, name="history"),
    path("restore/<int:id>/", views.restore_student, name="restore"),
    path("permanent_delete/<int:id>/", views.permanent_delete, name="permanent_delete"),
]
