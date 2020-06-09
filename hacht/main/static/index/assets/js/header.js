$(function(){
    $('#header_nav_elem a').each(function(){
        if ($(this).prop('href') == window.location.href){
            $(this).addClass('active');
        }
    });
});