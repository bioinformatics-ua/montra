function showExportMessage(){
    $('#exporting-message').fadeIn('fast');


// Validation of quicksearch
$('#quicksearch').submit(function() {

        var quick_search = $('#edit-search-block-form--3', $(this)).val().trim();

        if(!quick_search || quick_search.length == 0)
            return false;

        return true;
});

    setTimeout(function() {
      $('#exporting-message').fadeOut('fast');  
    }, 4000);
}

$(function(){
    $.get( "api/notifications", function( data ) {
        console.log("Loading notification center");
        
        if(data.unread && data.unread != 0){
           $('#notification_badge').text(data.unread);
           $('#notification_badge').show();  
        }
        if(data.notifications){
            $('#notification_center').html('<hr />');

            for(var i=0;i<data.notifications.length;i++){
                var new_notification = '<div class="notification';

                    if(!data.notifications[i].read){
                        new_notification+=" notification_unread "
                    }

                    new_notification+='">'+
                    data.notifications[i].message
                    +'<br /> <div class="clearfix"><div class="notification_origin pull-right">by '+data.notifications[i].origin+" at "+data.notifications[i].createddate+
                    '</div></div></div><hr />'

                $('#notification_center').append(new_notification);
            }
        }
        
    });
    
});
