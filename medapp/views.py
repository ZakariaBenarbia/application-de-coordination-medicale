from django.shortcuts import render, get_object_or_404, redirect

from .forms import PatientForm
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
    return render(
        request,
        "medapp/patient/patient_detail.html",
        {"patient": patient, "files": files, "practitioners": practitioners},
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
