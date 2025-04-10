from django.urls import path
from .views import JournalListCreateView, JournalDetailView

urlpatterns = [
    path('', JournalListCreateView.as_view(), name='journal-list-create'),
    path('<int:pk>/', JournalDetailView.as_view(), name='journal-detail'),
]