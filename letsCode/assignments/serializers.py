from rest_framework import serializers
from rest_framework.serializers import ValidationError

from questions.models import Question
from questions.serializers import QuestionSerializer

from .models import Assignment, AssignmentEnrollment


class AssignmentEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentEnrollment
        fields = ['id', 'user', 'assignment', 'status']


class AssignmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Assignment
        fields = ["id", "title", "description", "questions"]

    def create(self, validated_data):
        questions_data = validated_data.pop("questions", [])
        assignment = Assignment.objects.create(**validated_data)

        question_titles = [question_data["title"] for question_data in questions_data]
        questions = Question.objects.filter(title__in=question_titles)

        assignment.questions.add(*questions)

        return assignment

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)

        existing_questions = instance.questions.all()
        questions_data = validated_data.get("questions", [])

        new_questions = [Question.objects.get(title=q["title"]) for q in questions_data]

        instance.questions.set(new_questions)

        instance.save()
        return instance
