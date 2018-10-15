from collections import defaultdict
import json

from django.contrib import messages
from django.shortcuts import render

from evacuation.models import EvacUser, Desk, Office

from .models import Question, Answer, Survey
from django.contrib.auth.models import User, Group


def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            answers = Answer.objects.filter(user=request.user, question__survey__name='Post evacuation')
            if answers:
                messages.add_message(request, messages.INFO, "Survey already taken")
                return render(request, 'survey/survey.html')
            groups = request.user.groups.all()
            survey = Survey.objects.filter(group_features__in=groups, group_landmarks__in=groups, active=True)[0]
            questions = Question.objects.filter(survey=survey).order_by('order')
            evac_user = EvacUser.objects.get(user=request.user)
            has_taken = Answer.objects.filter(question=questions[0], user=request.user).exists()
            context = {
                'survey': questions,
                'floor': evac_user.floor if evac_user.floor else 1,
                'has_taken': has_taken,
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


def guest(request):
    if request.method == 'GET':
        survey = Survey.objects.filter(group_features=None, group_landmarks=None, active=True)[0]
        questions = Question.objects.filter(survey=survey).order_by('order')
        floor_offices = {0: defaultdict(dict), 1: defaultdict(dict), 2: defaultdict(dict), 3: defaultdict(dict)}
        offices = Office.objects.all()
        for office in offices:
            floor_offices[office.floor][office.name] = []
        desks = Desk.objects.all()
        for desk in desks:
            floor_offices[desk.office.floor][desk.office.name].append(desk.name)
        context = {
            'survey': questions,
            'has_taken': False,
            'floor_office_desks': json.dumps(floor_offices)
        }
        return render(request, 'survey/guest.html', context)
    else:

        latest_user = User.objects.all().order_by('-id')[0]
        user = User.objects.create_user('anon_{}'.format(latest_user.id + 1))

        user.save()

        floor = int(request.POST['floor']) if request.POST['floor'] else None
        office = Office.objects.get(name=request.POST['office']) if request.POST['office'] else None
        desk = Desk.objects.get(name=request.POST['desk'], office=office) if request.POST['desk'] else None

        extended_user = EvacUser(
            user=user,
            age=int(request.POST['age']),
            gender=request.POST['gender'],
            floor=floor,
            office=office,
            desk=desk,
            mobility_restriction='{}{}'.format('Yes: ' if int(request.POST['mobility']) else 'No', request.POST['mobility_restriction']),
            phone_make=request.POST['phone_make'],
            phone_use=','.join(request.POST.getlist('phone_use[]'))
        )
        extended_user.save()

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
                answer = Answer(question=question, user=user, text=answer_text)
                answer.save()

        messages.add_message(request, messages.SUCCESS, "Answers submitted successfully")
        return render(request, 'survey/guest.html')
