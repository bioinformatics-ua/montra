/*
 * delayKeyup
 * http://code.azerti.net/javascript/jquery/delaykeyup.htm
 * Inspired by CMS in this post : http://stackoverflow.com/questions/1909441/jquery-keyup-delay
 * Written by Gaten
 * Exemple : $("#input").delayKeyup(function(){ alert("5 secondes passed from the last event keyup."); }, 5000);
 */

(function($) {
    $.fn.delayKeyup = function(callback, ms) {
        var timer = 0;
        $(this).keyup(function() {
            clearTimeout(timer);
            timer = setTimeout(callback, ms);
        });
        return $(this);
    };
})(jQuery);

function PaginatorSorter(tableID, fString, selName, selValue, xtraData) {
    this.innerTable = $("#" + tableID);

    this.filters = [];
    this.filters.push("database_name_filter"); // = $("#database_name_filter",this.innerTable);
    this.filters.push("last_update_filter"); // = $("#last_update_filter",this.innerTable);
    this.filters.push("type_filter"); // = $("#type_filter",this.innerTable);
    this.filters.push("institution_filter"); // = $("#type_filter",this.innerTable);
    this.filters.push("location_filter"); // = $("#type_filter",this.innerTable);
    this.filters.push("nrpatients_filter"); // = $("#type_filter",this.innerTable);



    this.selName = selName;
    this.selValue = selValue;
    if (xtraData != undefined) {
        try {
            this.extraData = $.parseJSON(xtraData);
        } catch (err) {
            console.log(err);
        }
    }
    this.plugin = undefined;

    this.bind();

    this.form = $("#send2");
    this.updateForm(this.getQueryString(selName, selValue));
    this.fString = fString;
}
PaginatorSorter.prototype = {
    atachPlugin: function(plg) {
        this.plugin = plg;
        console.log(plg);
        plg.setData(this.extraData);

    },
    getQueryString: function(fieldType, value) {
        var json = "{";

        if (fieldType == undefined)
            json += '"' + this.selName + '": "' + this.selValue + '"';
        else
            json += '"' + fieldType + '": "' + value + '"';

        //console.log(json);
        for (var i = 0; i < this.filters.length; i++) { // in this.filters){ 
            try {

                var content = $("#" + this.filters[i], this.innerTable);
                json += ',"' + this.filters[i] + '": "' + content.val() + '"';
                //console.log(content.val());
                //console.log(content);
            } catch (err) {
                console.log("Found filter that doesnt exist, ignoring.");
            }

        }

        if (this.plugin != undefined) {
            var x = this.plugin.getExtraObjects();
            if (x != undefined)
                json += ', "extraObjects":' + JSON.stringify(x);
        }

        json += "}";
        //console.log(json);		
        return json;
    },
    onClick: function(fieldType, value) {
        var context = this;
        var data = [];

        var json = context.getQueryString(fieldType, value);

        var patt = /\/(\d+)/g;
        var page = patt.exec(window.location.href);
        if (page) {
            page = page[1];
        } else {
            page = 1;
        }

        var f = this.fString;
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "query/" + page,
            data: {
                'csrfmiddlewaretoken': $.cookie('csrftoken'),
                "filter": f,
                "s": json
            },
            success: function(data) {
                //console.log(data);
                if (data.Hits != undefined && data.Hits > 0) {
                    context.selName = fieldType;
                    context.selValue = value;

                    //context.updateForm(json);

                    /*for(filter in context.filters){ 	
						if(context.filters[filter].val().length > 0 ){
							var x = $("#"+filter+"_grp");
							x.removeClass("error");
						}
					}*/
                    console.log('SUCCESS');
                    context.submitthis();
                } else {
                    $("#table_content").html('<td colspan="9999"><center>No results to show</center></td>');
                    $(".pagination, .pagination-centered").html('');
                    //console.log('NOTSUCCESS');
                    /*
  					for(filter in context.filters){ 	
						if(context.filters[filter].val().length > 0 ){
							var x = $("#"+filter+"_grp");
							x.removeClass("success");
            				x.addClass("error");
						}
					}
					*/

                }
            }
        });
    },
    bind: function() {

        var value = $("#type_filter", this.innerTable).attr("def_value");
        $("option[value=" + value + "]", $("#type_filter", this.innerTable)).attr("selected", "yes");

        var context = this;

        $("#database_name_filter", this.innerTable).delayKeyup(function() {
            if (context.plugin != undefined) {
                context.plugin.clearSelection();
            }
            context.onClick(context.selName, context.selValue);
        }, 500);


        $("#last_update_filter", this.innerTable).delayKeyup(function() {
            if (context.plugin != undefined) {
                context.plugin.clearSelection();
            }
            context.onClick(context.selName, context.selValue);
        }, 500);

        $("#type_filter", this.innerTable).change(function() {
            if (context.plugin != undefined) {
                context.plugin.clearSelection();
            }
            context.onClick(context.selName, context.selValue);
        });


        $("#institution_filter", this.innerTable).delayKeyup(function() {
            if (context.plugin != undefined) {
                context.plugin.clearSelection();
            }
            context.onClick(context.selName, context.selValue);
        }, 500);
        $("#location_filter", this.innerTable).delayKeyup(function() {
            if (context.plugin != undefined) {
                context.plugin.clearSelection();
            }
            context.onClick(context.selName, context.selValue);
        }, 500);
        
        $("#nrpatients_filter", this.innerTable).delayKeyup(function() {
            if (context.plugin != undefined) {
                context.plugin.clearSelection();
            }
            context.onClick(context.selName, context.selValue);
        }, 500);

        $("#send2").submit(function() {
            context.updateForm();
        });
    },
    updateForm: function(json) {
        //console.log("Setting Value!!!");
        //console.log(json);
        if (json == undefined)
            json = this.getQueryString();

        $("#s", $("#send2")).val(json);
    },
    submitthis: function() {

        //this.form.submit();
        //$("#send2").submit();
        $("#send2").trigger('submit');
        //$("#submit_simulate").click();

    }
}

