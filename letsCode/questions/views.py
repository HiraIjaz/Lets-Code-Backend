from rest_framework import viewsets, permissions
from .models import Question
from .serializers import QuestionSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAdminUser, IsAuthenticated , IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, APIException


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def has_permission(self, request, view):
        if self.action == 'list':
            return True
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            raise NotFound("Question not found")

        if instance.isDeleted:
            raise APIException("Question is already deleted")

        instance.isDeleted = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            raise NotFound("Question not found")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
