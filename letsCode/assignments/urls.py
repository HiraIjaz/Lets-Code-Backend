from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (AssignmentCreateView, AssignmentListView,
                    AssignmentUpdateView, EnrollmentsViewSet,
                    UserAssignmentListView)

enrollment_router = DefaultRouter()
enrollment_router.register(r"api/enrollment", EnrollmentsViewSet)

urlpatterns = [
    path(
        "user/<str:username>/assignments/",
        UserAssignmentListView.as_view(),
        name="user-assignments",
    ),
    path("assignments/", AssignmentListView.as_view(), name="assignments"),
    path(
        "create-assignment/", AssignmentCreateView.as_view(), name="create-assignment"
    ),
    path(
        "edit-assignment/<int:pk>/",
        AssignmentUpdateView.as_view(),
        name="update-assignment",
    ),
]
