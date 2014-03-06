/**
    tablediff.js
    Copyright (C) 2013 - Luís A. Bastião Silva and Universidade de Aveiro

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see
<http://www.gnu.org/licenses/>
.
 */

/**
 * Compare each cell of the table 
 * @param  {[type]} table     [description]
 * @param  {[type]} cell_name [description]
 * @param  {[type]} value     [description]
 * @return {[type]}           1 = 
 */
compare_cell = function(table, cell_name, value)
{	
	var result_final = 0;
	//console.log("Cellname: " + cell_name.data);
	//console.log("Value: " + value.data);
	   $('#'+ table).each(function() {
	  	//console.log($(this.childNodes[3].childNodes));
	  	 $(this.childNodes[3].childNodes).each(function()
	  	{
	  		//console.log($(this.childNodes));
			 $(this).each(function()
		  	{	
		  			if (this.tagName=="TR")
		  			{
		  				//$('#t11').addClass("warning");
		  				//$(this.childNodes[1]).addClass("success");
		  				try
		  				{
		  				if ($(this.childNodes[1].childNodes[0]).context.data==cell_name.data)
		  				{
		  					//console.log("FOUND: " + value.data);
		  					//console.log($(this.childNodes[3].childNodes[0])[0].textContent);
		  					//console.log($(this.childNodes[3].childNodes[0])[0].textContent.indexOf(value.data));
		  					//if (value.data.indexOf($(this.childNodes[3].childNodes[0]).context) !== -1))
							if ($(this.childNodes[3].childNodes[0])[0].textContent.indexOf(value.data) !== -1 && $(this.childNodes[3].childNodes[0])[0].textContent === value.data)
		  					{
		  						//console.log("True: " + value.data);
		  						//$(this.childNodes[1]).addClass("success");
		  						result_final = 1;
		  						return false;
		  					}
		  					else if (($(this.childNodes[3].childNodes[0])[0].textContent.indexOf(value.data) >= 0 || value.data.indexOf($(this.childNodes[3].childNodes[0])[0].textContent) >= 0 ) && $(this.childNodes[3].childNodes[0])[0].textContent !== value.data)
		  					{
		  						//$(this.childNodes[1]).addClass("warning");
		  						result_final = 2;
		  						return result_final;
		  					}
		  					//$(this.childNodes[1]).addClass("error");
		  					$(this.childNodes[1]).add("found");
		  					//console.log($(this.childNodes[1]));
		  				}
		  				//console.log($(this.childNodes[1].childNodes[0]).context);
		  				//console.log($(this.childNodes[3].childNodes[0]).context);
		  				}
		  				catch (err) 
		  				{
		  					//console.log(err.message)

		  				}
		  				//console.log($(this));	
		  			}
		  	}	  
		  	);		
	  		
	  	}
	  	
	  	);
	  });
	  return result_final;
}





/**
 * Compare the table and change the colours according to the differencess
 * @param  {[type]} table1 [description]
 * @param  {[type]} table2 [description]
 * @return {[type]}        [description]
 */
comparetable = function(table1, table2){
	// Compare two tables: highlight the differences
	$(function() {

	  $('#'+ table1).each(function() {
	  	//console.log($(this.childNodes[3].childNodes));
	  	$(this.childNodes[3].childNodes).each(function()
	  	{	
	  		//console.log($(this.childNodes));
			$(this).each(function()
		  	{	
		  			if (this.tagName=="TR")
		  			{
		  				//console.log($(this.childNodes[1].childNodes[0]).context);
		  				//console.log($(this.childNodes[3].childNodes[0]).context);
		  				
		  				var result = compare_cell(table2, $(this.childNodes[1].childNodes[0]).context,$(this.childNodes[3].childNodes[0]).context);
		  				console.log('Result: ' + result );
		  				if (result==1)
		  				{

		  					console.log($('#' + table2));

		  					//$('#' + table2).childNodes[1].childNodes[0]).addClass("success")
		  					//$($('#' + table2).childNodes[1].childNodes[0]).addClass("success");
		  					$(this).addClass("success");
		  				}
		  				else if (result==2){
		  					//$($('#' + table2).childNodes[1].childNodes[0]).addClass("warning");
		  					$(this).addClass("warning");
		  				}
		  				else{
		  					//$($('#' + table2).childNodes[1].childNodes[0]).addClass("error");
		  					$(this).addClass("error");
		  				}
		  	}
		  	}	  
		  	);		
	  		
	  	}

	);
    var content;
    content = $(this).text().replace(/\s+/gi, ' ');
    //console.log(content)


  });
  $('#'+ table2).each(function() {

    var content;
    content = $(this).text().replace(/\s+/gi, ' ');
    //console.log(content)

  });
	  
	});

};

