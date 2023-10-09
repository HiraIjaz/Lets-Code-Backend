from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet, CodingQuestionSubmissionView

question_router = DefaultRouter()
question_router.register(r"api/questions", QuestionViewSet)

urlpatterns = [
    path(
        "submit-coding-question/",
        CodingQuestionSubmissionView.as_view(),
        name="submit-coding-question",
    ),
]
