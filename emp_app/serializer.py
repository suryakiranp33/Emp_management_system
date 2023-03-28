# from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import serializers
from .models import Employee, LeaveSystem


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        # fields = '__all__'
        exclude = ["email","user"]

class EmployeeLeaveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveSystem
        exclude = ["nature"]




class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')