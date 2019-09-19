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
    }else{
        element.css("display", 'none');
    }
}

function highlight_titles(element){

    str = element + " .titulo-descriptivo"
    
    if ($(str).css("color") == "rgb(255, 255, 255)"){
        
        $(element).css("border","0px");
        
        $(str).css("background-color", "rgb(233,236,239)");
        
        $(str).css("color", "rgb(73,80,87)");
    
    }else{
        
        $(element).css("border","solid 1px");
        
        $(element).css("border-color", "rgb(0,123,255)");
        
        $(str).css("background-color", "rgb(0,123,255)");
        
        $(str).css("color", "white");
    }
}

function agregar_paciente(){

    // Carga el formulario
    cargar_form_paciente("components/descriptivo_paciente/", "")

    // Hace que la columna sea visible
    toggle_vis($("#columna_paciente"));

}

function cargar_form_paciente(url, id_paciente){

    if (id_paciente){ 

        // Alista el request GET mediante una url
        apendice = "?id_paciente=" + id_paciente

        // Carga el formulario con los datos "prellenados"
        $("#columna_paciente").load(url+apendice, function(responseTxt, statusTxt, xhr){
            if(statusTxt == "error")
            alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
        });

    }else{

        // Carga el formulario sin datos
        $("#columna_paciente").load(url, function(responseTxt, statusTxt, xhr){
            if(statusTxt == "error")
            alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
        });
    }

}

function descriptivo_paciente_onclick(id_paciente){

    // Hace un load dinámico del form para cada paciente
    cargar_form_paciente("components/descriptivo_paciente/", id_paciente)

    // Muestra la columna de pacientes
    toggle_vis($("#columna_paciente"));

    // Resalta algunas características para mostrar que ha sido seleccionado
    highlight_titles("descriptivo_paciente_" + id_paciente);
}

function eliminar_onclick(e, id_paciente){
    
    // previene el href
    e.preventDefault();
    
    // Confirma que se quiera eliminar el paciente
    var val = confirm("¿Está seguro que desea eliminar el paciente?");
    
    if(val){

        // Realiza un request post para eliminar el paciente
        $.post(
            "eliminar/",
            {
                "id_paciente" : id_paciente
            },
            function(result){
                window.location.replace("/dashboard_pacientes/")
            }
        );
    }
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
    

    /*
    $(".columna_paciente").on("load", function() { 
        
    }); */

    /*
    $(".sesion_compacto").on("dblclick", function() { 
        toggle_vis($(".contenedor_sesion_completo"));
        
        highlight_titles(".sesion_compacto");
    }); */

}); 