paint_table2 = function(table2, tag, nameClass)
{
	$('#'+ table2).each(function() {
		$(this.childNodes[3].childNodes).each(function()
	  	{	

	  		$(this).each(function()
		  	{
		  		if (this.tagName=="TR")
		  		{
		  			//console.log($(this.childNodes[1].childNodes[0]).context.data );
		  			//console.log(tag);
		  			//if ($(this.childNodes[1].childNodes[0]).context.nodeValue.indexOf(tag)!==-1)
		  			try
		  			{
		  			if (tag.indexOf($(this.childNodes[1].childNodes[0]).context.data)!==-1)
		  			{
		  					//console.log("maasa");

		  				$(this).addClass(nameClass);
		  			}
		  			}
		  			catch (err)
		  			{}
		  		}
		  	});
	  	});
	});

};

comparetable_two = function(table1, table2){
	// Compare two tables: highlight the differences
	$(function() {

	  $('#'+ table1).each(function() {
	  	//console.log($(this.childNodes[3].childNodes));
	  	$(this.childNodes[3].childNodes).each(function()
	  	{	
	  		//console.log($(this.childNodes));
			$(this).each(function()
		  	{	
		  			if (this.tagName=="TR")
		  			{
		  				//console.log($(this.childNodes[1].childNodes[0]).context);
		  				//console.log($(this.childNodes[3]));
		  				
		  				var result = compare_cell(table2, $(this.childNodes[1].childNodes[0]).context,$(this.childNodes[3].childNodes[0]).context);
		  				//console.log('Result: ' + result );
		  				if (result==1)
		  				{

		  					//console.log($('#' + table2));
		  					//console.log($('#' + table1));
		  					paint_table2(table2,$(this.childNodes[1].childNodes[0]).context.data, "success" );

		  					//$('#' + table2).childNodes[1].childNodes[0]).addClass("success")
		  					//$($('#' + table2).childNodes[1].childNodes[0]).addClass("success");
		  					$(this).addClass("success");
		  				}
		  				else if (result==2){
		  					//$($('#' + table2).childNodes[1].childNodes[0]).addClass("warning");
		  					$(this).addClass("warning");
		  					
		  					paint_table2(table2,$(this.childNodes[1].childNodes[0]).context.data, "warning" );
		  				}
		  				else{
		  					//$($('#' + table2).childNodes[1].childNodes[0]).addClass("error");
		  					$(this).addClass("error");
		  					
		  					paint_table2(table2,$(this.childNodes[1].childNodes[0]).context.data, "error" );
		  				}
		  			}
		  	}	  
		  	);		
	  		
	  	}

	);


    var content;
    content = $(this).text().replace(/\s+/gi, ' ');
    //console.log(content)


  });
  $('#'+ table2).each(function() {

    var content;
    content = $(this).text().replace(/\s+/gi, ' ');
    //console.log(content)

  });
	  
	});

};

/**
 * [ description]
 * @param  {[type]} table_base  [description]
 * @param  {[type]} list_tables [description]
 * @return {[type]}             [description]
 */
tablediffall = function(table_base, list_tables)
{
	$(list_tables).each(function(table_tmp)
	{
		comparetable(list_tables[table_tmp],table_base);		
	});	

};

