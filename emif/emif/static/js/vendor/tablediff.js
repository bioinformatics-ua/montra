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
		  				$('#t11').addClass("warning");
		  				$(this.childNodes[1]).addClass("success");
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
		  						result_final = 1;
		  						return false;
		  					}
		  					else if ($(this.childNodes[3].childNodes[0])[0].textContent.indexOf(value.data) >= 0 && $(this.childNodes[3].childNodes[0])[0].textContent !== value.data)
		  					{

		  						result_final = 2;
		  						return result_final;
		  					}
		  					$(this.childNodes[1]).addClass("success");
		  					$(this.childNodes[1]).add("found");
		  					//console.log($(this.childNodes[1]));
		  				}
		  				//console.log($(this.childNodes[1].childNodes[0]).context);
		  				//console.log($(this.childNodes[3].childNodes[0]).context);
		  				}
		  				catch (err) 
		  				{
		  					console.log(err.message)

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
		  				//console.log('Result: ' + result );
		  				if (result==1)
		  					$(this).addClass("success");
		  				else if (result==2)
		  					$(this).addClass("warning");
		  				else
		  					$(this).addClass("error");
		  				//console.log($(this));	
		  			}
		  	}	  
		  	);		
	  		
	  	}

	);

  	$('td').each(function()
  	{
  		
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
		  				console.log(this);
		  				$(this).removeClass("success");
	  					$(this).removeClass("error");
		  			}
		  	});		
	  	});

	});
	});

};

function show_hide_match(list_tables, show)
{

	$(list_tables).each(function(table_tmp)
	{

		if (show)
		{
			$('#' + list_tables[table_tmp] + ' .success').show();	
		}
		else
		{
			$('#' + list_tables[table_tmp] + ' .success').hide();	
		}
		
	});
};

function show_hide_unmatch(list_tables, show)
{
	$(list_tables).each(function(table_tmp)
	{
		if (show)
		{
			$('#' + list_tables[table_tmp] + ' .error').show();	
		}
		else
		{
			$('#' + list_tables[table_tmp] + ' .error').hide();	
		}
	});
};

function show_hide_proximity(list_tables, show)
{
	$(list_tables).each(function(table_tmp)
	{
		if (show)
		{
			$('#' + list_tables[table_tmp] + ' .warning').show();	
		}
		else
		{
			$('#' + list_tables[table_tmp] + ' .warning').hide();	
		}
	});
};

function show_hide_empty_rows(list_tables, show)
{
	$(list_tables).each(function(table_tmp)
	{
		console.log(list_tables[table_tmp]);
		$("#" + list_tables[table_tmp]+" tr").each(function() {        
		    var cell = $.trim($($(this).find('td')[1]).text());
		    console.log(cell);
		    if (cell.length == 0){
		        //console.log('empty');
		        //$(this).addClass('nodisplay');
		        if (show)
		        {
		        	$(this).closest('tr').show();
		        }
		        else
		        {
		        	$(this).closest('tr').hide();	
		        }
		        
		    }                   
		});
	});
};



