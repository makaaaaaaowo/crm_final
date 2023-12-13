from django.shortcuts import render, redirect, HttpResponse
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record

from django.contrib import messages

from django.db import models
from django.http.response import JsonResponse

from rest_framework import viewsets
from .serializers import RecordSerializer
from .pdf import html2pdf
from django.db.models import Count

# - Homepage 

def home(request):

    return render(request, 'webapp/index.html')


# - Register a user

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Cuenta creada con exito!")

            return redirect("my-login")

    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)


# - Login a user

def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'form':form}

    return render(request, 'webapp/my-login.html', context=context)


# - Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()

    context = {'records': my_records}

    return render(request, 'webapp/dashboard.html', context=context)


# - Create a record 

@login_required(login_url='my-login')
def create_record(request):

    form = CreateRecordForm()

    if request.method == "POST":

        form = CreateRecordForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Usuario añadido con éxito!")

            return redirect("dashboard")

    context = {'form': form}

    return render(request, 'webapp/create-record.html', context=context)


# - Update a record 

@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, "Usuario actualizado con éxito!")

            return redirect("dashboard")
        
    context = {'form':form}

    return render(request, 'webapp/update-record.html', context=context)


# - Read / View a singular record

@login_required(login_url='my-login')
def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'webapp/view-record.html', context=context)


# - Delete a record

@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request, "Usuario eliminado con éxito!")

    return redirect("dashboard")



# - User logout

def user_logout(request):

    auth.logout(request)

    messages.success(request, "Has cerrado sesión")

    return redirect("my-login")

def about_us(request): 
    return render(request, 'webapp/about-us.html')



def stadistic_page(request):
    # Obtener la cantidad total de registros
    total_records = Record.objects.count()

    # Obtener la cantidad de registros por país
    records_by_country = Record.objects.values('country').annotate(count=Count('id'))

    # Obtener la cantidad de registros por ciudad
    records_by_city = Record.objects.values('city').annotate(count=Count('id'))

    # Obtener la cantidad de registros por región
    records_by_region = Record.objects.values('province').annotate(count=Count('id'))

    context = {
        'total_records': total_records,
        'records_by_country': records_by_country,
        'records_by_city': records_by_city,
        'records_by_region': records_by_region,
    }

    return render(request, 'webapp/stadistic-views.html', context=context)


def contact_us_page(request): 

    return render(request, 'webapp/contact-us.html')
  

class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

def pdf(request):
    # Obtén todos los registros desde la base de datos
    records = Record.objects.all()

    # Pasa los registros al contexto
    context = {'records': records}

    # Renderiza la plantilla con el contexto
    rendered_html = render(request, 'webapp/pdf.html', context)

    # Genera el PDF a partir del HTML renderizado
    pdf_response = html2pdf(rendered_html.content.decode())

    # Devuelve la respuesta PDF
    if pdf_response.status_code == 200:
        pdf_response['Content-Disposition'] = 'filename="report.pdf"'
        return pdf_response

    return pdf_response