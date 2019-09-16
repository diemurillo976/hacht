from django.shortcuts import render, redirect
from .models import User
from .models import Profile
from .models import Paciente_N
from .forms import RegistrationForm, Data_PacienteN
from django.shortcuts import get_object_or_404
#hola

def index(request):
    return render(request, 'index/index.html')

def login(request):
    return render(request, 'index/login.html')

def registration(request):
    if(request.method == 'POST'):
        form = RegistrationForm(request.POST)

        if(form.is_valid()):

            # Creates the django's user
            new_user = User(username=request.POST['correo'],
                            email=request.POST['correo'],
                            first_name=request.POST['nombre'])

            new_user.set_password(request.POST['password'])
            new_user.save()

            new_user.profile.rol = request.POST["rol"]
            new_user.profile.org = request.POST["org"]

            new_user.save()
            print('NUEVO REGISTRO USER AGREGADO')
            #messages.success(request, _('El usuario ha sido creado con éxito'))

            return redirect('registration_success')

    if(request.method == 'GET'):
        form = RegistrationForm()

    context = {'form' : form}
    return render(request, 'index/registration.html', context)


def registration_success(request):
    return render(request, 'index/registration_success.html')

def dashboard_pacientes(request):

    if request.method == "GET":

        all_patients_n = Paciente_N.objects.all()
        context = {'pacientes': all_patients_n}
        return render(request, 'index/dashboard_pacientes.html', context)
    
    elif request.method == "POST":

        id_p = request.POST["id"]

        if id_p != None:

            instancia_paciente = get_object_or_404(Paciente_N, pk=id_p)
            form = Data_PacienteN(request.POST, instance=instancia_paciente)
        
        else:
            form = Data_PacienteN(request.POST)

        if(form.is_valid()):
            
            """
            new_patient = Paciente_N(id_user=request.user, 
                                    nombre=request.POST["nombre"],
                                    ced=request.POST["cedula"],
                                    sexo=request.POST["sexo"],
                                    edad=request.POST["edad"],
                                    res=request.POST["res"],)
            """

            paciente = form.save()

            paciente.id_user = request.user

            paciente.save()

            return redirect('/dashboard_pacientes/')

        else:
            print(str(form._errors))

def dashboard_sesiones(request):

    return render(request, 'index/dashboard_sesiones.html')

def contact_us(request):
    return render(request, 'index/contact-us.html')

def features(request):
    return render(request, 'index/features.html' )

def descriptivo_paciente(request):
    
    # Si no hay paciente seleccionado se envía el form vacio
    if request.GET.get("id_paciente"):
        
        id_p = int(request.GET["id_paciente"])

        # Obtiene el paciente
        paciente = Paciente_N.objects.get(pk=id_p)

        # Crea el formulario
        form = Data_PacienteN(instance=paciente)

    else:
            
        # Crea el formulario
        form = Data_PacienteN()

    context = {'form': form}
    return render(request, 'index/components/descriptivo_paciente.html', context)