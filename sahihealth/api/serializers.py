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
    role = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'address', 'role')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Extract role name from validated_data
        role_name = validated_data.pop('role', None)

        # Create the User instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Retrieve the Role instance by name
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            raise serializers.ValidationError({"role": "Invalid role name provided."})

        # Create the DoctorsandCompunders instance
        DoctorsandCompunder = DoctorsandCompunders.objects.create(
            username=validated_data['username'],
            name=validated_data['first_name'],
            email=validated_data['email'],
            address=validated_data['address'],
            role=role
        )

        return user


class DoctorandCompounderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorsandCompunders
        fields = '__all__'
        depth = 1