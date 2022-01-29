from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet
from drf_react_template.mixins import FormSchemaViewSetMixin
from . models import Post
from . serializers import PostSerializer
from . permissions import LimitRecords


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

    # class Meta:
    #     model = Post
    #     fields = ['id', 'title', 'content']


class PostViewSet(ModelViewSet):

    # allowed HTTP methods
    http_method_names = HTTP_METHOD_NAMES

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [LimitRecords]

    class Meta:
        model = Post
        fields = ['id', 'title', 'content']
