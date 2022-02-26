from rest_framework.permissions import BasePermission


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
