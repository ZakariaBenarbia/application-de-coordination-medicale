from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.core.exceptions import SuspiciousFileOperation
import os

from .forms import PatientForm, PatientFileForm
from .models import TeamMember, Patient, Shift, PatientFile

# List all team members
def team_member_list(request):
    members = TeamMember.objects.all().order_by("name")
    return render(request, "medapp/team/team_member_list.html", {"members": members}) #Template path Django looks in

# Detail for a single team member (show their shifts and assigned patients)
def team_member_detail(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    shifts = Shift.objects.filter(member=member).order_by("-start_time")
    patients = member.patients.all()  # related_name='patients' on Patient.assigned_to
    return render(
        request,
        "medapp/team/team_member_detail.html",
        {"member": member, "shifts": shifts, "patients": patients},
    )

# List all patients
def patient_list(request):
    patients = Patient.objects.all().order_by("name")
    return render(request, "medapp/patient/patient_list.html", {"patients": patients})

# Detail for a single patient (show files and assigned practitioners)
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    files = PatientFile.objects.filter(patient=patient).order_by("-uploaded_at")
    practitioners = patient.assigned_to.all()
    
    if request.method == "POST":
        form = PatientFileForm(request.POST, request.FILES)
        if form.is_valid():
            patient_file = form.save(commit=False)
            patient_file.patient = patient
            patient_file.uploaded_by = request.user.team_member if hasattr(request.user, 'team_member') else None
            patient_file.save()
            return redirect("medapp:patient_detail", pk=patient.pk)
    else:
        form = PatientFileForm()
    
    return render(
        request,
        "medapp/patient/patient_detail.html",
        {"patient": patient, "files": files, "practitioners": practitioners, "file_form": form},
    )


def patient_create(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect("medapp:patient_detail", pk=patient.pk)
    else:
        form = PatientForm()

    return render(
        request,
        "medapp/patient/patient_form.html",
        {"form": form},
    )


def patient_edit(request, pk):
    """
    Edit an existing patient record.
    Reuses the same `PatientForm` and template as `patient_create`.
    """
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save()
            return redirect("medapp:patient_detail", pk=patient.pk)
    else:
        form = PatientForm(instance=patient)

    return render(
        request,
        "medapp/patient/patient_form.html",
        {"form": form, "patient": patient},
    )

def patient_file_download(request, file_id):
    """
    Download or view a patient file.
    """
    patient_file = get_object_or_404(PatientFile, pk=file_id)
    
    # Check if file exists
    if not patient_file.file:
        return render(request, "medapp/error.html", {"error": "File not found"}, status=404)
    
    try:
        # Open and serve the file
        response = FileResponse(patient_file.file.open('rb'))
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(patient_file.file.name)}"'
        return response
    except Exception as e:
        return render(request, "medapp/error.html", {"error": f"Could not open file: {str(e)}"}, status=500)