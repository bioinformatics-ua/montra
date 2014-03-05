/*
 * delayKeyup
 * http://code.azerti.net/javascript/jquery/delaykeyup.htm
 * Inspired by CMS in this post : http://stackoverflow.com/questions/1909441/jquery-keyup-delay
 * Written by Gaten
 * Exemple : $("#input").delayKeyup(function(){ alert("5 secondes passed from the last event keyup."); }, 5000);
 */
(function ($) {
    $.fn.delayKeyup = function(callback, ms){
        var timer = 0;
        $(this).keyup(function(){                   
            clearTimeout (timer);
            timer = setTimeout(callback, ms);
        });
        return $(this);
    };
})(jQuery);                   

function PaginatorSorter(tableID, fString, selName, selValue){
    this.innerTable = $("#"+tableID);

    this.filters = [];
    this.filters.push("database_name_filter");// = $("#database_name_filter",this.innerTable);
    this.filters.push("last_update_filter");// = $("#last_update_filter",this.innerTable);
    this.filters.push("type_filter");// = $("#type_filter",this.innerTable);

    this.selName = selName;
    this.selValue = selValue;

    this.form = $("#send2");
    this.updateForm(this.getQueryString(selName, selValue));

    this.bind();

    this.fString = fString; 
}
PaginatorSorter.prototype ={
	getQueryString : function(fieldType, value){
		var json = "{";

		if(fieldType == undefined)
			json += '"'+this.selName+'": "'+this.selValue+'"';
		else 
			json += '"'+fieldType+'": "'+value+'"';


		for(var i=0;i<this.filters.length;i++){// in this.filters){ 
			try
			  {
			  	var content = $("#"+this.filters[i],this.innerTable);
					json += ',"'+this.filters[i]+'": "'+content.val()+'"';
			}		 
			catch(err)
			 {
			  	console.log("Found filter that doesnt exist, ignoring.");
			 }

		}
		json += "}";
		
		console.log(json);
		
		return json;
	},
	onClick : function(fieldType, value){
		var context = this;
		var data = [];

		var json = context.getQueryString(fieldType, value);

		var patt=/\/(\d+)/g;
		var page = patt.exec(window.location.href);
		if( page){
			page = page[1];
		}else{
			page = 1;
		}
		
		var f = this.fString;
		$.ajax({
			type: "POST",
  			dataType: "json",
  			url: "query/"+page,
  			data: {'csrfmiddlewaretoken': $.cookie('csrftoken'), "filter": f, "s":json},
  			success: function(data){	
  				//console.log(data);
  				if(data.Hits != undefined && data.Hits > 0){ 			
			        context.updateForm(json);
			      
			        /*for(filter in context.filters){ 	
						if(context.filters[filter].val().length > 0 ){
							var x = $("#"+filter+"_grp");
							x.removeClass("error");
						}
					}*/
				  console.log('SUCCESS');
				  context.submitthis();
  				}else{
  					$("#table_content").html('<td colspan="9999"><center>No results to show</center></td>');
  					$(".pagination").html('<td colspan="9999"><center>No results to show</center></td>');
  					console.log('NOTSUCCESS');
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
	} ,
	bind : function(){

		var value = $("#type_filter",this.innerTable).attr("def_value");

		$("option[value="+value+"]", $("#type_filter",this.innerTable)).attr("selected", "yes");

		var context = this;

		$("#database_name_filter",this.innerTable).delayKeyup(function(){ context.onClick(context.selName, context.selValue); }, 500);


    	$("#last_update_filter",this.innerTable).delayKeyup(function(){ context.onClick(context.selName, context.selValue); }, 500);

    	$("#type_filter",this.innerTable).change(function(){
				context.onClick(context.selName, context.selValue);
			});
	}, 
	updateForm : function(json){
		$("#s", $("#send2")).val(json);
	}, 
	submitthis : function(){

		//this.form.submit();
		//$("#send2").submit();
		$("#send2").trigger('submit');
		//$("#submit_simulate").click();
		
	}
}

function paginator_via_post(){
	$("a",".pagination").each(function(){
	      $(this).click(function(e){
	       
	        var href = $(this).attr("href");
	         console.log(href);
	        var patt=/\/(\d+)/g;
	        var page = patt.exec(href);
	        if( page){
	          page = page[1];
	          var form = $("#send2");
	          $("#page", form).val(page);
	          form.submit();
	        }else{
	          page = "NULL";
	        }
	        e.preventDefault();
	      });

	    });
}