from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet

question_router = DefaultRouter()
question_router.register(r"api/questions", QuestionViewSet)
