from django.urls import path
from .views import *
urlpatterns = [
    path('coding-questions/', CodingQuestionList.as_view(), name='coding-question-list'),
    path('mcq-questions/', MCQQuestionList.as_view(), name='mcq-question-list'),
    path('mcq-categories/', MCQCategoryList.as_view(), name='category-list'),
    path('coding-categories/', CodingQuestionsCategoryList.as_view(), name='category-list'),
    path('questions/<int:id>/', QuestionDetail.as_view(), name='question-detail'),
    path('questions/search/', QuestionSearch.as_view(), name='question-search'),
    path('questions/category/<str:category_name>/', QuestionListByCategory.as_view(), name='question-list-by-category'),
]




