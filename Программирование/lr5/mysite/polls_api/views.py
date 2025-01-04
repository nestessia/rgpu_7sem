from rest_framework import generics, filters
from django.db.models import Count
from polls.models import Question
from polls.serializers import QuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class QuestionListAPI(APIView):
    def get(self, request):
        questions = Question.objects.all()

        # Фильтрация по датам
        date_from = request.query_params.get('date_from')
        if date_from:
            questions = questions.filter(pub_date__gte=date_from)

        date_to = request.query_params.get('date_to')
        if date_to:
            questions = questions.filter(pub_date__lte=date_to)

        # Фильтрация по типу вопроса
        question_type = request.query_params.get('question_type')
        if question_type:
            questions = questions.filter(question_type=question_type)

        # Сериализация данных
        data = []
        for question in questions:
            data.append({
                'id': question.id,
                'question_text': question.question_text,
                'pub_date': question.pub_date,
                'question_type': question.question_type
            })
        
        return Response(data)


class QuestionDetailAPI(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
