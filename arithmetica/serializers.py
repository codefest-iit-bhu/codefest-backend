from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import *
from website.serializers import ProfileSerializer
from website.models import Profile

class UserInfoSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()
    class Meta:
        model = UserInfo
        fields = ['id','user' ,'credits', 'lives','name']
        read_only_fields = ['user']
    def to_representation(self,data):
        data = super(UserInfoSerializer, self).to_representation(data)
        user_id=data['user']
        data.pop('user')
        data["user_id"]=user_id
        return data
    def get_name(self,obj):
        return obj.user.profile.name

class RoundInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=RoundInfo
        fields=['id','start_time','end_time','round_number','problem_statement']
        
class ErrorInfoSerializer(serializers.ModelSerializer):
    user_info=serializers.SerializerMethodField()
    class Meta:
        model = ErrorInfo
        fields = ['id','user_info' ,'round','credits', 'error','submitted_function',]
        read_only_fields = ['user_info','round']
    def get_user_info(self,obj):
        return UserInfoSerializer(obj.user_info).data