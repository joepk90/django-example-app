from datetime import datetime, timezone, timedelta
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import APIException
from rest_framework import status
from . models import Post


class LimitRecords(BasePermission):

    # limit individual post access to only the first post
    def has_permission(self, request, view):

        post_id = request.resolver_match.kwargs.get('pk')

        # if not requesting a specific post (list view) allow access
        if post_id == None:
            return True

        # if requesting the first post (id = 1) allow access
        if post_id == '1':
            return True

        # limit all other access
        return False


class CustomAPIException(APIException):

    def __init__(self, detail=None, code=None, error_id=None):
        super().__init__(detail=detail, code=code)
        self.error_id = error_id
        self.status_code = code


class LimitUpdates(BasePermission):
    message = {'errors': ['User is not a superuser']}

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:  # GET, HEADER, OPTIONS
            return True

        id = view.kwargs.get('pk', None)

        # we should never enter this because drf should first check if this post even exists...
        if id == None:
            raise CustomAPIException(
                detail='No post found',
                code=status.HTTP_404_NOT_FOUND
            )

        # 'instance' will be set in case of `PUT` request i.e update
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

        return True
