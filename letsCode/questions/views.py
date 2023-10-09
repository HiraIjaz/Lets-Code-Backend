from rest_framework import viewsets
from rest_framework.exceptions import APIException, NotFound
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Question
from .serializers import QuestionSerializer, CodingQuestionSubmissionSerializer
from utils import check_code


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def has_permission(self, request, view):
        if self.action == "list" or self.action == "get":
            return True
        else:
            permission_classes = [IsAdminUser, IsAuthenticated]
            authentication_classes = [JWTAuthentication]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = Question.objects.filter(isDeleted=False)
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

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


class CodingQuestionSubmissionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request, *args, **kwargs):
        serializer = CodingQuestionSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            answers_data = serializer.validated_data.get("answers", [])
            total_score = 0

            for answer_data in answers_data:
                code = answer_data.get("code")
                question_id = answer_data.get("questionId")

                question = Question.objects.get(id=question_id)
                question_data = question.data
                function_name = question_data.get("function_name", "")
                parameters = question_data.get("parameters", "")
                public_test_cases = question_data.get("public_test_cases", [])
                private_test_cases = question_data.get("private_test_cases", [])
                passed_test_case_count = 0
                for test_case in public_test_cases:
                    passed_test_case_count += check_code(
                        code,
                        function_name,
                        parameters,
                        test_case.get("input"),
                        test_case.get("output"),
                    )
                for test_case in private_test_cases:
                    passed_test_case_count += check_code(
                        code,
                        function_name,
                        parameters,
                        test_case.get("input"),
                        test_case.get("output"),
                    )
                print('count ', passed_test_case_count)
                if passed_test_case_count == len(private_test_cases) + len(
                    public_test_cases
                ):
                    total_score += 10

                else:
                    total_score += 0

            return Response({"score": total_score}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
