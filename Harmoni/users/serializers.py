from .models import User, ActivityLog
from rest_framework import serializers




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = { "password": {"write_only": True} }

    def create(self, validated_data):
        user  = User.objects.create_user(**validated_data)
        return user
    

class ActivityLogSerializer(serializers.ModelSerializer):
    action_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ActivityLog
        fields = ['id', 'action', 'action_display', 'ip_address', 'user_agent', 'metadata', 'created_at']

    def get_action_display(self, obj):
        return obj.get_action_display()