from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields = '__all__'

#User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','email')

#Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=255, write_only=True)
    class Meta:
        model = User
        fields = ('id','username','email','password','first_name','address')
        extra_kwargs = {"password":{"write_only":True}}
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
        role=Role.objects.get(role_id=5)
        DoctorsandCompunder = DoctorsandCompunders.objects.create(
            username=validated_data['username'],
            name=validated_data['first_name'],
            email=validated_data['email'],
            address=validated_data['address'],
            role=role
        )
        DoctorsandCompunder.save()
        return user
    

class DoctorandCompounderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorsandCompunders
        fields = '__all__'
        depth = 1