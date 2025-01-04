from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime


class Question(models.Model):
    QUESTION_TYPES = [
        ('single', 'Один вариант ответа'),
        ('multiple', 'Несколько вариантов ответа'),
        ('text', 'Текстовый ответ'),
    ]

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default='single'
    )

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class TextAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.question_text}: {self.answer_text[:50]}"
