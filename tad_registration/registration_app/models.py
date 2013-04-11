# -*- coding: UTF-8 -*-
from django.db import models

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
    def get_registration_cost(self):
        cost = 0
        for p in self.participant_set.all():
            cost += p.get_participation_cost()

        if self.billing_type != 'email':
            cost += 5

        return cost

    
    contact_person = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.EmailField()
    billing_type = models.CharField(max_length=255, choices=BILLING_TYPE_CHOICES, help_text="A processing fee of 5 EUR is applied for all billing types other than Email.")
    invoice_customer_id = models.IntegerField(blank=True, null=True)
    invoice_invoice_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.organisation + ' (' + self.contact_person + ')'

class Participant(models.Model):
    PARTICIPATION_CHOICES = (
        ('both_days', 'Both days – 200 €'),
        ('both_days_member', 'Both days (member) – 180 €'),
        ('conference_day', 'Conference day – 140 €'),
        ('conference_day_member', 'Conference day (member) – 130 €'),
        ('student', 'Student – 10 €')
    )

    T_SHIRT_SIZE = (
        ('no_shirt', 'No T-shirt'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL')
    )

    def get_participation_cost(self):
        payments = {
          'both_days': 200,
          'both_days_member': 180,
          'conference_day': 140,
          'conference_day_member': 130,
          'student': 10
        }
        return payments[self.participation_choice]

    name = models.CharField(max_length=255)
    participation_choice = models.CharField(max_length=255, choices=PARTICIPATION_CHOICES, help_text="Member choices are for Asteriski ry and Digit ry members only!")
    conference_dinner = models.BooleanField(default=True, help_text="Not selecting this does not affect the price, it only allows us to reduce waste by not ordering too much food. You can change this until May 1st by notifying us at registration@turkuagileday.fi.")
    special_diet = models.CharField(max_length=255, blank=True)
    t_shirt_size = models.CharField(verbose_name="T-shirt size", max_length=255, choices=T_SHIRT_SIZE, help_text="Getting the T-shirts depends on finding a T-shirt sponsor. Interested? Ask more about sponsoring us from <a href=\"mailto:info@turkuagileday.fi\">info@turkuagileday.fi</a>!")
    twitter_account = models.CharField(max_length=255, blank=True)
    email_address = models.EmailField()
# TODO: WORKSHOPS!
    other_info = models.TextField(blank=True)

    registration = models.ForeignKey(Registration)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.participation_choice == 'student' and self.conference_dinner == True:
            raise ValidationError('Student price does not include the conference dinner!')

    def __unicode__(self):
        return self.name + ' (' + self.participation_choice + ')'

class BillingType(models.Model):
    vat_no = models.CharField(max_length=255, blank=True)
    recipient = models.CharField(max_length=255)
    reference = models.CharField(max_length=255, blank=True)
    registration = models.ForeignKey(Registration)

class NormalBillingType(BillingType):
    email_address = models.EmailField()

class PostBillingType(BillingType):
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    post_office = models.CharField(max_length=255)
    extra_info = models.CharField(max_length=255, blank=True)

class EBillingType(BillingType):
    billing_address = models.CharField(max_length=255)
    operator = models.CharField(max_length=255)
