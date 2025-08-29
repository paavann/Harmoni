from .models import Journal
from rest_framework import serializers


class JournalSerializer(serializers.ModelSerializer):
    is_editable = serializers.SerializerMethodField()

    class Meta:
        model = Journal
        fields = [
            'id', 
            'user',
            'title',
            # 'category',
            'content',
            'ai_response',
            'sentiment',
            'created_at',
            'updated_at',
            # 'attachment',
            'is_editable',
        ]
        read_only_fields = [ 'user', 'ai_response', 'sentiment', 'created_at', 'updated_at', 'is_editable' ]

    def get_is_editable(self, obj):
        return obj.is_editable()