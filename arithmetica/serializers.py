from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import *
from website.serializers import ProfileSerializer
from website.models import Profile


class UserInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.profile.name", required=False)
    user_id = serializers.PrimaryKeyRelatedField(source="user.id", read_only=True)

    class Meta:
        model = UserInfo
        fields = ["id", "user_id", "credits", "lives", "name"]
        read_only_fields = ["user_id", "name"]

    def get_name(self, obj):
        return obj.user.profile.name


class RoundInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundInfo
        fields = ["id", "start_time", "end_time", "round_number", "problem_statement"]

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data["start_time"] > data["end_time"]:
            raise serializers.ValidationError("finish must occur after start")
        return data


class ErrorInfoSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = ErrorInfo
        fields = [
            "id",
            "user_info",
            "round",
            "credits",
            "error",
            "submitted_function",
        ]
        read_only_fields = ["user_info", "round"]

    def get_user_info(self, obj):
        return UserInfoSerializer(obj.user_info).data
