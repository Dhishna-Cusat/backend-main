from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import CACreateViewSet

router = DefaultRouter()
router.register(r'ca', CACreateViewSet)


urlpatterns = [
    path('ca/getref', views.get_referral, name='get_referral'),
    path('ca/points', views.get_points, name='get_points'),
              ] + router.urls
