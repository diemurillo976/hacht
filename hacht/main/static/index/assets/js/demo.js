function img_onClick(img_index, resultado){

    if (resultado != null){
        str = 'components/comp_demo/?index=' + img_index + '&resultado=' + resultado;
    } else {
        str = 'components/comp_demo/?index=' + img_index;
    }

    $('#col_demo').load(str, function(responseTxt, statusTxt, xhr){
        if(statusTxt == "error")
        alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
    });

    $('#col_demo').css("display", "inline");

}

function analizar_click(){

    $("#cont_bolita").addClass("loader");

    return true;
}

function closeCol(){
    $('.close-icon').on('click', function(){
  
        $('#col_demo').fadeOut();
    })
}
