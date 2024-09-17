from django.urls import path

from . import views
urlpatterns = [
    path("", views.guest_list_create),
    path("guest/<int:pk>",views.get_update_delete_guest)
]
