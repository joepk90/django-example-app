from rest_framework import serializers
from . models import Post
from datetime import datetime, timezone, timedelta


class PostSerializer(serializers.ModelSerializer):

    last_update = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'last_update']

    # The following validation prevent the post from being saved if the last_update is within 1 hour
    # TODO: setup authentication instead of limiting updates by time

    def validate(self, data):

        # 'instance' will be set in case of `PUT` request i.e update
        if self.instance:
            object_id = self.instance.id  # get the 'id' for the instance
            post = Post.objects.get(id=object_id)

            last_update_plus_one_hour = post.last_update + timedelta(hours=1)
            datetime_now = datetime.now(timezone.utc)

            if last_update_plus_one_hour > datetime_now:

                remaining_timedelta = last_update_plus_one_hour - datetime_now
                remaining_time_in_minutes = remaining_timedelta.total_seconds() / 60
                raise serializers.ValidationError('The post cannot be updated for another ' + str(round(remaining_time_in_minutes)) + ' minutes')

        return data
