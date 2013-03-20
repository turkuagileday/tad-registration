from django.forms import ModelForm
from models import Registration, Participant, NormalBillingType, PostBillingType, EBillingType

class RegistrationForm(ModelForm):
    class Meta:
        model = Registration

class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        exclude = ('registration')

class NormalBillingForm(ModelForm):
    class Meta:
        model = NormalBillingType
        exclude = ('registration')

class PostBillingForm(ModelForm):
    class Meta:
        model = PostBillingType
        exclude = ('registration')

class EBillingForm(ModelForm):
    class Meta:
        model = EBillingType
        exclude = ('registration')
