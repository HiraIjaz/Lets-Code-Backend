from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Assignment, AssignmentEnrollment
from .serializers import AssignmentEnrollmentSerializer, AssignmentSerializer


class ApprovedEnrollmentsForUserListView(ListAPIView):
    serializer_class = AssignmentEnrollmentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        queryset = AssignmentEnrollment.objects.filter(user=user.id, status="approved")
        return queryset


class EnrollmentsViewSet(viewsets.ModelViewSet):
    queryset = AssignmentEnrollment.objects.all()
    serializer_class = AssignmentEnrollmentSerializer

    def has_permission(self, request, view):
        if self.action == "post":
            permission_classes = [IsAuthenticated]
            authentication_classes = [JWTAuthentication]
            return [permission() for permission in permission_classes]
        else:
            permission_classes = [IsAdminUser, IsAuthenticated]
            authentication_classes = [JWTAuthentication]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = AssignmentEnrollment.objects.filter(status="pending")
        serializer = AssignmentEnrollmentSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            enrollment = AssignmentEnrollment.objects.get(pk=pk)
        except:
            return Response(status=HTTP_404_NOT_FOUND)

        new_status = "approved"

        enrollment.status = new_status
        enrollment.save()

        serializer = AssignmentEnrollmentSerializer(enrollment)
        return Response(serializer.data)

    def create(self, request):
        serializer = AssignmentEnrollmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = self.request.user
        serializer = AssignmentEnrollmentSerializer(user=user.id, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AssignmentListView(ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class AssignmentCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = AssignmentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(creator=request.user)

            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AssignmentUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
