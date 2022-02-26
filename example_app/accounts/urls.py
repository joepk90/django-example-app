from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import CustomDjsoserUserViewSet, UserAuthenticateFormViewSet

router = DefaultRouter()
router.register("users", CustomDjsoserUserViewSet)
router.register('form/token', UserAuthenticateFormViewSet, basename='accountforms')

# TODO: enable djoser auth endpoints if authenticated as super user

urlpatterns = [
    path('', include('djoser.urls.jwt')),
]

urlpatterns += router.urls
