from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PatientEntry
from .util import (
    get_rp_dict,
    get_all_active_patient_entries,
    get_all_completed_patient_entries,
    send_consumers_table,
    save_model_changes,
    save_model,
)


@login_required()
def view(request):
    template = loader.get_template("cspatients/view.html")
    context = {
        "active": get_all_active_patient_entries(),
        "completed": get_all_completed_patient_entries(),
    }
    return HttpResponse(template.render(context), status=200)


@login_required()
def patient(request, patient_id):
    template = loader.get_template("cspatients/patient.html")
    patiententry = (
        PatientEntry.objects.filter(patient__patient_id=patient_id)
        .order_by("-decision_time")
        .first()
    )

    context = {"patiententry": patiententry}
    if patiententry:
        status_code = status.HTTP_200_OK
    else:
        status_code = status.HTTP_404_NOT_FOUND
    return HttpResponse(template.render(context), status=status_code)


@login_required()
def form(request):
    errors = []
    status_code = status.HTTP_200_OK
    if request.method == "POST":
        entry, errors = save_model(request.POST)
        if entry:
            status_code = status.HTTP_201_CREATED
            send_consumers_table()
        else:
            status_code = status.HTTP_400_BAD_REQUEST
    return render(
        request, "cspatients/form.html", context={"errors": errors}, status=status_code
    )


# API VIEWS
class NewPatientEntryView(APIView):
    def post(self, request):
        entry, errors = save_model(get_rp_dict(request.data))
        if entry:
            send_consumers_table()
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return JsonResponse({"errors": ", ".join(errors)}, status=status_code)


class CheckPatientExistsView(APIView):
    def post(self, request):
        try:
            patient_id = get_rp_dict(request.data)["patient_id"]
            PatientEntry.objects.get(patient__patient_id=patient_id)
        except PatientEntry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


class UpdatePatientEntryView(APIView):
    def post(self, request):
        changes_dict = get_rp_dict(request.data, context="entrychanges")
        entry, errors = save_model_changes(changes_dict)
        if entry:
            status_code = status.HTTP_200_OK
            send_consumers_table()
        else:
            status_code = status.HTTP_400_BAD_REQUEST
        return JsonResponse({"errors": ", ".join(errors)}, status=status_code)


class EntryStatusUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = get_rp_dict(request.data)
        try:
            patiententry = PatientEntry.objects.get(
                patient__patient_id=data["patient_id"]
            )

            if data["option"] == "Delivery":
                patiententry.delivery_time = timezone.now()
            elif data["option"] == "Completed":
                patiententry.completion_time = timezone.now()

            patiententry.save()
            send_consumers_table()
        except PatientEntry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)
