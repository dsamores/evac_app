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
            # survey = list(TextQuestion.objects.filter(survey__name='Post evacuation'))
            # survey += list(ChoicesQuestion.objects.filter(survey__name='Post evacuation'))
            # survey.sort(key=lambda x: x.order)
            survey = Question.objects.filter(survey__name='Post evacuation').order_by('order')
            context = {'survey': survey}
            return render(request, 'survey/survey.html', context)
        return render(request, 'evacuation/login.html')
    else:
        # email = request.POST['email']
        # password = request.POST['password']

        for question_id, answer in request.POST.items():
            if 'q_' in question_id:
                question_id = int(question_id[2:])
                question = Question.objects.get(pk=question_id)

        messages.add_message(request, messages.SUCCESS, "Answers submitted successfully")
        return render(request, 'survey/survey.html')
