from django.db import models


class Patient(models.Model):
    patient_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField(default=20)

    def __str__(self):
        return self.name


class PatientEntry(models.Model):
    patient_id = models.ForeignKey(
        Patient, to_field="patient_id", on_delete=models.CASCADE
    )
    operation = models.CharField(max_length=255, default="CS")
    gravpar = models.CharField(max_length=6, default="G1P1")
    comorbid = models.CharField(max_length=255, null=True)
    indication = models.CharField(max_length=255, null=True)
    decision_time = models.DateTimeField(auto_now_add=True)
    discharge_time = models.DateTimeField(null=True)
    delivery_time = models.DateTimeField(null=True)
    completion_time = models.DateTimeField(null=True)
    urgency = models.IntegerField(default=4)
    location = models.CharField(max_length=255, null=True)
    outstanding_data = models.CharField(max_length=255, null=True)
    clinician = models.CharField(max_length=255, null=True)
    apgar_1 = models.IntegerField(null=True)
    apgar_5 = models.IntegerField(null=True)

    def __str__(self):
        return str(self.patient_id) + " having " + self.operation
