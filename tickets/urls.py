from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import obtain_auth_token

router=DefaultRouter()
router.register("guests",views.guest_viewset)
router.register("movies",views.movie_viewset)
router.register("reservation",views.reservation_viewset)

urlpatterns = [
    path("", views.guest_list_create),
    path("guest/<int:pk>",views.get_update_delete_guest),
    path("guests/",views.CBV_guest),
    path("<int:pk>",views.get_guest),
    path("all_guests",views.mixins_list.as_view()),
    path("get_guest/<int:pk>",views.mixins_pk.as_view()),
    path("all",views.generics_list.as_view()),
    path("getGuest/<int:pk>",views.geneerics_pk.as_view()),
    path("viewset/",include(router.urls)),
    path("search",views.search),
    path("new_reservation",views.new_reservation),
    path("api-auth-token",obtain_auth_token),
]
