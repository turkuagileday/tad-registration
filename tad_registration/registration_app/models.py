from django.db import models
from django.forms import ModelForm

class Registration(models.Model):
    """
    Represent single registration.
    Every registration has contact_person, information about billing and all info about participants. Note that one registration can have more than one participant
    """
    BILLING_TYPE_CHOICES = (
        ('email', 'Email'),
        ('post', 'Post'),
        ('ebilling', 'E-billing')
    )
    contact_person = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    billing_type = models.CharField(max_length=255, choices=BILLING_TYPE_CHOICES)

class Participant(models.Model):
    PARTICIPATION_CHOICES = (
        ('both_days', 'Both days'),
        ('both_days_member', 'Both days (member)'),
        ('conference_day', 'Conference day'),
        ('conference_day_member', 'Conference day (member)'),
        ('student', 'Student')
    )

    T_SHIRT_SIZE = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL')
    )

    name = models.CharField(max_length=255)
    participation_choice = models.CharField(max_length=255, choices=PARTICIPATION_CHOICES)
    conference_dinner = models.BooleanField()
    special_diet = models.CharField(max_length=255, blank=True)
    t_shirt_size = models.CharField(max_length=255, choices=T_SHIRT_SIZE)
    twitter_account = models.CharField(max_length=255, blank=True)
# TODO: WORKSHOPS!
    other_info = models.TextField(blank=True)

    registration = models.ForeignKey(Registration)

class BillingType(models.Model):
    y_id = models.CharField(max_length=255, blank=True) # y_id, ugh :(
    recipient = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    registration = models.ForeignKey(Registration)

class NormalBillingType(BillingType):
    email_address = models.EmailField()

class PostBillingType(BillingType):
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    post_office = models.CharField(max_length=255)
    extra_info = models.CharField(max_length=255)

class EBillingType(BillingType):
    billing_address = models.CharField(max_length=255)
    operator = models.CharField(max_length=255)

# FORMS
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
