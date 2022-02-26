from datetime import datetime, timezone, timedelta
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException
from rest_framework import status
from drf_react_template.mixins import FormSchemaViewSetMixin
from . models import Post
from . serializers import PostSerializer
from . permissions import LimitRecords


class CustomAPIException(APIException):

    def __init__(self, detail=None, code=None, error_id=None):
        super().__init__(detail=detail, code=code)
        self.error_id = error_id
        self.status_code = code


def custom_perform_update(self, serializer):

    if self.request.user.is_authenticated == True:
        return serializer.save()

    id = self.kwargs.get('pk', None)
    post = Post.objects.get(id=id)

    last_update_plus_one_hour = post.last_update + timedelta(hours=1)
    datetime_now = datetime.now(timezone.utc)

    if last_update_plus_one_hour > datetime_now:

        remaining_timedelta = last_update_plus_one_hour - datetime_now
        remaining_time_in_minutes = remaining_timedelta.total_seconds() / 60
        message = 'The post cannot be updated for another ' + str(round(remaining_time_in_minutes)) + ' minutes'
        raise CustomAPIException(
            detail=message,
            code=status.HTTP_401_UNAUTHORIZED
        )
    serializer.save()


# allowed HTTP methods
# this prevents posts from being deleted:
# while only the first post is accessible, we don't want to delete the first post
HTTP_METHOD_NAMES = [
    'get',
    # 'post',
    'put',
    'patch',
    # 'delete',
]


# Form View Set

# list view: not allowed (don't want to return a list and the form schema)
# http://host/blog/forms/

# retrieve view: allowed
# http://host/blog/forms/:id

# TODO
# work out how to request just the form data:
# - use a query parameter (form=true) to includeFormSchemaViewSetMixin
# - setup authentication? - stop the form data from being returned if not authenticated


class PostFormViewSet(CreateModelMixin,
                      #   DestroyModelMixin,
                      #   ListModelMixin,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      FormSchemaViewSetMixin):

    # allowed HTTP methods
    http_method_names = HTTP_METHOD_NAMES

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny, LimitRecords]

    # class Meta:
    #     model = Post
    #     fields = ['id', 'title', 'content']

    def perform_update(self, serializer):
        custom_perform_update(self, serializer)


class PostViewSet(ModelViewSet):

    # allowed HTTP methods
    http_method_names = HTTP_METHOD_NAMES

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny, LimitRecords]

    class Meta:
        model = Post
        fields = ['id', 'title', 'content']

    def perform_update(self, serializer):
        custom_perform_update(self, serializer)
