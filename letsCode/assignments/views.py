from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Assignment, AssignmentEnrollment
from .serializers import AssignmentEnrollmentSerializer, AssignmentSerializer


class UserAssignmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get_or_404(username=username)
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        assignments_enrolled = AssignmentEnrollment.objects.filter(
            user=user
        ).values_list("assignment", flat=True)
        assignments = Assignment.objects.filter(id__in=assignments_enrolled)
        serializer = AssignmentSerializer(assignments, many=True)

        return Response(serializer.data, safe=False, status=status.HTTP_200_OK)


class EnrollmentsViewSet(viewsets.ModelViewSet):
    queryset = AssignmentEnrollment.objects.all()
    serializer_class = AssignmentEnrollmentSerializer

    def list(self, request):
        queryset = AssignmentEnrollment.objects.filter(status='pending')
        serializer = AssignmentEnrollmentSerializer(queryset, many=True)
        return Response(serializer.data)


class AssignmentListView(ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class AssignmentCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = AssignmentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(creator=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
