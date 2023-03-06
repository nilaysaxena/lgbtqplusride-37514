from django.contrib import admin
from .models import TermAndCondition


@admin.register(TermAndCondition)
class TermAndConditionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'type']