tablediffall_two = function(table_base, list_tables)
{
	$(list_tables).each(function(table_tmp)
	{
		comparetable_two(table_base, list_tables[table_tmp]);		
	});	
	
};





/**
 * Clean the formats of a table
 * @param  {[string]} list_tables List of tables
 * @return {[None]}             None
 */
cleantablediff = function(list_tables)
{
	$(list_tables).each(function(table_tmp)
	{
		//console.log(list_tables[table_tmp]);
		$('#'+ list_tables[table_tmp]).each(function() 
		{
	  	//console.log($(this.childNodes[3].childNodes));
	  	$(this.childNodes[3].childNodes).each(function()
	  	{
	  		//console.log($(this.childNodes));
			$(this).each(function()
		  	{	
		  			if (this.tagName=="TR")
		  			{
		  				//console.log(this);
		  				$(this).removeClass("success");
	  					$(this).removeClass("error");
		  			}
		  	});		
	  	});

	});
	});

};

function hide_uncessary_qs(list_tables, table_tmp){
	var visibles_left = $('#' + list_tables[table_tmp] + ' tr:visible').length;


	if(visibles_left <= 0){
		$('#' + list_tables[table_tmp]).parent().parent().parent().hide();
	}
}

function hideTableCell(list_tables, table_tmp, word){
	$("#" + list_tables[table_tmp]+" tr").each(function() {        
		    var cell = $.trim($($(this).find('td')[0]).text()).toLowerCase();
		    //console.log(cell + "==" + word +"?");
		    if (cell.indexOf(word.toLowerCase()) == -1)
		       // $(this).closest('tr').show();    
		    //else
		    	$(this).closest('tr').hide();	 
		                       
	});
}

function hideEmptyCells(list_tables, table_tmp, show_emptyrows){
		$("#" + list_tables[table_tmp]+" tr").each(function() {  

			var classes = $(this).prop("class").split(' ');
			var this_class;
			for(var i=0;i<classes.length;i++){
				if(classes[i].indexOf('rowid_') != -1)
					this_class=classes[i];
			}
			console.log(this_class);
			var no_value = true;
			$("."+this_class).each(function() {
			    var cell = $.trim($($(this).find('td')[1]).text());

	 		    if (cell.length != 0){
			    	no_value = false;
			    } 
			});
			if(no_value){
			        if (show_emptyrows)
			        {
			        	$("."+this_class).show();
			        }
			        else
			        {
			        	$("."+this_class).hide();	
			        }
			}
 
		});
}

/* This function concatenates all previous functions of filtering in a unique function... 
   It was getting hard to synchronize everything when we only have the information on the 
   	dom and all was separated 
*/
function filter_results(list_tables, word, show_match, show_unmatch, show_emptyrows, show_proximity){

	$(list_tables).each(function(table_tmp)
	{
		// First we reset
		$('#' + list_tables[table_tmp]).parent().parent().parent().show();
		$('#' + list_tables[table_tmp] + " entry").show();
		// match
		if (show_match)
		{
			$('#' + list_tables[table_tmp] + ' .success').show();	
		}
		else
		{
			$('#' + list_tables[table_tmp] + ' .success').hide();	
		}

		// unmatch
		if (show_unmatch)
		{
			$('#' + list_tables[table_tmp] + ' .error').show();	
		}
		else
		{
			$('#' + list_tables[table_tmp] + ' .error').hide();	
		}

		// proximity
		if (show_proximity)
		{
			$('#' + list_tables[table_tmp] + ' .warning').show();	
		}
		else
		{
			$('#' + list_tables[table_tmp] + ' .warning').hide();	
		}
		
		// emptyrows
		hideEmptyCells(list_tables, table_tmp, show_emptyrows);
		
		
		// filter
		hideTableCell(list_tables, table_tmp, word);
	
		// remove unnecessary tables (empty)
		hide_uncessary_qs(list_tables, table_tmp);

	});
}


