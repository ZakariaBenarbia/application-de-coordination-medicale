from django.contrib import admin
from .models import TeamMember, Shift, Patient, PatientFile


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "role", "phone", "user")
    search_fields = ("name", "email", "role", "phone")
    list_filter = ("role",)
    ordering = ("name",)
    readonly_fields = ("user",)  # User is created automatically; prevent manual changes here
    fields = ("name", "email", "role", "phone", "password", "user")  # Show password field in form


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("member", "start_time", "end_time", "notes")
    search_fields = ("member__name", "notes")
    list_filter = ("member",)
    date_hierarchy = "start_time"
    autocomplete_fields = ("member",)
    ordering = ("-start_time",)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "age")
    search_fields = ("name", "medical_history")
    filter_horizontal = ("assigned_to",)
    ordering = ("name",)


@admin.register(PatientFile)
class PatientFileAdmin(admin.ModelAdmin):
    list_display = ("patient", "file", "uploaded_at", "uploaded_by")
    readonly_fields = ("uploaded_at",)
    search_fields = ("patient__name", "uploaded_by__name", "file")
    list_filter = ("uploaded_by", "uploaded_at", "patient")
    autocomplete_fields = ("patient", "uploaded_by")
    ordering = ("-uploaded_at",)
