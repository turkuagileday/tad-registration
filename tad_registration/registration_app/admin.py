from django.contrib import admin
from registration_app.models import Participant, Registration, CouponCodePrice, CouponCode
from communicator import Communicator
import logging

class ParticipantAdmin(admin.ModelAdmin):
  list_display = ('name', 'participation_choice', 'conference_dinner', 'ride_from_helsinki', 'ride_from_tampere', 'active',)
  list_filter = ('participation_choice', 'conference_dinner', 'active',)

class ParticipantInline(admin.TabularInline):
  model = Participant
  extra = 0
  can_delete = False
  fields = ('name', 'participation_choice', 'conference_dinner', 't_shirt_size', 'twitter_account', 'email_address',)

class RegistrationAdmin(admin.ModelAdmin):
  inlines = [
    ParticipantInline,
  ]
  list_display = ('organisation', 'contact_person', 'billing_type', 'date',)
  list_filter = ('billing_type',)
  actions = ['send_invoice']

  def send_invoice(modeladmin, request, queryset):
    for registration in queryset:
      communicator = Communicator(registration)
      try:
        if registration.billing_type == 'email':
          communicator.send_invoice_email()
      except RuntimeError:
        logging.error("Invalid statuscode. Is cloudvoice working. Email wasn't sent")
  send_invoice.short_description = 'Send invoice'

class CouponCodePriceInline(admin.TabularInline):
  model = CouponCodePrice
  extra = 0
  fields = ('participation_choice', 'price', 'amount',)

class CouponCodeAdmin(admin.ModelAdmin):
  inlines = [
    CouponCodePriceInline,
  ]
  list_display = ('code',)

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(CouponCode, CouponCodeAdmin)
