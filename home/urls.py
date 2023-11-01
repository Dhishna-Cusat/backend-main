from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import CACreateViewSet

router = DefaultRouter()
router.register(r'ca', CACreateViewSet)

urlpatterns = [
    path('test/', views.test_view, name='my_route'),
] + router.urls
