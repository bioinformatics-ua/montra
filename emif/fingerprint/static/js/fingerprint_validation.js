

function OpenButtonValidator(context){
    this.context = context;
    this.database_name = null;
}
OpenButtonValidator.prototype = {
    onInit : function(dom){
        if(this.database_name == null){
            var question_number = $(dom).attr("id").replace("open-button_validator_", "question_")
            question_number = question_number.replace(".","\\.");

            this.database_name = $('#'+question_number).val();
        }
    },
    validate : function(question_number, controllerDOM){
        var draw_validator = this.context.draw_validator;
        question_number = question_number.replace(".","\\.");
        var text = $(controllerDOM).val();

        //getValidator
        var validator = $('[id="open-button_validator_'+question_number+'"]');
        //console.log(validator);
        var validated = false;

        if(text.length == 0){
            draw_validator(validator, false , "Database name must not be empty");
            return false;
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
    },
    setDatabase : function(db){
        this.database_name = db;
    }
}

function NumericValidator(context){
    this.regex = /^\d{1,3}(\'\d{3})*(\.[0-9]+)?$/;
    this.context = context;
}
NumericValidator.prototype ={
    onInit : function(dom){

    },
    validate : function(question_number, controllerDOM){
        var draw_validator = this.context.draw_validator;
        question_number = question_number.replace(".","\\.");
        var validator = $('[id="numeric_validator_'+question_number+'"]');
        //console.log(validator);

        var text = $(controllerDOM).val();
        if(text.length == 0){
            draw_validator(validator, true, "");
            return true;
        }
        var res = this.regex.test(text);
        if(!res){
            draw_validator(validator, false, "This Field must be numeric");
        }else{
            draw_validator(validator, true, "");
        }

        return res;
    },
    controllerDOM : function(validatorDOM){
        return $("input", validatorDOM);
    }
}

function SelfValidator(context){
    this.context = context;
}
SelfValidator.prototype ={
    onInit : function(dom){

    },
    validate : function(question_number, controllerDOM){
        var draw_validator = this.context.draw_validator;
        question_number = question_number.replace(".","\\.");
        var validator = $('[id="self_validator_'+question_number+'"]');

        console.log('validator self');
        var success = validator.find('input').inputmask("isComplete");
        console.log(success);

        return success;
    },
    controllerDOM : function(validatorDOM){
        return $("input", validatorDOM);
    }
}

function EmailValidator(context){
    this.regex = /\S+@\S+\.\S/;
    this.context = context;
}
EmailValidator.prototype ={
    onInit : function(dom){

    },
    validate : function(question_number, controllerDOM){
        var draw_validator = this.context.draw_validator;
        question_number = question_number.replace(".","\\.");
        var validator = $('[id="email_validator_'+question_number+'"]');
        //console.log(validator);

        var text = $(controllerDOM).val();
        if(text.length == 0){
            draw_validator(validator, true, "");
            return true;
        }
        var res = this.regex.test(text);

        if(!res){
            draw_validator(validator, false, "This Field must be an email");
        }else{
            draw_validator(validator, true, "");
        }

        return res;
    },
    controllerDOM : function(validatorDOM){
        return $("input", validatorDOM);
    }
}
function UrlValidator(context){
    /* I didnt make up this regex for url validation, Url validation well done is not trivial,
    so im using Diego Perini well tested solution.
    Ref from: http://pastebin.com/JUKSeB0v */
    this.regex = /^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$/i;
    this.context = context;
}
UrlValidator.prototype ={
    onInit : function(dom){

    },
    validate : function(question_number, controllerDOM){
        var draw_validator = this.context.draw_validator;
        question_number = question_number.replace(".","\\.");
        var validator = $('[id="url_validator_'+question_number+'"]');
        //console.log(validator);

        var text = $(controllerDOM).val().trim();
        if(text.length == 0){
            draw_validator(validator, true, "");
            return true;
        }
        var res = this.regex.test(text);

        if(!res){
            draw_validator(validator, false, "This Field must be an url (starting with http://)");
        }else{
            draw_validator(validator, true, "");
        }

        return res;
    },
    controllerDOM : function(validatorDOM){
        return $("input", validatorDOM);
    }
}
/* To validate urls inside publication,
 * in the future could be expanded to do other kinds of validations on publciations too
 */
function PublicationsValidator(context){
    /* I didnt make up this regex for url validation, Url validation well done is not trivial,
    so im using Diego Perini well tested solution.
    Ref from: http://pastebin.com/JUKSeB0v */
    this.regex = /^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$/i;
    this.context = context;
}
PublicationsValidator.prototype ={
    onInit : function(dom){

    },
    validate : function(question_number, controllerDOM){
        var draw_validator = this.context.draw_validator;
        question_number = question_number.replace(".","\\.");
        var validator = $('[id="url_validator_'+question_number+'"]');
        //console.log(validator);
        console.error('cDom:controllerDOM');
        //console.log(controllerDOM);
        var text = $(controllerDOM).val().trim();
        if(text.length == 0){
            draw_validator(validator, true, "");
            return true;
        }
        var res = this.regex.test(text);

        if(!res){
            draw_validator(validator, false, "This Field must be an url (starting with http://)");
        }else{
            draw_validator(validator, true, "");
        }

        return res;
    },
    controllerDOM : function(validatorDOM){
        return $("input", validatorDOM);
    }
}

function Fingerprint_Validator(searchMode){
    this.validators = [];
    this.fingerprint_name = new OpenButtonValidator(this);

    this.validators["open-button"] = { n: "open-button_validator", v: this.fingerprint_name};
    this.validators["numeric"] = { n: "numeric_validator", v: new NumericValidator(this)};
    this.validators["open-validated"] = { n: "self_validator", v: new SelfValidator(this)};
    this.validators["email"] = { n: "email_validator", v: new EmailValidator(this)};
    this.validators["url"] = { n: "url_validator", v: new UrlValidator(this)};
    this.validators["publication"] = { n: "publication", v: new PublicationsValidator(this)};
}
Fingerprint_Validator.prototype ={
    onInit : function(){
        var self = this;

        for( x in self.validators ){
            $("."+self.validators[x].n).each(function(i, v) {
                self.validators[x].v.onInit(v);
            });
        }

        $('[id^="qform"]').submit(function(evnt){
            //console.log(self);
            self.validateFormContext(evnt, this);
        });
    },
    reload : function(){
        this.onInit();
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
            console.log($("span", validator));
            $("span", validator).text(feedback_message);
        }
    },
    setDatabase : function(db){
        this.fingerprint_name.setDatabase(db);
    },
    validateForm: function(evnt){
        var self = this;

        list = [];
        for( x in self.validators ){
            $("."+self.validators[x].n).each(function(i, v) {

                var cDOM = self.validators[x].v.controllerDOM(v);
                var validator_id = $(v).attr("id");
                validator_id= validator_id.replace(self.validators[x].n+"_", "");

                //console.log(validator_id);

                if( !self.validators[x].v.validate( validator_id, cDOM)){
                    evnt.preventDefault();

                    var qs_id = validator_id.split(".")[0];

                    //console.log(qs_id);
                    //questionsets_handle( $("#qs_"+qs_id )[0]);
                    list.push(validator_id);
                }

            });
        return list;
        }
    },
    validateFormContext: function(evnt, context){
        var self = this;

        list = [];

        for( x in self.validators ){
                if (self.validators[x].n == 'self_validator'){
                    console.log('context');
                    console.log(context);
                }
            $("."+self.validators[x].n, context).each(function(i, v) {
                if (self.validators[x].n == 'self_validator'){
                    console.log(i);
                    console.log(v);
                }
                var cDOM = self.validators[x].v.controllerDOM(v);
                var validator_id = $(v).attr("id");
                validator_id= validator_id.replace(self.validators[x].n+"_", "");

                if( !self.validators[x].v.validate( validator_id, cDOM)){
                    if(evnt)
                        evnt.preventDefault();

                    var qs_id = validator_id.split(".")[0];

                    //console.log(qs_id);
                    //questionsets_handle( $("#qs_"+qs_id )[0]);
                    list.push(validator_id);
                }

            });
        }
        return list;

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
