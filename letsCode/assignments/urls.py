from django.urls import path
from .views import UserAssignmentListView, AssignmentListView, AssignmentCreateView, AssignmentUpdateView

urlpatterns = [
    path('user/<str:username>/assignments/', UserAssignmentListView.as_view(), name='user-assignments'),

    path('assignments/', AssignmentListView.as_view(), name='assignments'),
    path('create-assignment/', AssignmentCreateView.as_view(), name='create-assignment'),
    path('edit-assignment/<int:pk>/', AssignmentUpdateView.as_view(), name='update-assignment'),



]
