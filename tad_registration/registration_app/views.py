from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from models import RegistrationForm, ParticipantForm, Participant

def registration(request):
    registration_form = RegistrationForm()
    participant_form = ParticipantForm()
    return render(request, 'registration.html', {
        'reg_form': registration_form,
        'part_forms': (participant_form, )
      })

def register(request):
    def populate_participant(index, reg_model, data):
        index_suffix = "-{i}".format(i=index)
        form_keys = [key for key in data if key.endswith(index_suffix)]
        model = Participant()
        for key in form_keys:
            real_key = key.split('-')[0]
            setattr(model, real_key, data[key])

        if reg_model:
            model.registration = reg_model

        model.conference_dinner = model.conference_dinner == "on"

        return model

    def validate_participants(participants):
        valid_participants = True
        for p in participants:
            try:
                p.full_clean()
            except ValidationError as e:
                valid_participants = False
                p.errors = e.message_dict
        return valid_participants

    if request.method == "POST":
        registration_form = RegistrationForm(request.POST)
        participant_count = int(request.POST['participant-count'])

        # Regmodel will be removed if validation error from validating participants is encountered
        valid_registration = registration_form.is_valid()
        reg_model = None
        if valid_registration:
            reg_model = registration_form.save()


        allowed_keys = {}
        for key in request.POST:
            for participant_key in Participant._meta.get_all_field_names():
                if participant_key != 'id' and key.startswith(participant_key):
                  allowed_keys.update({key: request.POST[key]})

        participants = [populate_participant(i, reg_model, allowed_keys) for i in range(0, participant_count)]
        valid_participants = validate_participants(participants)

        if valid_participants and valid_registration:
            for p in participants:
                p.save()
            return HttpResponse("success")
        else:
            if reg_model:
                reg_model.delete()

            participant_forms = []
            for model in participants:
                form = ParticipantForm(instance=model)
                if hasattr(model, "errors"):
                    form.errors.update(model.errors)
                participant_forms.append(form)

            return render(request, 'registration.html', {
                'reg_form': registration_form,
                'part_forms': participant_forms
            })
    else:
        return HttpResponseRedirect('/')
