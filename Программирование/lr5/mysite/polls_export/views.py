from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from polls.models import Question
import csv
import json
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class ExportDataAPI(APIView):
    renderer_classes = [JSONRenderer]  # По умолчанию используем JSON рендерер

    def get(self, request, *args, **kwargs):
        try:
            logger.debug(f"Request path: {request.path}")
            logger.debug(f"Request GET params: {request.GET}")
            
            questions = Question.objects.all()
            export_format = request.query_params.get('format', 'json').lower()
            
            logger.debug(f"Requested format: {export_format}")

            # Подготовим данные
            data = []
            for question in questions:
                question_data = {
                    'id': question.id,
                    'question_text': question.question_text,
                    'pub_date': question.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'question_type': question.question_type,
                }

                if question.question_type == 'text':
                    question_data['answers'] = [
                        {
                            'text': answer.answer_text,
                            'created_at': answer.created_at.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        for answer in question.textanswer_set.all()
                    ]
                else:
                    question_data['choices'] = [
                        {
                            'text': choice.choice_text,
                            'votes': choice.votes
                        }
                        for choice in question.choice_set.all()
                    ]
                    question_data['total_votes'] = sum(
                        choice.votes for choice in question.choice_set.all()
                    )

                data.append(question_data)

            # В зависимости от формата возвращаем разный response
            if export_format == 'csv':
                response = HttpResponse(
                    content_type='text/csv',
                    headers={'Content-Disposition': 'attachment; filename="polls_data.csv"'},
                )
                
                writer = csv.writer(response)
                # Записываем заголовки
                writer.writerow(['Question ID', 'Question Text', 'Publication Date', 
                               'Question Type', 'Total Votes', 'Choices/Answers'])
                
                # Записываем данные
                for item in data:
                    if item['question_type'] == 'text':
                        answers = '; '.join([a['text'] for a in item.get('answers', [])])
                    else:
                        answers = '; '.join([f"{c['text']} ({c['votes']} votes)" 
                                          for c in item.get('choices', [])])
                    
                    writer.writerow([
                        item['id'],
                        item['question_text'],
                        item['pub_date'],
                        item['question_type'],
                        item.get('total_votes', 0),
                        answers
                    ])
                
                return response
            else:
                return Response(data)

        except Exception as e:
            logger.error(f"General error: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
