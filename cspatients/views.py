from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .models import Patient, PatientEntry
from .util import get_rp_dict, view_all_context, patient_has_delivered
from .util import send_consumers_table, save_model_changes, save_model


def log_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    context = {
        "try": False,
    }
    if request.method == "POST":
        context['try'] = True
        password = request.POST['password']
        username = request.POST['username']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.GET.get('next')
            return HttpResponseRedirect(next)
    return render(request, 'cspatients/login.html', context, status=200)


@login_required(login_url="/cspatients/login")
def log_out(request):
    template = loader.get_template('cspatients/logout.html')
    logout(request)
    return HttpResponse(template.render())


@login_required(login_url="/cspatients/login")
def view(request):

    template = loader.get_template('cspatients/view.html')
    context = {
        "patiententrys": view_all_context()
    }
    return HttpResponse(
        template.render(context),
        status=200
        )


@login_required(login_url="/cspatients/login")
def patient(request, patient_id):
    template = loader.get_template("cspatients/patient.html")
    try:
        patiententry = PatientEntry.objects.get(patient_id=patient_id)
        context = {
            "patiententry": patiententry,
        }
        status_code = 200
    except Patient.DoesNotExist:
        context = {
            "patiententry": False,
        }
        status_code = 400
    return HttpResponse(template.render(context), status=status_code)


@login_required(login_url="/cspatients/login")
def form(request):
    context = {
        "saved": False,
    }
    status_code = 200
    if request.method == "POST":
        status_code = save_model(request.POST)
        if status_code == 201:
            send_consumers_table()
    return render(
        request, "cspatients/form.html",
        context=context,
        status=status_code
        )


@csrf_exempt
def rp_event(request):
    """
        RapidPro should use the following url
        /event?secret=momkhulu

    """
    # Takes in the information from Rapid Pro
    status_code = 405
    if request.method == "POST":
        if request.GET.get('secret') == "momkhulu":
            status_code = save_model(request.POST)
            if status_code == 201:
                send_consumers_table()
    return HttpResponse(status=status_code)


@csrf_exempt
def patientexists(request):
    """
        Returns 200 if Patient exists and 400 if Patient Does Not Exist
    """
    status_code = 405
    if request.method == "POST":
        try:
            Patient.objects.get(
                patient_id=get_rp_dict(request.POST, "patient")['patient_id']
                )
            status_code = 200
        except Patient.DoesNotExist:
            status_code = 400
    return HttpResponse(status=status_code)


@csrf_exempt
def entrychanges(request):
    status_code = 405
    if request.method == "POST":
        status_code = save_model_changes(request.POST)
    return HttpResponse(status=status_code)


@csrf_exempt
def entrydelivered(request):
    status_code = 405
    if request.method == "POST":
        status_code = patient_has_delivered(request.POST)
    return HttpResponse(status=status_code)
