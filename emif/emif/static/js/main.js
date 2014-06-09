function showExportMessage(){
    $('#exporting-message').fadeIn('fast');

    setTimeout(function() {
      $('#exporting-message').fadeOut('fast');  
    }, 4000);
}