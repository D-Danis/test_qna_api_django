from rest_framework import serializers
from .models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()
    
    class Meta:
        model = Answer
        fields = ['id', 'question', 'user_id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at', 'question']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Answer text cannot be empty.")
        return value


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at', 'answers']
        read_only_fields = ['id', 'created_at', 'answers']

    def validate_text(self, value)-> str:
        if not value.strip():
            raise serializers.ValidationError("Question text cannot be empty.")
        return value
