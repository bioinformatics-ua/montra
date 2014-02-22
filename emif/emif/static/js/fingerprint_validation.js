
function OpenButtonValidator(context){
    this.context = context;
    this.database_name = null;
}
OpenButtonValidator.prototype ={
    onInit : function(dom){
        if(this.database_name == null){
            var question_number = $(dom).attr("id").replace("open-button_validator_", "question_")
            question_number = question_number.replace(".","\\.");
            
            this.database_name = $('#'+question_number).val();
        }
    },
    validate : function(question_number, controllerDOM){
        draw_validator = this.context.draw_validator;
        question_number = question_number.replace(".","\\.");
        var text = $(controllerDOM).val();
        
        //getValidator
        var validator = $('#open-button_validator_'+question_number);
        console.log(validator);
        var validated = false;

        if(text.length == 0){
            draw_validator(validator, false , "Database name must not be empty");
            return false
        }
        if(text == this.database_name){
            draw_validator(validator, true , "");       
            return true;
        }

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
    },
    controllerDOM : function(validatorDOM){
        return $("input", validatorDOM);
    }
}

function NumericValidator(context){
    this.context = context;
}
NumericValidator.prototype ={
    onInit : function(dom){
        
    },
    validate : function(question_number, controllerDOM){
        draw_validator = this.context.draw_validator;        
        question_number = question_number.replace(".","\\.");        
        var validator = $('#numeric_validator_'+question_number);
        console.log(validator);
        
        var regex = /\D/i;

        var text = $(controllerDOM).val();
        
        res = regex.exec(text);
        if(res != null)
            draw_validator(validator, false, "This Field must be numeric");
        else
            draw_validator(validator, true, "");
            

        return res == null;
    },
    controllerDOM : function(validatorDOM){
        return $("input", validatorDOM);
    }
}

function Fingerprint_Validator(searchMode){
    this.validators = [];

    this.validators["open-button"] = { n: "open-button_validator", v: new OpenButtonValidator(this)};
    this.validators["numeric"] = { n: "numeric_validator", v: new NumericValidator(this)};
}
Fingerprint_Validator.prototype ={
    onInit : function(){
        var self = this;
        
        for( x in self.validators ){
            $("."+self.validators[x].n).each(function(i, v) {        
                self.validators[x].v.onInit(v);
            });    
        }

        $("#qform").submit(function(evnt){
            console.log(self);
            self.validateForm(evnt);
        });
    },
    validate : function (clas, questionNumber, controllerDOM){
        var validator = this.validators[clas];
        if(validator != undefined){
            validator.v.validate(questionNumber, controllerDOM);
        }
    },
    draw_validator: function(validator, validated, feedback_message){
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
    },
    validateForm: function(evnt){
        self = this;

        for( x in self.validators ){
            $("."+self.validators[x].n).each(function(i, v) {

                var cDOM = self.validators[x].v.controllerDOM(v);
                var validator_id = $(v).attr("id");
                validator_id= validator_id.replace(self.validators[x].n+"_", "");

                console.log(validator_id);

                if( !self.validators[x].v.validate( validator_id, cDOM)){
                    evnt.preventDefault();     

                    var qs_id = validator_id.split(".")[0];

                    console.log(qs_id);
                    questionsets_handle( $("#qs_"+qs_id )[0]);
                }

            });    
        }
    },
    searchMode: function(searchMode){
        if(searchMode == undefined || !searchMode){
            this.validators["open-button"] = { n: "open-button_validator", v: new OpenButtonValidator(this)};
            console.log("Fingerprint_Validator: SearchMode disabled");
        }else{
            delete this.validators["open-button"];        
            console.log("Fingerprint_Validator: SearchMode disabled");
        }
    }
}