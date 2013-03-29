from django.contrib import admin
from registration_app.models import Participant, Registration

class RegistrationAdmin(admin.ModelAdmin):
  list_display = ('organisation', 'contact_person', 'billing_type',)
  list_filter = ('billing_type',)

class ParticipantAdmin(admin.ModelAdmin):
  list_display = ('name', 'participation_choice',)
  list_filter = ('participation_choice',)

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Registration, RegistrationAdmin)
