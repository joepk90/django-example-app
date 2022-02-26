from djoser.views import UserViewSet


class CustomDjsoserUserViewSet(UserViewSet):
    http_method_names = [
        'get',
        # 'post', # disabled to prevent new user regisrations
        'patch',
        'delete',
        'head',
        'options',
    ]
