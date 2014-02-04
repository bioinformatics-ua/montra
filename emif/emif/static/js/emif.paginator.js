 


 // URL Hack to make paginator work with base
$(document).ready(function(){
    $('a[href="#"]').attr('href', function(i, val){
        return window.location + val;
    });
});