from rest_framework import serializers

from anony_app.models import User


class UserDetailedSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ( "username", "password")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("created_at", )
