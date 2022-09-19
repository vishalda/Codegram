from rest_framework import serializers
from .models import Group

class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields=('id','Title','Description','Image','admin')