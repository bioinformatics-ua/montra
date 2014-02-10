var database_name = null;
var qs_number_pattern = /open-button_validator_(\d+).01/i;

$(document).ready(function(){

    $(".open-button_validator").each(function(i, v) {        
        if(database_name == null){
            var question_number = $(v).attr("id").replace("open-button_validator_", "question_")
            question_number = question_number.replace(".","\\.");
            
            database_name = $('#'+question_number).val();
        }
    });

    $("#qform").submit(function(evnt){
        validateForm(evnt);
    });

});

function validateForm(evnt){
    $(".open-button_validator").each(function(i, v) {
        var validator_id = $(v).attr("id");
        if( !validate( validator_id.replace("open-button_validator_", "question_"))){
            evnt.preventDefault();     
            var result = validator_id.match(qs_number_pattern);
            if(result.length == 2){
                questionsets_handle( $("#qs_"+result[1]).get(0) );        
            }
        }
    });
}

function draw_validator(validator, validated, feedback_message){
    if (validated)
    {
        validator.removeClass("error");
        validator.addClass("success");
        $("span", validator).text(feedback_message);
    } else {        
        validator.removeClass("success");
        validator.addClass("error");
        $("span", validator).text(feedback_message);
    }
}

function validate(question_number)
{
    question_number = question_number + "";
    question_number = question_number.replace(".","\\.");
    var text = $('#'+question_number).val();
    
    //getValidator
    var validator = $('#open-button_validator_'+question_number.replace("question_",""));
    var feedback_message;          
    var validated = false;

    if(text.length == 0){
        draw_validator(validator, false , "Database name must not be empty");
        return false
    }
    if(text == database_name){
        draw_validator(validator, true , "");       
        return true;
    }
    //console.log($('#'+question_number).val());

    $.ajax({
        type: 'GET',
        url: 'api/validate?name='+text,
        dataType: 'json',
        success: function(data) {
              //console.log(data['contains'])
              
              if (data['contains'] == false)
              {
                validated = true;
                draw_validator(validator, validated, "Database Name Available.");
              }else{
                validated = false;
                draw_validator(validator, validated, "Database Name already exists.");
              }     
            },
        data: {},
        async: false
    });

    return validated;
};