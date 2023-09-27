from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .models import AssignmentEnrollment, Assignment
from django.core.exceptions import ObjectDoesNotExist
from .serializers import AssignmentSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class UserAssignmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        assignments_enrolled = AssignmentEnrollment.objects.filter(user=user).values_list('assignment', flat=True)
        assignments = Assignment.objects.filter(id__in=assignments_enrolled)
        serializer = AssignmentSerializer(assignments, many=True)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class AssignmentListView(ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class AssignmentCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = AssignmentSerializer(data=request.data)

        if serializer.is_valid():
            print(request.user)
            serializer.save(creator=request.user)

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
