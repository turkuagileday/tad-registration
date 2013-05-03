from django.contrib import admin
from registration_app.models import Participant, Registration, CouponCodePrice, CouponCode

class ParticipantAdmin(admin.ModelAdmin):
  list_display = ('name', 'participation_choice', 'conference_dinner', 'ride_from_helsinki', 'active',)
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
