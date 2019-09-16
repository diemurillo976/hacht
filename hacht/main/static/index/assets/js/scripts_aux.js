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
    toggle_vis($("#columna_paciente"));
}

function cargar_form_paciente(url, id_paciente){

    apendice = "?id_paciente=" + id_paciente

    if (id_paciente){ 

        $("#columna_paciente").load(url+apendice, function(responseTxt, statusTxt, xhr){
            if(statusTxt == "error")
            alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
        });
    }else{
        $("#columna_paciente").load(url, function(responseTxt, statusTxt, xhr){
            if(statusTxt == "error")
            alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
        });
    }

}

function descriptivo_paciente_onclick(id_paciente){
    toggle_vis($("#columna_paciente"));
    highlight_titles("descriptivo_paciente_" + id_paciente);

    cargar_form_paciente("components/descriptivo_paciente/", id_paciente)
}

$(document).ready(function() { 

    cargar_form_paciente("components/descriptivo_paciente/", "")

    /*
    $(".columna_paciente").on("load", function() { 
        
    }); */

    /*
    $(".sesion_compacto").on("dblclick", function() { 
        toggle_vis($(".contenedor_sesion_completo"));
        
        highlight_titles(".sesion_compacto");
    }); */

}); 
