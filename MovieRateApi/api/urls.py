from django.urls import path, include
from rest_framework import routers
from .views import MovieViewSet, RatingViewSet, UserViewset


route = routers.DefaultRouter()
route.register('users',UserViewset)
route.register('movies', MovieViewSet)
route.register('ratings', RatingViewSet)


urlpatterns = [
    path('/', include(route.urls))
]