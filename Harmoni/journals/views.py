from rest_framework import generics, permissions
from .models import Journal
from .serializers import JournalSerializer
from .ai_utils import generate_analysis, sentiment_analysis


#check whether the user owns the Journal
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

#GET/CREATE Journal
class JournalListCreateView(generics.ListCreateAPIView):
    serializer_class = JournalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        journal_text = serializer.validated_data.get("content")
        mbti_type = user.mbti_type

        sentiment = sentiment_analysis(journal_text)
        ai_response = generate_analysis(journal_text, sentiment, mbti_type)

        serializer.save(user=user, ai_response=ai_response, sentiment=sentiment)

#GET/DELETE Journal
class JournalDetailView(generics.RetrieveDestroyAPIView):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]