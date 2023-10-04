from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ApprovedEnrollmentsForUserListView,
    AssignmentCreateView,
    AssignmentListView,
    AssignmentUpdateView,
    EnrollmentsListView,
    EnrollmentsViewSet,
)

enrollment_router = DefaultRouter()
enrollment_router.register(r"api/enrollments", EnrollmentsViewSet)

urlpatterns = [
    path(
        "user-enrollments/",
        ApprovedEnrollmentsForUserListView.as_view(),
        name="user-enrollments",
    ),
    path(
        "all-enrollments/",
        EnrollmentsListView.as_view(),
        name="all-enrollments",
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
