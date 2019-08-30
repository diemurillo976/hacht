function toggle_vis(element){
    if (element.css("display") == 'none'){
        element.css("display", 'inline');
    }else{
        element.css("display", 'none');
    }
}

function highlight_titles(element){
    
    str = element + " .titulo-descriptivo";
    
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

$(document).ready(function() { 
    $(".sesion_compacto").on("click", function() { 
        toggle_vis($(".contenedor_sesion_completo"));
        
        highlight_titles(".sesion_compacto");
    }); 
    
    $(".comp-paciente").on("click", function() { 
        toggle_vis($(".contenedor_paciente"));
        
        highlight_titles("#descriptivo_paciente_1");
    }); 
}); 
