from django.contrib import admin
from .models import Candidate, kindId, Offers, State, Postulation
# Register your models here.

admin.site.register(Candidate)
admin.site.register(kindId)
admin.site.register(Offers)
admin.site.register(State)
admin.site.register(Postulation)