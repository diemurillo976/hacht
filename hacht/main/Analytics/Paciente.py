from ..forms import Muestra
import random

def analytics_paciente(request):

    def random_color():

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return 'rgba({}, {}, {}, 255)'.format(r, g, b)

    if request.method == "GET":

        # Gets all "Muestra" objects with its related "Sesion" object
        datos_muestras = Muestra.objects.select_related('sesion').all()

        # Obtains all "Muestra" objects grouped by "pred" field of sesion
        datos_muestras = datos_muestras.values(
            'sesion_id', 'sesion__date', 'pred', 'sesion__id_paciente', 'sesion__id_usuario').annotate(
                cantidad=Count('pred'),
                probabilidad=Count('pred') / Count('id'))

        # Orders the set by cantidad in a descending manner
        datos_muestras = datos_muestras.order_by('-cantidad')

        # Filters the query to only those important to the session at hand
        if request.user.profile.rol == '0':
            id_p = request.GET["id_paciente"]
            datos_muestras = datos_muestras.filter(sesion__id_paciente=id_p)
        else:
            id_u = request.user.id
            datos_muestras = datos_muestras.filter(sesion__id_usuario=id_u)

        # Gets the possible values of "pred" according to Muestra objects
        # As distinct() is not working, we get the predictions and dates and then filter to get only the unique ones
        possible_predictions = datos_muestras.values_list("pred", flat="true").order_by("pred")
        possible_predictions = list(dict.fromkeys(possible_predictions))

        possible_dates = datos_muestras.values_list("sesion__date", flat="true").order_by("sesion__date")
        possible_dates = list(dict.fromkeys(possible_dates))

        datasets = []
        labels_datasets = []

        for prediction in possible_predictions:

            fechas_vistas = []

            if prediction not in labels_datasets:

                data = []

                for date in possible_dates:

                    # These will be the x axis of the plot
                    if str(date) not in labels_datasets:
                        labels_datasets.append(str(date))

                    if str(date) not in fechas_vistas:

                        try:

                            # This is the y axis
                            dato = datos_muestras.get(sesion__date=date, pred=prediction)
                            data.append(dato["cantidad"])

                        except Exception as e:

                            # If the record does not exist then it must be 0
                            data.append(0)

                        fechas_vistas.append(str(date))

                color = random_color()

                dataset = {
                    'data' : data,
                    'label' : prediction,
                    'backgroundColor': color,
                    'borderColor': color,
                    'fill': False
                }

                datasets.append(dataset)

        data_obj = {
            'datasets' : datasets,
            'labels' : labels_datasets
        }

        data_obj = json.dumps(data_obj)

        """
        Obtiene un resumen de los datos para graficar en tipo pie
        Esto significa que obtiene las muestras y lo único que importa es la cantidad de cada tipo
        de tumor existente en la base para el paciente.
        """

        datos_muestras = Muestra.objects.select_related('sesion').all()
        datos_muestras = datos_muestras.values('pred', 'sesion__id_paciente').annotate(
                cantidad=Count('pred'),
                probabilidad=Count('pred') / Count('id'))
        datos_muestras = datos_muestras.order_by('-cantidad')
        datos_muestras = datos_muestras.filter(sesion__id_paciente=id_p)

        data = []
        labels = []
        colors = []

        for dato in datos_muestras:
            data.append(dato['cantidad'])
            labels.append(dato['pred'])
            colors.append(random_color())

        data_pie_obj = {

            'datasets' : [{
                'data' : data,
                'backgroundColor' : colors
            }],

            'labels' : labels,

        }

        data_pie_obj = json.dumps(data_pie_obj)

        context = {
            'datos_muestras' : datos_muestras,
            'data_line' : data_obj,
            'data_pie' : data_pie_obj
        }

        if request.GET.get("android"):
            return render(request, 'index/components/paciente_graficos_app.html', context)
        else:
            return render(request, 'index/components/paciente_graficos.html', context)
