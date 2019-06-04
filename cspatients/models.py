from django.contrib.auth.models import User
from django.db import models


class Patient(models.Model):
    patient_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.patient_id, self.name)


class PatientEntry(models.Model):
    ELECTIVE = 5
    COLD = 4
    HOT_YELLOW = 3
    HOT_ORANGE = 2
    IMMEDIATE = 1

    URGENCY_CHOICES = (
        (ELECTIVE, "Elective"),
        (COLD, "Cold"),
        (HOT_YELLOW, "Hot"),
        (HOT_ORANGE, "Hot"),
        (IMMEDIATE, "Immediate"),
    )

    patient = models.ForeignKey(
        Patient, related_name="patient_entries", on_delete=models.CASCADE
    )
    operation = models.CharField(max_length=255, default="CS")
    parity = models.IntegerField(default=0)
    gravidity = models.IntegerField(default=1)
    comorbid = models.CharField(max_length=255, null=True)
    indication = models.CharField(max_length=255, null=True)
    decision_time = models.DateTimeField(auto_now_add=True)
    completion_time = models.DateTimeField(null=True)
    urgency = models.IntegerField(default=4, choices=URGENCY_CHOICES)
    location = models.CharField(max_length=255, null=True)
    outstanding_data = models.CharField(max_length=255, null=True)
    clinician = models.CharField(max_length=255, null=True)
    foetus = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def gravpar(self):
        return "G{}P{}".format(self.gravidity, self.parity)

    def __str__(self):
        return "{} having {}".format(self.patient, self.operation)


class Baby(models.Model):
    patiententry = models.ForeignKey(
        PatientEntry, related_name="entry_babies", on_delete=models.CASCADE
    )
    baby_number = models.IntegerField()
    delivery_time = models.DateTimeField()
    apgar_1 = models.IntegerField()
    apgar_5 = models.IntegerField()
    baby_weight_grams = models.IntegerField()
    nicu = models.BooleanField()

    class Meta:
        unique_together = ("patiententry", "baby_number")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    msisdn = models.CharField("MSISDN(+country code)", max_length=30, blank=True)

    def __str__(self):
        return "{}: {}".format(self.user.username, self.msisdn)
