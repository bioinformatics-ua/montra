$(function(){
    var timer;
    var __delay = function(callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
    var valid_name;
    var valid_type;
    var setSave = function(){
        var save_button = $('#save-plugin');

        if(valid_type && valid_name)
            save_button.removeAttr('disabled');
        else
            save_button.attr('disabled','disabled');


    }
    var iconChanger = function(target, status){
        var icon = $(target);

        switch(status){
            case 'load':
                icon.html('<i class="fa fa-refresh fa-2x fa-spin text-info"></i>');
                break;
            case 'success':
                icon.html('<i title="The value is valid, and can be used." class="fa fa-check fa-2x text-success"></i>');
                break;
            case 'warn':
                icon.html('<i title="The name is already taken. Please choose another" class="tooltippable fa fa-2x fa-times text-error"></i>');
                break;
            case 'fail':
                icon.html('<i title="The value is invalid." class="tooltippable fa fa-2x fa-times text-error"></i>');
                break;
        }
        icon.tooltip({container: 'body'});
    }
    var tryType = function(self){
        var choosen = Number.parseInt($(self).val());
        console.log(choosen);
        switch(choosen){
            case -1:
                valid_type=false;
                iconChanger('#id-type-icon', 'fail'); break;
            default:
                valid_type=true;
                iconChanger('#id-type-icon', 'success'); break;
        }
    };
    $('#id-type').change(function(){ tryType(this)});



    var tryName = function(self) {
            var temptive_name = $(self).val();

            var slug = $('#current_slug').val();

            iconChanger('#id-name-icon', 'load');

            $.post('developer/checkname/', {
                name: temptive_name,
                slug: slug
            })
            .done(function(result) {
                if(result.success){
                    valid_name=true;
                    iconChanger('#id-name-icon', 'success');
                }
                else{
                    valid_name=false;
                    iconChanger('#id-name-icon', 'warn');
                }

            })
            .fail(function() {
                valid_name=false;
                iconChanger('#id-name-icon', 'warn');
            });

        };
    $('#id-name').keyup(function(){
        __delay(tryName(this), 700);
    });
    $('#id-name').change(function(){
        __delay(tryName(this), 700);
    });

    $('#save_plugin').submit(function(event){
        var type = Number.parseInt($('#id-type').val());
        var name = $('#id-name').val();
        if(valid_name == undefined ){
            tryName($('#id-name'));
        }
        if(valid_type == undefined ){
            tryType($('#id-type'));
        }

        if( !valid_name || !valid_type){
            event.preventDefault();

            bootbox.alert('Please confirm if the information filled is valid');
            return false;
        }
    });



    $('#versions').dataTable({
        "bFilter": false,
        "oLanguage": {
            "sEmptyTable": "No versions found for this plugin"
        }
    });

    $("div.toolbar").html('<b>Custom tool bar! Text/images etc.</b>');

    $('#id-name').keyup();
    $('#id-type').change();
});
