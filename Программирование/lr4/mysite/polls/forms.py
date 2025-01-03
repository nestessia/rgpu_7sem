from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
       model = Question
       fields = ['question_text']
    question_text = forms.CharField(max_length=200, label='Текст вопроса')
    choice1 = forms.CharField(max_length=200, label='Вариант ответа 1')
    choice2 = forms.CharField(max_length=200, label='Вариант ответа 2')