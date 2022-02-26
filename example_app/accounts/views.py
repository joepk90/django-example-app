from djoser.views import UserViewSet
from drf_react_template.mixins import FormSchemaViewSetMixin
from rest_framework.permissions import AllowAny
from . serializers import UserAuthenticateSerializer


class CustomDjsoserUserViewSet(UserViewSet):
    http_method_names = [
        'get',
        # 'post', # disabled to prevent new user regisrations
        'patch',
        'delete',
        'head',
        'options',
    ]


class UserAuthenticateFormViewSet(FormSchemaViewSetMixin):
    serializer_class = UserAuthenticateSerializer
    permission_classes = [AllowAny]
