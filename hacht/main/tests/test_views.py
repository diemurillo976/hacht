import codecs
import os
import json
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, Client, RequestFactory
from django.conf import settings as s

from ..forms import RegistrationForm, Data_PacienteN
from ..views import login_app, index, ayuda, handle_error, crear_csv_demo

#from ..Clients.Implementations import Web

class WebTestCase(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.medico = User(username='medico',
                        email='medico@email.com',
                        first_name='NombreMedico')
        self.medico.set_password('12345')
        self.medico.save()

        self.medico.profile.rol = '0' #Rol de doctor
        self.medico.profile.org = 'Ejemplo inc.'
        self.medico.save()


        self.investigador = User(username='investigador',
                        email='investigador@email.com',
                        first_name='NombreInvestigador')

        self.investigador.set_password('12345')
        self.investigador.save()

        self.investigador.profile.rol = '1' #Rol de investigador
        self.investigador.profile.org = 'Ejemplo inc.'
        self.investigador.save()



    def tearDown(self):
        medico = User.objects.get(username='medico')
        investigador = User.objects.get(username='investigador')

        medico.delete()
        investigador.delete()

    def test_loginapp_medico(self):
        self.client.login(username='medico', password='12345')

        response = self.client.get('/login_app/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/dashboard_pacientes/')

    def test_loginapp_investigador(self):
        self.client.login(username='investigador', password='12345')

        response = self.client.get('/login_app/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/dashboard_sesiones/')


    def test_about_us(self):
        response = self.client.get('/about_us/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/about_us.html')

    def test_ayuda(self):
        response = self.client.get('/help/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/help.html')

    def test_handle_error(self):
        response = self.client.get('/help/')
        request = self.factory.get('')
        request.user = AnonymousUser()

        response = handle_error(request, 404, "Mensaje de error.")
        self.assertEquals(response.status_code, 404)

    def test_handle_500_error(self):
        request = self.factory.get('')

        response = handle_error(request, 500, "Mensaje de error.")
        self.assertEquals(response.status_code, 500)

    def test_index_get(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/index.html')

    def test_registration_get(self):
        response = self.client.get('/registration/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/registration.html')

    def test_registration_get_error_con_usuario_iniciado(self):
        self.client.login(username='medico', password='12345')

        response = self.client.get('/registration/')
        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'index/error.html')

    def test_registration_post(self):

        data = {
            'nombre':['Prueba'],
            'correo':['prueba@email.com'],
            'password':['12345'],
            'rol':['0'],
            'org':['Org inc.'],
            'uso':['Uso de prueba.']
        }
        response = self.client.post('/registration/', data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/registration.html')
        self.assertTrue(User.objects.filter(email='prueba@email.com'))

        usuario_creado = User.objects.get(username='prueba@email.com')
        usuario_creado.delete()


    def test_demo_get(self):
        response = self.client.get('/demo/')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/demo.html')

    def test_demo_get_abrir_comp_demo_con_imagen(self):
        response = self.client.get('/demo/components/comp_demo/', {'index': 0})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/components/comp_demo.html')
        self.assertEquals(0, response.context['index'])


    def test_demo_get_con_resultado(self):
        response = self.client.get('/demo/components/comp_demo/', {'index': 0, 'resultado': 0})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/components/comp_demo.html')
        self.assertEquals(0, response.context['index'])
        self.assertEquals('Adenosis', response.context['resultado'])


    def test_demo_post_resultado_img(self):
        data = {
            'index': 0,
            'url':'https://firebasestorage.googleapis.com/v0/b/hacht-570b8.appspot.com/o/Demo_subset%2FSOB_B_A-14-22549G-100-009_0.png?alt=media'
        }

        response = self.client.post('/demo/components/comp_demo/', data)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/demo.html')
        self.assertTrue('resultado' in response.context)


    def test_dashboard_pacientes_get_medico(self):
        self.client.login(username='medico', password='12345')

        response = self.client.get('/dashboard_pacientes/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/dashboard_pacientes.html')


    def test_dashboard_pacientes_get_investigador(self):
        self.client.login(username='investigador', password='12345')

        response = self.client.get('/dashboard_pacientes/')
        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'index/error.html')

    #TODO this fails
    def test_dashboard_pacientes_post_nuevo_paciente(self):
        self.client.login(username='medico', password='12345')
        data = {
            'ced':['12345'],
            'nombre':['Nombre'],
            'res':['Lugar.'],
            'edad':['80'],
            'sexo':['0']
        }

        #response = self.client.post('/dashboard_pacientes/', data)


        #self.assertEquals(response.status_code, 302)
        #self.assertRedirects(response, '/dashboard_pacientes/')


    def test_dashboard_pacientes_post_error(self):
        self.client.login(username='medico', password='12345')
        data = {
            'nombre': ['Nombre'],
            'res': ['Lugar.'],
            'sexo': ['0']
        }

        response = self.client.post('/dashboard_pacientes/', data)

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'index/error.html')


    def test_descriptivo_paciente_get_form_vacio(self):
        response = self.client.get('/dashboard_pacientes/components/descriptivo_paciente/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/components/descriptivo_paciente.html')

    #Todo
    def test_eliminar_paciente(self):
        """
        self.client.login(username='medico', password='12345')
        response = self.client.get('/')
        print("\n PRUEBA", response.context['user'].id)

        data = {
            'ced':['12345'],
            'nombre':['Nombre'],
            'res':['Lugar.'],
            'edad':80,
            'sexo':0
        }


        form = Data_PacienteN(data)
        print(form.errors)
        if (form.is_valid()):
            paciente = form.save()
            paciente.id_user = response.context['user'].id
            paciente.save()


        data = {'id_paciente':paciente.id_user}
        response = self.client.post('/dashboard_pacientes/eliminar/', data)

        self.assertEquals(response.status_code, 204)
    """

    #todo FALTA ID PACIEEEENTEEE
    def test_dashboard_sesiones_get_medico(self):
        """
        self.client.login(username='medico', password='12345')

        response = self.client.get('/dashboard_sesiones/', {'id_paciente':0})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/dashboard_sesiones.html')
        """

    def test_dashboard_sesiones_get_investigador(self):
        self.client.login(username='investigador', password='12345')

        response = self.client.get('/dashboard_sesiones/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/dashboard_sesiones.html')

    def test_dashboard_sesiones_no_sesion(self):
        response = self.client.get('/dashboard_sesiones/')
        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'index/error.html')

    def test_descriptivo_sesion(self):
        pass

    def test_eliminar_sesion(self):
        pass

    def test_muestras_sesion(self):
        pass

    def test_agregar_muestra(self):
        pass

    def test_modificar_muestra(self):
        pass

    def test_contact_us_get(self):
        response = self.client.get('/contact_us/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/contact-us.html')

    def test_features_get(self):
        response = self.client.get('/features/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/features.html')

    def test_crear_csv_demo(self):
        try:
            crear_csv_demo()
            path = s.STATIC_ROOT
            csv_path = os.path.join(path, "index", "assets", "csv", "demo_temp.csv")
            open(csv_path, 'r')
            self.assertTrue(True)

        except:
            self.fail("Metodo no funciona correctamente.")

