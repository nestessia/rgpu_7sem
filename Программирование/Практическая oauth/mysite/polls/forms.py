from django import forms
from .models import Question, Choice


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type']

    question_text = forms.CharField(
        max_length=200,
        label='Текст вопроса',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    question_type = forms.ChoiceField(
        choices=Question.QUESTION_TYPES,
        label='Тип вопроса',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ChoiceFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        
        # Получаем тип вопроса из формы вопроса
        if 'question_type' in self.data and self.data['question_type'] != 'text':
            if len(self.forms) < 2:
                raise forms.ValidationError("Необходимо добавить минимум 2 варианта ответа")


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        
    choice_text = forms.CharField(
        max_length=200,
        label='Вариант ответа',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
