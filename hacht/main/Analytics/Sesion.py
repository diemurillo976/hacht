from ..forms import Muestra
import random
from django.db.models import Count
import json
from django.shortcuts import render
from ..Clients import ClientFactory


# Auxiliar function to assist the analytics for Sesion
# It gets metrics associated with each class present
def get_metrics(muestras_general):

    # Obtains the "Muestra" objects grouping by "pred" and counting it
    muestras_pred = muestras_general.values('pred').annotate(
        cantidad=Count('pred'))

    # Group by pred_true adding the count of it
    muestras_pred_true = muestras_general.values('pred_true').annotate(
        cantidad=Count('id'))

    muestras_val = muestras_general.values('pred', 'pred_true')

    # Flatten the results
    muestras_p = muestras_pred.values_list('pred', flat=True)
    muestras_pt = muestras_pred_true.values_list('pred_true', flat=True)

    # Gets unique values
    possible_values = list(muestras_p) + list(muestras_pt)
    possible_values = list(dict.fromkeys(possible_values))

    # We have to check if None is a possibility; it makes sense in the model, not in here
    if None in possible_values:
        possible_values.remove(None)

    metrics_dict = {}

    for value in possible_values:

        TP = muestras_val.filter(pred=value, pred_true=value).count()
        FP = muestras_val.filter(pred=value).exclude(pred_true=value).count()
        FN = muestras_val.filter(pred_true=value).exclude(pred=value).count()
        TN = muestras_val.exclude(pred_true=value).exclude(pred=value).count()

        precission = 0

        if (TP + FP) != 0:
            precission = TP / (TP + FP)

        recall = 0

        if (TP + FN) != 0:
            recall = TP / (TP + FN)

        specificity = 0

        if (TN + FN) != 0:
            specificity = TN / (TN + FN)

        f1_score = 0

        if (precission + recall) != 0:
            f1_score = 2 * ((precission * recall) / (precission + recall))

        val_dict = {
            'TP' : TP,
            'FP' : FP,
            'FN' : FN,
            'TN' : TN,
            'precission' : precission,
            'recall' : recall,
            'specificity' : specificity,
            'f1_score' : f1_score
        }

        metrics_dict[value] = val_dict

    return metrics_dict, possible_values

def analytics_sesion(request):

    def random_color():

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return 'rgba({}, {}, {}, 255)'.format(r, g, b)

    if request.method == "GET" and request.GET.get("id_sesion"):

        id_s = request.GET["id_sesion"]

        muestras_general = Muestra.objects.filter(sesion=id_s)

        muestras_no_val = muestras_general.values('pred_true').filter(pred_true=None).annotate(
            cantidad=Count("id")
        )

        try:
            cantidad_no_val = muestras_no_val.values_list("cantidad", flat=True).get(pred_true=None)
        except:
            cantidad_no_val = 0

        datos_muestras = muestras_general.values('pred').annotate(
            cantidad=Count('pred'),
            probabilidad=Count('pred') / Count('id')).order_by('-cantidad')

        data = []
        labels = []
        colors = []

        for dato in datos_muestras:
            data.append(dato['cantidad'])
            labels.append(dato['pred'])
            colors.append(random_color())

        data_obj = {

            'datasets' : [{
                'data' : data,
                'backgroundColor' : colors
            }],

            'labels' : labels,

        }

        data_obj = json.dumps(data_obj)

        val_dict, possible_values = get_metrics(muestras_general)

        context = {
            'datos_muestras' : datos_muestras,
            'data' : data_obj,
            'val_dict' : val_dict,
            'classes' : possible_values,
            'cantidad_no_val' : cantidad_no_val
        }

        client = ClientFactory.get_client(request)

        return client.show_graficos_sesion(request, context)
