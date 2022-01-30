from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('forms', views.PostFormViewSet, basename='forms')
# basename set to prevent conflict with posts endpoint

urlpatterns = router.urls
