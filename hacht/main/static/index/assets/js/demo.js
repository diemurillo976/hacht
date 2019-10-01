function img_onClick(img_url){
    str = 'components/comp_demo/?url=' + img_url;

    $('#cont_demo').load(str, function(responseTxt, statusTxt, xhr){
        if(statusTxt == "error")
        alert("Error: " + xhr.status + ": " + xhr.statusText + "\nCon url: " + str);
    });

}