from rest_framework import generics, serializers, filters
from .models import Question
from rest_framework.response import Response
from .serializers import QuestionSerializer
from django.db.models import Q
from rest_framework.views import APIView

class CodingQuestionList(generics.ListAPIView):
    queryset = Question.objects.filter(type='coding')
    serializer_class = QuestionSerializer


class MCQQuestionList(generics.ListAPIView):
    queryset = Question.objects.filter(type='mcq')
    serializer_class = QuestionSerializer


class MCQCategoryList(APIView):
    def get(self, request):
        categories = list(Question.objects.filter(type='mcq').values_list('category', flat=True).distinct())
        return Response(categories)


class CodingQuestionsCategoryList(APIView):
    def get(self, request):
        categories = list(Question.objects.filter(type='coding').values_list('category', flat=True).distinct())
        return Response(categories)


class QuestionDetail(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'id'


class QuestionSearch(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return Question.objects.filter(Q(title__icontains=query) | Q(data__icontains=query))


class QuestionListByCategory(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        return Question.objects.filter(category=category_name)
