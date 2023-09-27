from rest_framework import serializers
from .models import Assignment
from questions.serializers import QuestionSerializer
from questions.models import Question
from rest_framework.serializers import ValidationError


class AssignmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])

        assignment = Assignment.objects.create(**validated_data)

        for question_data in questions_data:
            question_id = question_data.get('title')

            try:
                question = Question.objects.get(title=question_id)
                assignment.questions.add(question)
            except Question.DoesNotExist:
                raise ValidationError('Invalid Questions')

        return assignment

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        existing_questions = instance.questions.all()
        questions_data = validated_data.get('questions', [])

        # Remove questions that are no longer in the updated list
        for existing_question in existing_questions:
            if existing_question not in questions_data:
                instance.questions.remove(existing_question)

        # Add non existing questions
        for new_question in questions_data:
            question_id = new_question.get('title')
            if new_question not in existing_questions:
                try:
                    question = Question.objects.get(title=question_id)
                    instance.questions.add(question)
                except Question.DoesNotExist:
                    raise ValidationError('Invalid Questions')

        instance.save()
        return instance
