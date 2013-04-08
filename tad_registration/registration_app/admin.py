from django.contrib import admin
from registration_app.models import Participant, Registration

class ParticipantAdmin(admin.ModelAdmin):
  list_display = ('name', 'participation_choice', 'conference_dinner',)
  list_filter = ('participation_choice', 'conference_dinner',)

class ParticipantInline(admin.TabularInline):
  model = Participant
  extra = 0
  can_delete = False
  fields = ('name', 'participation_choice', 'conference_dinner', 't_shirt_size', 'twitter_account', 'email_address',)

class RegistrationAdmin(admin.ModelAdmin):
  inlines = [
    ParticipantInline,
  ]
  list_display = ('organisation', 'contact_person', 'billing_type',)
  list_filter = ('billing_type',)

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Registration, RegistrationAdmin)
