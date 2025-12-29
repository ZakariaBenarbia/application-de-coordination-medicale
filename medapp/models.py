from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    # Password to be set by admin when creating the team member
    password = models.CharField(max_length=128, blank=True, help_text="Set the login password for this team member")
    # Link to Django's User model for secure authentication
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='team_member')
    
    def __str__(self):
        return self.name


class Shift(models.Model):    
    member = models.ForeignKey(TeamMember, on_delete=models.CASCADE) # Links to TeamMember model
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.member.name} - {self.start_time} to {self.end_time}"

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Male')
    medical_history = models.TextField(blank=True)
    assigned_to = models.ManyToManyField(TeamMember, related_name='patients')  # Allows multiple practitioners

    def __str__(self):
        return self.name

class PatientFile(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    file = models.FileField(upload_to='patient_files/')  # Stores files in media/patient_files/
    uploaded_at = models.DateTimeField(auto_now_add=True) # Timestamp of upload
    uploaded_by = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"File for {self.patient.name} uploaded on {self.uploaded_at}"


# Signal: Create or update a corresponding Django User when TeamMember is saved
@receiver(post_save, sender=TeamMember)
def create_or_update_user(sender, instance, created, **kwargs):
    """
    After a TeamMember is saved, ensure a corresponding User exists.
    Username = slugified name (unique). User is linked back to TeamMember.
    """
    # If user already linked, nothing to do
    if instance.user:
        return

    # Generate unique username from team member name
    base_username = slugify(instance.name) if instance.name else f"user_{instance.id}"
    username = base_username
    counter = 1

    # Ensure uniqueness by appending counter if needed
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    # Create User with the generated username
    user = User.objects.create_user(
        username=username,
        email=instance.email if instance.email else '',
        first_name=instance.name
    )
    # Password will be set by admin via the password field in TeamMember
    if instance.password:
        user.set_password(instance.password)
        user.save()
    user.save()

    # Link the User back to the TeamMember
    instance.user = user
    instance.save(update_fields=['user'])
