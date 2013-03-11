from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import RegistrationForm, ParticipantForm

def registration(request):
    registration_form = RegistrationForm()
    participant_form = ParticipantForm()
    return render(request, 'registration.html', {
        'reg_form': registration_form,
        'part_form': participant_form
      })

def register(request):
    if request.method == "POST":
        return HttpResponse("TODO: HANDLE REGISTRATION")
    else:
        return HttpResponseRedirect('/')
