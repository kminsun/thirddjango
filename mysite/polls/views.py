from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse
from django.db.models import Sum

from .models import Question, Choice, Etc_data


# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    etc_data = question.etc_data_set.all()
    votes_orderby = Choice.objects.filter(question_id=question_id).order_by('-votes')
    return render(request, 'polls/results.html', {'question': question, 'votes_orderby': votes_orderby, 'etc_data':etc_data} )

    # etc_data_isnull = get_object_or_404(Etc_data, pk=pk+1)
    # etc_data = Etc_data.objects.order_by('-pk')
    # max_voting = get_object_or_404(Choice, pk=question_id)
    # max_voting = Choice.objects.all().aggregate(Max('votes'))
    # max_voting = question.choice_set.all().aggregate(Max('votes'))
    # max_voting = question.choice_set.get(pk=question_id)
    # return render(request, 'polls/results.html', {'question': question, 'votes_orderby': votes_orderby})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # etc_data_temp = Etc_data(etc_text=request.POST['etc'], question_id=question_id, votes=0)
        # if etc_data.get(question_id=question_id).etc_text == request.POST['etc']:
        etc_data = question.etc_data_set.all()
        etc = request.POST['etc']
        selected_choice_list = request.POST.getlist('choice')

        # for choice in selected_choice_list:
        #     selected_choice = question.choice_set.get(pk=choice)
        #     selected_choice.votes += 1
        #     selected_choice.save()

        for etc_select in etc_data:
            if etc != '':
                etc_data_temp = Etc_data(etc_text=request.POST['etc'], question_id=question_id, votes=0)
                etc_data_temp.votes += 1
                etc_data_temp.save()

            elif str(etc_select) == etc:
                select_etc = question.etc_data_set.get(question_id=question_id, etc_text=etc)
                select_etc.votes += 1
                select_etc.save()


            for choice in selected_choice_list:
                selected_choice = question.choice_set.get(pk=choice)
                selected_choice.votes += 1
                selected_choice.save()

            # elif etc != '':
            #     etc_data_temp = Etc_data(etc_text=request.POST['etc'], question_id=question_id, votes=0)
            #     etc_data_temp.votes += 1
            #     etc_data_temp.save()
            #     break


            # else:
            #     return render(request, 'polls/detail.html', {
            #         'question': question,
            #         'error_message': "you didn't select choice."
            #     })

        # selected_choice_list = request.POST.getlist('choice')
        # selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # max_voting = question.choice_set.get(pk=question_id).aggregate(Max('votes'))
        # max_voting = Choice.objects.all().aggregate(Max('votes'))

        # for choice in selected_choice_list:
        #     selected_choice = question.choice_set.get(pk=choice)
        #     selected_choice.votes += 1
        #     selected_choice.save()

    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    # else:
        # selected_choice.votes += 1
        # selected_choice.save()
        # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    except(KeyError, etc_select.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "you didn't select choice or write."
        })

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))