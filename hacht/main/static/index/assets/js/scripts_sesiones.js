function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggle_vis(element){
    if (element.css("display") == 'none'){
        element.css("display", 'inline');
    }
}

function highlight_titles(element){

    // strings to query each "comp_paciente" that is each container of "Sesion" objects
    all_element = "#contenedor_sesiones .comp-paciente"
    str = all_element + " .titulo-descriptivo"

    // first all selected values get de-selected
    $(all_element).css("border", "0px");
    $(str).css("background-color", "rgb(233,236,239)");
    $(str).css("color", "rgb(73,80,87)");

    str = element + " .titulo-descriptivo"
    
    // Then the selected value will show a "selected state"
    $(element).css("border","solid 1px");
    $(element).css("border-color", "rgb(0,123,255)");
    $(str).css("background-color", "rgb(0,123,255)");
    $(str).css("color", "white");
}

function agregar_sesion(id_paciente){

    // Carga el formulario
    cargar_form_sesion("components/descriptivo_sesion/", id_paciente, "")

    // Hace que la columna sea visible
    toggle_vis($("#contenedor_sesion_completo"));

}

function cargar_form_sesion(url, id_paciente, id_sesion){

    if (id_paciente) {
        apendice = "?id_paciente=" + id_paciente

        if (id_sesion){ 

            // Alista el request GET mediante una url
            apendice += "&id_sesion=" + id_sesion

            // Carga el formulario con los datos "prellenados"
            $("#cont_sesion").load(url+apendice, function(responseTxt, statusTxt, xhr){
                if(statusTxt == "error")
                    alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
            });

        }else{

            // Carga el formulario sin datos
            $("#cont_sesion").load(url+apendice, function(responseTxt, statusTxt, xhr){
                if(statusTxt == "error")
                    alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
            });
        }
    } else {

        if (id_sesion){ 

            // Alista el request GET mediante una url
            apendice = "?id_sesion=" + id_sesion

            // Carga el formulario con los datos "prellenados"
            $("#cont_sesion").load(url+apendice, function(responseTxt, statusTxt, xhr){
                if(statusTxt == "error")
                    alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
            });
        }else{

            // Carga el formulario sin datos
            $("#cont_sesion").load(url, function(responseTxt, statusTxt, xhr){
                if(statusTxt == "error")
                    alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
            });
        }

    }

}

function cargar_muestras_sesion(url, id_sesion){

    apendice = "?id_sesion=" + id_sesion;

    // Carga el formulario con los datos "prellenados"
    $("#cont_muestras_sesion").load(url+apendice, function(responseTxt, statusTxt, xhr){
        if(statusTxt == "error")
            alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
    });

}

function cargar_analytics_sesion(url, id_sesion){

    apendice = "?id_sesion=" + id_sesion;

    // Carga el formulario con los datos "prellenados"
    $("#cont_analytics_sesion").load(url+apendice, function(responseTxt, statusTxt, xhr){
        if(statusTxt == "error")
            alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
    });

}

function sesion_onclick(id_paciente, id_sesion){

    // Hace un load dinámico del form para cada paciente
    cargar_form_sesion("components/descriptivo_sesion/", id_paciente, id_sesion);

    // Carga las muestras
    cargar_muestras_sesion("components/muestras_sesion/", id_sesion);

    // Carga los graficos y analytics
    cargar_analytics_sesion("components/analytics_sesion/", id_sesion);

    // Muestra la columna de pacientes
    toggle_vis($("#contenedor_sesion_completo"));

    // Resalta algunas características para mostrar que ha sido seleccionado
    highlight_titles("#descriptivo_sesion_" + id_sesion);
}

function inicializar_graficos(data){
    var ctx = $("#canvas_dona");
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: data
    });
}

function eliminar_onclick(e, id_paciente, id_sesion){
    
    // previene el href
    e.preventDefault();
    
    // Confirma que se quiera eliminar el paciente
    var val = confirm("¿Está seguro que desea eliminar la sesión?");
    
    if(val){

        // Realiza un request post para eliminar el paciente
        $.post(
            "eliminar/",
            {
                "id_sesion" : id_sesion
            },
            function(result){
                window.location.replace("/dashboard_sesiones/?id_paciente=" + id_paciente)
            }
        );
    }
}

function image_on_click(id_img){

    // Get the modal
    var modal = document.getElementById("myModal");

    var img = document.getElementById(id_img);
    var modalImg = document.getElementById("img01");
    var captionText = document.getElementById("caption");

    modal.style.display = "block";
    modalImg.src = img.src;
    captionText.innerHTML = img.alt;

}

function span_on_click(){

    // Get the modal
    var modal = document.getElementById("myModal");

    modal.style.display = "none";
}

$(document).ready(function() { 

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    

}); 
