function PaginatorSorter(tableID, fString, selName, selValue){
    this.innerTable = $("#"+tableID);

    this.filters = [];
    this.filters["database_name_filter"] = $("#database_name_filter",this.innerTable);
    this.filters["last_update_filter"] = $("#last_update_filter",this.innerTable);
    this.filters["type_filter"] = $("#type_filter",this.innerTable);

    this.selName = selName;
    this.selValue = selValue;

    this.bind();

    this.fString = fString; 
}
PaginatorSorter.prototype ={
	onClick : function(fieldType, value){
		var data = [];

		if(fieldType == undefined)
			data[this.selName] = this.selValue;
		else 
			data[fieldType] = value;

		for(filter in this.filters){ 
			console.log(filter);
			if(this.filters[filter].val().length >= 2 ){
				data[filter] = this.filters[filter].val();
			}
		}

		var json = "{"
		first = true
		for(v in data){
			if(!first)
				json += ", "
			json += '"'+v+'": "'+data[v]+'"';
			first = false;
		}
		json += "}";
		//console.log(json);

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
  			data: {"filter": f, "s":json},
  			success: function(data){	
  				//console.log(data);
  				if(data.Hits != undefined && data.Hits > 0)
  					window.location.search="?s="+json;
  			}
		});
	} ,
	bind : function(){
		var value = this.filters["type_filter"].attr("def_value");

		$("option[value="+value+"]", this.filters["type_filter"]).attr("selected", "yes");

		var context = this;
		for(filter in context.filters){ 
			context.filters[filter].change( 
				function(){
					context.onClick()
				});
		}

	}
}