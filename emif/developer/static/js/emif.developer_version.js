
$(function(){
    iFrameResize({heightCalculationMethod: 'lowestElement'});

    $('#id-remote').click(function(){
        console.log(this.checked);

        if(this.checked){
            $('#remote_path').show();
            $('#local_editor').hide();
        } else {
            $('#remote_path').hide();
            $('#local_editor').show();
        }
    });

    $('#version-details').submit(function(event){

        var version = $('#id-version').val();
        var is_remote = $('#id-remote')[0].checked;

        var data;

        if(is_remote){
            data = $('#id-path').val();
        } else {
            data = editor.getValue().trim();
        }

        $('#id-code').val(data);

        var url_patt = '^(?!mailto:)(?:(?:http|https|ftp)://)(?:\\S+(?::\\S*)?@)?(?:(?:(?:[1-9]\\d?|1\\d\\d|2[01]\\d|22[0-3])(?:\\.(?:1?\\d{1,2}|2[0-4]\\d|25[0-5])){2}(?:\\.(?:[0-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-4]))|(?:(?:[a-z\\u00a1-\\uffff0-9]+-?)*[a-z\\u00a1-\\uffff0-9]+)(?:\\.(?:[a-z\\u00a1-\\uffff0-9]+-?)*[a-z\\u00a1-\\uffff0-9]+)*(?:\\.(?:[a-z\\u00a1-\\uffff]{2,})))|localhost)(?::\\d{2,5})?(?:(/|\\?|#)[^\\s]*)?$';

        if(version.trim() === '' || isNaN(version)){
            bootbox.alert('You must specify a valid integer number for the version parameter');
            event.preventDefault();
            return false;
        }
        if(
            is_remote &&
            (data > 2000 || !(new RegExp(url_patt).test(data)))
        ){
            bootbox.alert('You must specify a valid URL, starting with http://');
            event.preventDefault();
            return false;
        }

    });

    $('#submit-version').click(function(){
        var desc = $('#approval_desc').val();
        console.log(desc);

        bootbox.confirm('<div class="form"><div class="control-group"><div class="controls">\
            <textarea id="descriptionapp" class="fullwidth" rows="8" \
            placeholder="Write a submission description if deemed necessary.">'+
            desc+'</textarea>\
            </div></div></div>'
        , function(result) {
          if (result) {
            console.log('hey ho');
            $('#approval_desc').val($('#descriptionapp').val());

            $('#submit_me').click();
          }
        });
    });

});
