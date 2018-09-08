import json

from django.contrib import messages
from django.shortcuts import render

from evacuation.models import EvacUser

from .models import Question, Answer, Survey


def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            answers = Answer.objects.filter(user=request.user, question__survey__name='Post evacuation')
            if answers:
                messages.add_message(request, messages.INFO, "Survey already taken")
                return render(request, 'survey/survey.html')
            groups = request.user.groups.all()
            survey = Survey.objects.filter(group_features__in=groups, group_landmarks__in=groups, active=True)
            questions = Question.objects.filter(survey=survey[0]).order_by('order')
            evac_user = EvacUser.objects.get(user=request.user)
            context = {
                'survey': questions,
                'floor': evac_user.floor
            }
            return render(request, 'survey/survey.html', context)
        return render(request, 'evacuation/login.html')
    else:
        for question_id, answer_text in request.POST.items():
            if 'q_' in question_id:
                question = Question.objects.get(pk=int(question_id[2:]))
                if question.type == 'SingleChoice':
                    answer_text = answer_text[2:]
                elif question.type == 'SingleChoiceOther':
                    answer_text = answer_text[2:]
                    if answer_text == 'c_other':
                        other_answer = request.POST['other_{}'.format(question_id[2:])]
                        answer_text = '{}:{}'.format(answer_text, other_answer)
                elif question.type == 'MultipleChoice':
                    answers = request.POST.getlist(question_id)
                    answer_text = ','.join(map(lambda x: x[2:], answers))
                elif question.type == 'MultipleChoiceOther':
                    answers = request.POST.getlist(question_id)
                    if 'c_other' in answers:
                        other_answer = request.POST['other_{}'.format(question_id[2:])]
                        answers[answers.index('c_other')] = 'q_other:{}'.format(other_answer)
                    answer_text = ','.join(map(lambda x: x[2:], answers))
                elif question.type == 'Sketch':
                    answer_dict = {
                        'sketch': answer_text,
                        'floor': request.POST['floor_{}'.format(question_id[2:])],
                        'properties': request.POST['properties_{}'.format(question_id[2:])],
                    }
                    answer_text = json.dumps(answer_dict)
                answer = Answer(question=question, user=request.user, text=answer_text)
                answer.save()

        messages.add_message(request, messages.SUCCESS, "Answers submitted successfully")
        return render(request, 'survey/survey.html')
