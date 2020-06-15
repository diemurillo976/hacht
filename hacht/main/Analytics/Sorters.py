from ..CNN_src import TumourClasses as tc
from ..models import Sesion
from ..forms import Muestra

#Función utilizada como criterio de comparación para el sort de muestras en malignas y benignas
def muestras_sort_key(form):
    return tc.class_comparison_dict[form.instance.pred_true] if form.instance.pred_true else tc.class_comparison_dict[form.instance.pred]

#Función utilizada como criterio de comparación para el sort de pacientes, en orden de aquellos con muestras malignas en su sesión más reciente
def pacientes_sort_key(form):
    sesiones = Sesion.objects.filter(id_paciente=form.pk).order_by("-date")
    if(len(sesiones) == 0):
        return -1
    ultima_sesion = sesiones[0]

    for muestra in Muestra.objects.filter(sesion=ultima_sesion.pk):
        if (muestra.pred_true):
            if(tc.class_comparison_dict[muestra.pred_true]):
                return 1
            else:
                continue
        elif(tc.class_comparison_dict[muestra.pred]):
            return 1

    return 0
