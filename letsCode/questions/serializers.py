from rest_framework import serializers

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "title", "data", "type"]


class CodingAnswerSerializer(serializers.Serializer):
    questionId = serializers.IntegerField()
    code = serializers.CharField()


class CodingQuestionSubmissionSerializer(serializers.Serializer):
    answers = CodingAnswerSerializer(many=True)
