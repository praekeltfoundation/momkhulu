from django.urls import path

from . import views

urlpatterns = [
    path("", views.view, name="root"),
    path("view", views.view, name="cspatient_view"),
    path("form", views.form, name="cspatient_form"),
    path("patient/<str:patient_id>", views.patient, name="cspatient_patient"),
    path(
        "api/rpnewpatiententry",
        views.NewPatientEntryView.as_view(),
        name="rp_newpatiententry",
    ),
    path(
        "api/rppatientexists",
        views.CheckPatientExistsView.as_view(),
        name="rp_patientexits",
    ),
    path(
        "api/rpentrychanges",
        views.UpdatePatientEntryView.as_view(),
        name="rp_entrychanges",
    ),
    path(
        "api/rpentrystatusupdate",
        views.EntryStatusUpdateView.as_view(),
        name="rp_entrystatus_update",
    ),
    path("health_details", views.detailed_health, name="detailed-health"),
]
