from django.shortcuts import render
from .models import Question, Answer
from django.contrib import messages


def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            answers = Answer.objects.filter(user=request.user, question__survey__name='Post evacuation')
            if answers:
                messages.add_message(request, messages.INFO, "Survey already taken")
                return render(request, 'survey/survey.html')
            survey = Question.objects.filter(survey__name='Post evacuation').order_by('order')
            context = {'survey': survey}
            return render(request, 'survey/survey.html', context)
        return render(request, 'evacuation/login.html')
    else:
        for question_id, answer_text in request.POST.items():
            if 'q_' in question_id:
                question = Question.objects.get(pk=int(question_id[2:]))
                if question.type == 'SingleChoice':
                    answer_text = answer_text[2:]
                answer = Answer(question=question, user=request.user, text=answer_text)
                answer.save()

        messages.add_message(request, messages.SUCCESS, "Answers submitted successfully")
        return render(request, 'survey/survey.html')
