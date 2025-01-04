from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import redirect
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required

from .forms import QuestionForm, ChoiceForm, ChoiceFormSet
from .models import Choice, Question, TextAnswer


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return all published questions (not including those set to be
        published in the future), ordered by publication date.
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.question_type == 'text':
            context['text_answers'] = self.object.textanswer_set.all().order_by('-created_at')
        return context


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if question.question_type == 'text':
        text_answer = request.POST.get("text_answer", "").strip()
        if not text_answer:
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "Необходимо ввести ответ.",
                },
            )
        # Сохраняем текстовый ответ
        TextAnswer.objects.create(
            question=question,
            answer_text=text_answer
        )
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        
    elif question.question_type == 'multiple':
        # Получаем список выбранных вариантов
        selected_choices = request.POST.getlist("choice")
        if not selected_choices:
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "Выберите хотя бы один вариант ответа.",
                },
            )
        try:
            for choice_id in selected_choices:
                selected_choice = question.choice_set.get(pk=choice_id)
                selected_choice.votes = F("votes") + 1
                selected_choice.save()
        except (KeyError, Choice.DoesNotExist):
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "Выбран недопустимый вариант ответа.",
                },
            )
    else:  # single choice
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "Вы не выбрали вариант ответа.",
                },
            )
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.save()
    
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


@login_required
def create_poll(request):
    choice_formset_class = formset_factory(ChoiceForm, formset=ChoiceFormSet, extra=2, min_num=2)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_formset = choice_formset_class(request.POST)
        
        is_valid_formset = True
        if question_form.data.get('question_type') != 'text':
            is_valid_formset = choice_formset.is_valid()
        
        if question_form.is_valid() and is_valid_formset:
            # Сохраняем вопрос
            question = question_form.save(commit=False)
            question.pub_date = timezone.now()
            question.save()
            
            # Сохраняем варианты ответа только для не текстовых вопросов
            if question.question_type != 'text':
                for choice_form in choice_formset:
                    if choice_form.cleaned_data.get('choice_text'):
                        choice = choice_form.save(commit=False)
                        choice.question = question
                        choice.save()
            
            return redirect('polls:index')
    else:
        question_form = QuestionForm()
        choice_formset = choice_formset_class()
    
    return render(request, 'polls/create_poll.html', {
        'question_form': question_form,
        'choice_formset': choice_formset
    })
