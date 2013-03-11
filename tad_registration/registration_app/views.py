from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from models import RegistrationForm, ParticipantForm, Participant

def registration(request):
    registration_form = RegistrationForm()
    participant_form = ParticipantForm()
    return render(request, 'registration.html', {
        'reg_form': registration_form,
        'part_form': participant_form
      })

# TODO: REQUIRED FIELDS! INFO USER
def register(request):
    def populate_participant(index, reg_model, request):
        index_suffix = "-{i}".format(i=index)
        form_keys = [key for key in request.POST if key.endswith(index_suffix)]
        model = Participant()
        for key in form_keys:
            real_key = key.split('-')[0]
            setattr(model, real_key, request.POST[key])

        model.registration = reg_model
        model.conference_dinner = model.conference_dinner == "on"
        model.full_clean()

        return model
        
    if request.method == "POST":
        registration_form = RegistrationForm(request.POST)
        participant_count = int(request.POST['participant-count'])

        if registration_form.is_valid():
            # Regmodel will be removed if validation error from validating participants is encountered
            reg_model = registration_form.save()

            try:
                participants = [populate_participant(i, reg_model, request) for i in range(0, participant_count)]
                for p in participants:
                    p.save()

                return HttpResponse("success")
            except ValidationError:
                reg_model.delete()
                return HttpResponse("Not valid participants")

        else:
            return HttpResponse("Not valid registration")
    else:
        return HttpResponseRedirect('/')
