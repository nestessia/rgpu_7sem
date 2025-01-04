from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from polls.models import Question
import csv
import logging
import json

logger = logging.getLogger(__name__)


class ExportDataAPI(APIView):
    def get(self, request, format=None, *args, **kwargs):
        try:
            logger.debug(f"Request path: {request.path}")
            logger.debug(f"Request GET params: {request.GET}")
            
            # Определяем формат из пути URL или из параметра запроса
            if request.path.endswith('.csv'):
                export_format = 'csv'
            elif request.path.endswith('.json'):
                export_format = 'json'
            else:
                export_format = request.query_params.get('format', 'json').lower()
            
            if export_format not in ['json', 'csv']:
                return Response(
                    {'error': f'Unsupported format: {export_format}. Use json or csv.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            logger.debug(f"Requested format: {export_format}")
            
            questions = Question.objects.all()
            
            # Подготовим данные
            data = []
            for question in questions:
                question_data = {
                    'id': question.id,
                    'question_text': question.question_text,
                    'pub_date': question.pub_date.strftime(
                        '%Y-%m-%d %H:%M:%S'
                    ),
                    'question_type': question.question_type,
                }

                if question.question_type == 'text':
                    question_data['answers'] = [
                        {
                            'text': answer.answer_text,
                            'created_at': answer.created_at.strftime(
                                '%Y-%m-%d %H:%M:%S'
                            )
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
                    headers={
                        'Content-Disposition': 'attachment; filename="polls_data.csv"'
                    },
                )
                
                writer = csv.writer(response)
                writer.writerow([
                    'Question ID',
                    'Question Text', 
                    'Publication Date',
                    'Question Type', 
                    'Total Votes',
                    'Choices/Answers'
                ])
                
                for item in data:
                    if item['question_type'] == 'text':
                        answers = '; '.join(
                            [a['text'] for a in item.get('answers', [])]
                        )
                    else:
                        answers = '; '.join(
                            [f"{c['text']} ({c['votes']} votes)"
                             for c in item.get('choices', [])]
                        )
                    
                    writer.writerow([
                        item['id'],
                        item['question_text'],
                        item['pub_date'],
                        item['question_type'],
                        item.get('total_votes', 0),
                        answers
                    ])
                
                return response
            else:  # json
                response = HttpResponse(
                    content_type='application/json',
                    headers={
                        'Content-Disposition': 'attachment; filename="polls_data.json"'
                    },
                )
                json.dump(data, response, indent=2)
                return response

        except Exception as e:
            logger.error(f"General error: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
