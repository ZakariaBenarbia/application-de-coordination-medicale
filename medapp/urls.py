from django.urls import path
from . import views

app_name = "medapp"

urlpatterns = [
    path("", views.team_member_list, name="team_index"),
    path("team/", views.team_member_list, name="team_member_list"),
    path("team/<int:pk>/", views.team_member_detail, name="team_member_detail"),
    path("patients/", views.patient_list, name="patient_list"),
    path("patients/new/", views.patient_create, name="patient_create"),
    path("patients/<int:pk>/", views.patient_detail, name="patient_detail"),
    path("patients/<int:pk>/edit/", views.patient_edit, name="patient_edit"),
    path("files/<int:file_id>/", views.patient_file_download, name="patient_file_download"),
]
