


App.prototype.ajaxGetEvents=function(targetid){
    $.ajax({type: 'GET',
        url:'/ajax',
        data:{
            method:'eventtype',
            parameters: ''
        },
        success:function(data){
            data = jQuery.parseJSON(data);
            targetid.attr('disabled','disabled');
            targetid.empty();
            if(data.result.length==0){
                return;
            }
            for(i in data.result){
                targetid.append('<option value="'+data.result[i]+'">'+data.result[i]+'</option>');
            }
            targetid.removeAttr('disabled')
        }
    })
}