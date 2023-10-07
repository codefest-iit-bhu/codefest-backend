from rest_framework import serializers
from rest_framework.exceptions import ParseError

from website.models import Profile
from website.serializers import ProfileSerializer

from .models import *
import sympy as sp



class UserInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.profile.name", required=False)
    user_id = serializers.PrimaryKeyRelatedField(source="user.id", read_only=True)

    class Meta:
        model = UserInfo
        fields = ["id", "user_id", "credits", "lives", "name"]
        read_only_fields = ["user_id", "name"]

class RoundInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundInfo
        fields = ["id", "start_time", "end_time", "round_number","training_points" ,"problem_statement"]
        read_only_fields=["training_points"]
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data["start_time"] > data["end_time"]:
            raise serializers.ValidationError("finish must occur after start")
        return data

class RoundInfoPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundInfo
        fields = ["id", "start_time", "end_time", "round_number","training_points" ,"problem_statement"]

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(RoundInfoPublicSerializer, self).__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


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


class LatexExpressionSerializer(serializers.Serializer):
    latex_expression = serializers.CharField()
    round_id = serializers.IntegerField()

    def validate_round_id(self, value):
        try:
            round_info = RoundInfo.objects.get(id=value)
        except RoundInfo.DoesNotExist:
            raise serializers.ValidationError("Round not found.")

        return value

    def validate_latex_expression(self, value):
        try:
            parsed_expr = sp.sympify(value)
        except Exception as e:
            raise serializers.ValidationError(f"Invalid latex expression: {e}")

        return value
