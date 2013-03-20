import logging
from functools import partial

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from forms import RegistrationForm, ParticipantForm, NormalBillingForm, PostBillingForm, EBillingForm
from models import Participant, NormalBillingType, PostBillingType, EBillingType

def registration(request):
    registration_form = RegistrationForm()
    participant_form = ParticipantForm()
    normal_billing_form = NormalBillingForm()
    post_billing_form = PostBillingForm()
    e_billing_form = EBillingForm()
    return render(request, 'registration.html', {
        'reg_form': registration_form,
        'part_forms': (participant_form, ),
        'normal_billing_form': normal_billing_form,
        'post_billing_form': post_billing_form,
        'e_billing_form': e_billing_form
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

    def populate_billing_type(reg_model, data):
        def populate_common(billing_model, reg_model, data):
            billing_model.y_id = data.get('y_id', '')
            billing_model.recipient = data.get('recipient', '')
            billing_model.reference = data.get('reference', '')
            billing_model.registration = reg_model

        def populate_email(reg_model, data):
            email_model = NormalBillingType()
            populate_common(email_model, reg_model, data)
            email_model.email_address = data.get('email_address', '')
            return email_model

        def populate_post(reg_model, data):
            post_model = PostBillingType()
            populate_common(post_model, reg_model, data)
            post_model.address = data.get('address', '')
            post_model.postal_code = data.get('postal_code', '')
            post_model.post_office = data.get('post_office', '')
            post_model.extra_info = data.get('extra_info', '')
            return post_model

        def populate_ebilling(reg_model, data):
            e_model = EBillingType()
            populate_common(e_model, reg_model, data)
            e_model.billing_address = data.get('billing_address')
            e_model.operator = data.get('operator')
            return e_model

        populate_funcs = {
            'email': populate_email,
            'post': populate_post,
            'ebilling': populate_ebilling
        }

        try:
            model = populate_funcs[reg_model.billing_type](reg_model, data)
            try:
                model.full_clean()
            except ValidationError as e:
                model.errors = e.message_dict
            return model

        except KeyError:
            return None

    if request.method == "POST":
        logging.debug("got registration")

        registration_form = RegistrationForm(request.POST)
        normal_billing_form = NormalBillingForm()
        post_billing_form = PostBillingForm()
        e_billing_form = EBillingForm()


        participant_count = int(request.POST['participant-count'])

        # Regmodel and billingmodel will be removed if validation error from validating participants is encountered
        reg_model = None
        billing_model = None

        valid_registration = registration_form.is_valid()
        if valid_registration:
            reg_model = registration_form.save()

            billing_model = populate_billing_type(reg_model, request.POST)

            normal_billing_form = NormalBillingForm(instance=billing_model)
            post_billing_form = PostBillingForm(instance=billing_model)
            e_billing_form = EBillingForm(instance=billing_model)

            billing_forms = {
                'email': normal_billing_form,
                'post': post_billing_form,
                'ebilling': e_billing_form
            }

            if billing_model and not hasattr(billing_model, "errors"):
                billing_model = billing_model.save()

            else:
                valid_registration = False
                if billing_model:
                    billing_forms[reg_model.billing_type].errors.update(billing_model.errors)



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

            if billing_model and not hasattr(billing_model, "errors"):
                billing_model.delete()

            participant_forms = []
            for model in participants:
                form = ParticipantForm(instance=model)
                if hasattr(model, "errors"):
                    form.errors.update(model.errors)
                participant_forms.append(form)

            return render(request, 'registration.html', {
                'reg_form': registration_form,
                'part_forms': participant_forms,
                'normal_billing_form': normal_billing_form,
                'post_billing_form': post_billing_form,
                'e_billing_form': e_billing_form
            })
    else:
        return HttpResponseRedirect('/')
