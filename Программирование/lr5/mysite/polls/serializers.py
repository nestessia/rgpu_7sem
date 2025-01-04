from rest_framework import serializers
from .models import Question, Choice, TextAnswer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']


class TextAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextAnswer
        fields = ['id', 'answer_text', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, source='choice_set')
    text_answers = TextAnswerSerializer(many=True, read_only=True, source='textanswer_set')
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'question_type', 'choices', 'text_answers', 'total_votes']

    def get_total_votes(self, obj):
        return sum(choice.votes for choice in obj.choice_set.all()) 