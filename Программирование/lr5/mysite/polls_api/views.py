from rest_framework import generics, filters
from django.db.models import Count
from polls.models import Question
from polls.serializers import QuestionSerializer


class QuestionListAPI(generics.ListAPIView):
    serializer_class = QuestionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['pub_date', 'choice__votes']

    def get_queryset(self):
        queryset = Question.objects.annotate(
            total_votes=Count('choice__votes')
        ).all()

        # Фильтрация по дате
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(pub_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(pub_date__lte=end_date)

        # Сортировка
        sort_by = self.request.query_params.get('sort_by', None)
        if sort_by == 'date':
            queryset = queryset.order_by('-pub_date')
        elif sort_by == 'votes':
            queryset = queryset.order_by('-total_votes')

        return queryset


class QuestionDetailAPI(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
