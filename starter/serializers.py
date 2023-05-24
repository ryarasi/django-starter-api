from rest_framework import serializers
from .models import File, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
