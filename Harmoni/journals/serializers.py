from .models import Journal, JournalEntry
from rest_framework import serializers



class JournalSerializer(serializers.ModelSerializer):
    total_entries = serializers.SerializerMethodField()

    class Meta:
        model = Journal
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "total_entries",
        ]
        read_only_fields = ["id", "created_at", "total_entries"]

    def get_total_entries(self, obj):
        return obj.entries.count()


class JournalEntrySerializer(serializers.ModelSerializer):
    is_editable = serializers.SerializerMethodField()

    class Meta:
        model = JournalEntry
        fields = [
            "id",
            "journal",
            "title",
            "content",
            "category",
            "ai_response",
            "sentiment",
            "created_at",
            "updated_at",
            "is_editable",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "ai_response",
            "sentiment",
            "is_editable",
        ]

        def get_is_editable(self, obj):
            return obj.is_editable()