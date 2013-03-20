from django.forms import ModelForm
from models import Registration, Participant, NormalBillingType, PostBillingType, EBillingType
from decorators import parsleyfy

@parsleyfy
class RegistrationForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Registration


@parsleyfy
class ParticipantForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Participant
        exclude = ('registration')

@parsleyfy
class NormalBillingForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = NormalBillingType
        exclude = ('registration')

@parsleyfy
class PostBillingForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = PostBillingType
        exclude = ('registration')

@parsleyfy
class EBillingForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = EBillingType
        exclude = ('registration')