//This plugin handles the select boxes for the SearchResultsPage
function SelectPaginatorPlugin() {
    this.selectedList = undefined;
    this.typedb = undefined;
}
SelectPaginatorPlugin.prototype = {
    getExtraObjects: function() {
        var self = this;
        var list = [];
        if (this.selectedList != undefined)
            list = list.concat(this.selectedList);

        $("input.checkbox[name^=chk_]").each(function(x, y) {
            var name = $(y).attr("name");
            name = name.substring(4, name.length);
            //console.log(name);

            var index = list.indexOf(name);
            if ($(y).is(":checked")) {
                if (index == -1) {
                    list.push(name);
                    self.typedb = $(y).attr('typedb');
                }


            } else {
                if (index != -1) {
                    var sliced = list.splice(index, 1);
                }
            }
        });

        if (list.length > 0)
            return {
                selectedList: list,
                typedb: self.typedb
            };

        return undefined;
    },
    setData: function(data) {
        //console.log(data);
        if (data != undefined && data.selectedList != undefined) {
            this.selectedList = data.selectedList;

            this.typedb = data.typedb;

            console.log("DEFINED SELECTED LIST: " + this.selectedList);
            this.populateBoxes();
        }
    },
    populateBoxes: function() {
        if (this.selectedList != undefined) {
            var selects = this.selectedList;

            for (var i = 0; i < selects.length; i++) {
                //console.log("input.checkbox[name=chk_"+selects[i]+"]");
                $("input.checkbox[name=chk_" + selects[i] + "]").click();
            }
        }
        if (this.typedb != undefined) {
            $('input.checkbox:not([typedb="' + this.typedb + '"])').prop('disabled', true);
        }
    },
    clearSelection: function() {
        this.selectedList = [];
        this.populateBoxes();
        this.typedb = undefined;

        $("input.checkbox[name^=chk_]").removeProp("checked");
    },
    onFiltering: function() {
        this.clearSelection();
    }
}

function paginator_via_post() {
    var rows = $("#paginator_rows").val();
    //console.log("Rows: "+rows);
    $("#page_rows").val(rows);

    $("#paginator_rows").change(function(){
        $("#page_rows").val($(this).val());
        $("#send2").submit();
    });

    $("a", ".pagination").each(function() {
        $(this).click(function(e) {
            var parent = $(this).parent("li");
            if(parent.hasClass("active") || parent.hasClass("disabled")){
                e.preventDefault();
                return false;
            }
            
            var href = $(this).attr("href");
            console.log(href);
            var patt = /\/(\d+)/g;
            var page = patt.exec(href);
            if (page) {
                page = page[1];
                var form = $("#send2");
                $("#page", form).val(page);
                form.submit();
            } else {
                page = "NULL";
            }
            e.preventDefault();
        });

    });
}