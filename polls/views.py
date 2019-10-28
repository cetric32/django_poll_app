import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.conf import settings
from django.contrib.auth.decorators import login_required

from polls.models import Poll, Choice, Vote

from .forms import PollForm, EditPollForm, ChoiceForm

# Create your views here.

@login_required
def polls_list(request):
    """
    Renders the polls_list.htm template which lists all
    the currently available polls

    """


    polls = Poll.objects.all()

    paginator = Paginator(polls,5)

    page = request.GET.get('page')
    polls = paginator.get_page(page)


    context = { "polls":polls }
    return render(request, 'polls/polls_list.htm',context)


@login_required
def add_poll(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.owner = request.user
            new_poll.pub_date = datetime.datetime.now()
            new_poll.save()
            new_choice1 = Choice(
                poll = new_poll,
                choice_text = form.cleaned_data['choice1']
            ).save()
            new_choice2 = Choice(
                poll = new_poll,
                choice_text = form.cleaned_data['choice2']
            ).save()

            messages.success(request,
                            'Poll and Choices Added!',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('polls:list')


    else:
        form = PollForm()
    context = {'form':form}
    return render(request,'polls/add_poll.htm',context)

@login_required
def edit_poll(request,poll_id):
    poll = get_object_or_404(Poll,id=poll_id)
    if request.user != poll.owner:
        return redirect('polls:list')
    if request.method == 'POST':
        form = EditPollForm(request.POST,instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request,
                            'Poll Edited Succsessfully!',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('polls:list')
    else:
        form = EditPollForm(instance=poll)
    context = {'form':form,'poll':poll}
    return render(request,'polls/edit_poll.htm',context)


@login_required
def add_choice(request,poll_id):
    poll = get_object_or_404(Poll,id=poll_id)
    if request.user != poll.owner:
        return redirect('polls:list')

    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(request,
                            'Choice Added Successfully!',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('polls:edit_poll',poll.id)

    else:
        form = ChoiceForm()


    return render(request,'polls/add_choice.htm',{'form':form})


@login_required
def edit_choice(request,choice_id):
    choice = get_object_or_404(Choice,id=choice_id)
    poll = get_object_or_404(Poll,id=choice.poll.id)
    if request.user != poll.owner:
        return redirect('polls:list')

    if request.method == 'POST':
        form = ChoiceForm(request.POST,instance=choice)
        if form.is_valid():
            form.save()
            messages.success(request,
                            'Choice Edited Successfully!',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('polls:edit_poll',poll.id)

    else:
        form = ChoiceForm(instance=choice)


    return render(request,'polls/add_choice.htm',{'form':form,'edit_mode':True,'choice':choice})




@login_required
def poll_detail(request,poll_id):
    """
    Renders poll_detail.htm which allows a user to vote
    on the choices of a poll
    """
    #poll = Poll.objects.get(id=poll_id)
    poll = get_object_or_404(Poll,id=poll_id)

    results = poll.get_results_dict()

    user_can_vote = poll.user_can_vote(request.user)

    context = { "poll":poll,'user_can_vote':user_can_vote,'results':results }
    return render(request,'polls/poll_detail.htm',context)

@login_required
def delete_choice(request,choice_id):
    choice = get_object_or_404(Choice,id=choice_id)
    poll = get_object_or_404(Poll,id=choice.poll.id)
    if request.user != poll.owner:
        return redirect('polls:list')
    if request.method == 'POST':
        choice.delete()
        messages.success(
            request,
            'Choice deleted successfully',
            extra_tags = 'alert alert-success alert-dismissible fade show'
            )
        return redirect('polls:edit_poll',poll.id)
    return render(request,'polls/delete_choice_confirm.htm',{'choice':choice})


@login_required
def delete_poll(request,poll_id):
    poll = get_object_or_404(Poll,id=poll_id)
    if request.user != poll.owner:
        return render('polls:list')
    if request.method == 'POST':
        poll.delete()
        messages.success(
            request,
            'Poll deleted successfully',
            extra_tags = 'alert alert-success alert-dismissible fade show'
            )
        return redirect('polls:list')
    
    return render(request,'polls/delete_poll_confirm.htm',{'poll':poll_id})

@login_required
def poll_vote(request,poll_id):
    poll = get_object_or_404(Poll,id=poll_id)

    if not poll.user_can_vote(request.user):
        messages.error(request,
                        "You have already voted on the poll!",
                        extra_tags='alert alert-danger alert-dismissible fade show'
                        )
        return redirect('polls:list')
    choice_id = request.POST.get('choice')    
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        new_vote = Vote(user=request.user,poll=poll,choice= choice)
        print(new_vote)
        new_vote.save()
    else:
        messages.error(request,
                        "No Choice Was Selected!",
                        extra_tags='alert alert-danger alert-dismissible fade show'
                        )
        return redirect('polls:details',poll_id=poll_id)
    return redirect('polls:details',poll_id=poll_id)




