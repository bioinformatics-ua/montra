$(function(){

    $('#id-remote').click(function(){
        console.log(this.checked);

        if(this.checked){
            $('#remote_path').show();
            $('#local_editor').hide();
        } else {
            $('#remote_path').hide();
            $('#local_editor').show();
        }
    })

});
