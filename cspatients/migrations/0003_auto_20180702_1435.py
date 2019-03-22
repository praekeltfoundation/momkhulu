# Generated by Django 2.0.6 on 2018-07-02 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("cspatients", "0002_auto_20180627_1525")]

    operations = [
        migrations.CreateModel(
            name="PatientEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("operation", models.CharField(default="CS", max_length=255)),
                ("gravpar", models.CharField(default="G1P1", max_length=6)),
                ("comorbid", models.CharField(max_length=255, null=True)),
                ("indication", models.CharField(max_length=255, null=True)),
                ("decision_time", models.DateTimeField(auto_now_add=True)),
                ("discharge_time", models.DateTimeField(null=True)),
                ("delivery_time", models.DateTimeField(null=True)),
                ("urgency", models.IntegerField(default=4)),
                ("location", models.CharField(max_length=255, null=True)),
                ("outstanding_data", models.CharField(max_length=255, null=True)),
                ("clinician", models.CharField(max_length=255, null=True)),
                ("apgar_1", models.IntegerField(null=True)),
                ("apgar_5", models.IntegerField(null=True)),
            ],
        ),
        migrations.AlterModelOptions(name="patient", options={}),
        migrations.RemoveField(model_name="patient", name="clinician"),
        migrations.RemoveField(model_name="patient", name="comorbidity"),
        migrations.RemoveField(model_name="patient", name="data"),
        migrations.RemoveField(model_name="patient", name="date"),
        migrations.RemoveField(model_name="patient", name="gravidity"),
        migrations.RemoveField(model_name="patient", name="indication"),
        migrations.RemoveField(model_name="patient", name="location"),
        migrations.RemoveField(model_name="patient", name="parity"),
        migrations.RemoveField(model_name="patient", name="time"),
        migrations.RemoveField(model_name="patient", name="urgency"),
        migrations.AddField(
            model_name="patiententry",
            name="patient_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="cspatients.Patient",
                to_field="patient_id",
            ),
        ),
    ]
