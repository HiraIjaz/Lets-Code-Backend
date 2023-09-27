from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet

# Create a router and register the QuestionViewSet with it.
router = DefaultRouter()
router.register(r"api/questions", QuestionViewSet)
