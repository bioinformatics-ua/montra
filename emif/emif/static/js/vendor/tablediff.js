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
compare_cell = function(table, cell_name, value) {
    var result_final = 0;
    //console.log("Cellname: " + cell_name.data);
    //console.log("Value: " + value.data);
    $('#' + table).each(function() {
        $(this).children().eq(1).children().each(function() {

            //$('#t11').addClass("warning");
            //$(this.childNodes[1]).addClass("success");
            try {
                var question = $(this.childNodes[1].childNodes[0]);
                var response = $(this.childNodes[3].childNodes[0]);


                if (question.context.data == cell_name.data) {
                    //console.log(question.context.data + "? --" + (response.length == 0 && (value == undefined || value.data == undefined)));
                    //console.log("FOUND: " + value.data);
                    //console.log($(this.childNodes[3].childNodes[0])[0].textContent);
                    //console.log($(this.childNodes[3].childNodes[0])[0].textContent.indexOf(value.data));
                    //if (value.data.indexOf($(this.childNodes[3].childNodes[0]).context) !== -1))
                    //console.log("COMPARE:[" + response[0].textContent + "][" + value.data + "]");
                    if (response.length == 0 && (value == undefined || value.data == undefined)) {
                        result_final = 3;

                        return false;
                    } else if (response[0].textContent.indexOf(value.data) !== -1 && response[0].textContent === value.data) {
                        //console.log("True: " + value.data);
                        //$(this.childNodes[1]).addClass("success");
                        result_final = 1;
                        return false;
                    } else if (
                        (response[0].textContent.indexOf(value.data) >= 0 ||
                            value.data.indexOf(response[0].textContent) >= 0
                        ) && response[0].textContent !== value.data) {
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
            } catch (err) {
                //console.log(err.message)

            }
            //console.log($(this));		

        });
    });
    return result_final;
}





/**
 * Compare the table and change the colours according to the differencess
 * @param  {[type]} table1 [description]
 * @param  {[type]} table2 [description]
 * @return {[type]}        [description]
 */
comparetable = function(table1, table2) {
    // Compare two tables: highlight the differences
    $(function() {

        $('#' + table1).each(function() {
            $(this).children().eq(1).children().each(function() {
                    //console.log($(this.childNodes[1].childNodes[0]).context);
                    //console.log($(this.childNodes[3].childNodes[0]).context);

                    var result = compare_cell(table2, $(this.childNodes[1].childNodes[0]).context, $(this.childNodes[3].childNodes[0]).context);
                    console.log('Result: ' + result);
                    if (result == 1) {

                        console.log($('#' + table2));

                        //$('#' + table2).childNodes[1].childNodes[0]).addClass("success")
                        //$($('#' + table2).childNodes[1].childNodes[0]).addClass("success");
                        $(this).addClass("success");
                    } else if (result == 2) {
                        //$($('#' + table2).childNodes[1].childNodes[0]).addClass("warning");
                        $(this).addClass("warning");
                    } else if (result == 3) {
                        //$($('#' + table2).childNodes[1].childNodes[0]).addClass("warning");
                        $(this).addClass("emptycells");
                    } else {
                        //$($('#' + table2).childNodes[1].childNodes[0]).addClass("error");
                        $(this).addClass("error");
                    }


                }

            );
            var content;
            content = $(this).text().replace(/\s+/gi, ' ');
            //console.log(content)


        });
        $('#' + table2).each(function() {

            var content;
            content = $(this).text().replace(/\s+/gi, ' ');
            //console.log(content)

        });

    });

};

paint_table2 = function(table2, tag, nameClass) {
    $('#' + table2).each(function() {
        $(this).children().eq(1).children().each(function() {

            //console.log($(this.childNodes[1].childNodes[0]).context.data);
            //console.log(tag);
            //if ($(this.childNodes[1].childNodes[0]).context.nodeValue.indexOf(tag)!==-1)
            try {
                if (tag.indexOf($(this.childNodes[1].childNodes[0]).context.data) !== -1) {

                    $(this).addClass(nameClass);
                    $('.database_listing_names .'+discoverRowId(this)).addClass(nameClass);

                }
            } catch (err) {}

        });
    });

};

function discoverRowId(element){
    var classes = $(element).attr('class').split(' ');

    for(var i=0; i < classes.length;i++){
        if(classes[i].indexOf('rowid_') != -1){
            return classes[i];
        }
    }
}

comparetable_two = function(table1, table2) {
    var empty_rows = 0;
    // Compare two tables: highlight the differences
    $(function() {

        $('#' + table1).each(function() {
            $(this).children().eq(1).children().each(function() {

                    var question = $(this.childNodes[1].childNodes[0]);
                    //var question = $(this).children().first().contents();
                    var response;
                    try {
                        response = $(this.childNodes[3].childNodes[0]);
                    } catch (err) {}
                    //console.log(question);
                    //console.log(response);

                    var result = -2;
                    // if (response && response.length !== 0)
                    result = compare_cell(table2, question.context, response.context);
                    //console.log("RESULT: " + result + "TEST:[" + question.context.data + "]");

                    if (result == 1) {

                        //console.log($('#' + table2));
                        //console.log($('#' + table1));
                        paint_table2(table2, question.context.data, "success");

                        //$('#' + table2).childNodes[1].childNodes[0]).addClass("success")
                        //$($('#' + table2).childNodes[1].childNodes[0]).addClass("success");
                        $(this).addClass("success");
                    } else if (result == 2) {
                        //$($('#' + table2).childNodes[1].childNodes[0]).addClass("warning");
                        $(this).addClass("warning");

                        paint_table2(table2, question.context.data, "warning");
                    } else if (result == 3) {
                        paint_table2(table2, question.context.data, "emptycells");
                        $(this).addClass("emptycells");

                    } else {
                        //$($('#' + table2).childNodes[1].childNodes[0]).addClass("error");
                        $(this).addClass("error");

                        paint_table2(table2, question.context.data, "error");
                    }

                }

            );


            var content;
            content = $(this).text().replace(/\s+/gi, ' ');
            //console.log(content)


        });
        $('#' + table2).each(function() {

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
tablediffall = function(table_base, list_tables) {
    $(list_tables).each(function(table_tmp) {
        comparetable(list_tables[table_tmp], table_base);
    });

};

tablediffall_two = function(table_base, list_tables) {
    // If we are calling it a second time, we must reset this because of base

    $(list_tables).each(function(table_tmp) {
        comparetable_two(table_base, list_tables[table_tmp]);
    });

};





/**
 * Clean the formats of a table
 * @param  {[string]} list_tables List of tables
 * @return {[None]}             None
 */
/*cleantablediff = function(list_tables)
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
	  					$(this).removeClass("warning");
		  			}
		  	});		
	  	});

	});
	});

};*/
/* Isnt this just faster ? */
cleantablediff = function() {
    $('.database_listing .error').removeClass('error');
    $('.database_listing .success').removeClass('success');
    $('.database_listing .warning').removeClass('warning');
    $('.database_listing .emptycells').removeClass('emptycells');
    $('.database_listing .entry').show();
}

function hide_uncessary_qs(list_tables, table_tmp) {
    var visibles_left = $('#' + list_tables[table_tmp] + ' tr:visible').length;


    if (visibles_left <= 0) {
        $('#' + list_tables[table_tmp]).parent().parent().parent().hide();
    }
}

function hideTableCell(list_tables, table_tmp, word) {
    $("#" + list_tables[table_tmp] + " tr").each(function() {
        var cell = $.trim($($(this).find('td')[0]).text()).toLowerCase();
        //console.log(cell + "==" + word +"?");
        if (cell.indexOf(word.toLowerCase()) == -1)
        // $(this).closest('tr').show();    
        //else
            $(this).closest('tr').hide();

    });
}

function hideEmptyCells(list_tables, table_tmp, show_emptyrows) {
    $("#" + list_tables[table_tmp] + " tr").each(function() {

        var classes = $(this).prop("class").split(' ');
        var this_class;
        for (var i = 0; i < classes.length; i++) {
            if (classes[i].indexOf('rowid_') != -1)
                this_class = classes[i];
        }

        var no_value = true;
        $("." + this_class).each(function() {
            var cell = $.trim($($(this).find('td')[1]).text());

            if (cell.length != 0) {
                no_value = false;
            }
        });

        if (no_value) {
            if (!show_emptyrows) {
                $("." + this_class).hide();
            }
        }

    });
}

/* This function concatenates all previous functions of filtering in a unique function... 
   It was getting hard to synchronize everything when we only have the information on the 
   	dom and all was separated 
*/
function reset_results(databases, reference){
    var reference_table = $('table[id^="HEADER_"] ');
    reference_table.each(function(){
        $(this).parent().parent().parent().show();
        $(this).find(" .entry").show();
    });
   var reference_table = $('table[id^="'+reference+'_"] ');
    reference_table.each(function(){
        $(this).parent().parent().parent().show();
        $(this).find(" .entry").show();
    });
    for(var i=0;i<databases.length;i++){
        var tables = $('table[id^="'+databases[i]+'_"] ');

        tables.each(function(){
            $(this).parent().parent().parent().show();
            $(this).find(" .entry").show();
        });

    }
}
/**
 * We only can hide stuff if we dont have any ocurrence of the type on the showing databases

 */
function showMinimumDenominator(condition, class_to_check, table, databases){  

    // Showing is additive
    if(condition == true){
        $(table).find('.'+class_to_check).show();
    } 
    // Adding requires the class_to_check to not appear in any of the lines.
    else {
        $(table).find('.entry').each(function(){
            var row = $(this).data('rowid');

            var fullfills_condition = true;
            $('.rowid_'+row).each(function(){
                // If the row is not the base table, nor the header, and is in the showing list
                // we can consider it for the minimum denominator
                if(
                    !$(this).hasClass('basetable') && $(this).data('fingerprintid') != 'HEADER'

                    && dbindexOf($(this).data('fingerprintid'), databases) != -1

                    ){
                    if(!$(this).hasClass(class_to_check)){
                        fullfills_condition = false;
                        return false;
                    }
                }
            });

            if(fullfills_condition)
                $('.rowid_'+row).hide();
        });
    }
}
function dbindexOf(entry, array){
    for(var i=0;i<array.length;i++){
        if(array[i] == entry)
            return i;
    }
    return -1;
}
function filter_results(databases, reference, word, show_match, show_unmatch, show_emptyrows, show_proximity) {
    console.log('filtering unmatch: '+show_unmatch);
    // reset results
    reset_results(databases, reference);

        var tables = $('table[id^="'+reference+'_"] ');

        tables.each(function(){

            // match
            showMinimumDenominator(show_match,      'success',     this, databases);

            // unmatch
            showMinimumDenominator(show_unmatch,    'error',       this, databases);

            // proximity
            showMinimumDenominator(show_proximity,  'warning',     this, databases);

            // emptyrows
            showMinimumDenominator(show_emptyrows,  'emptycells',  this, databases);            

        });
    


    /*$(list_tables).each(function(table_tmp) {

        // filter
        hideTableCell(list_tables, table_tmp, word);

        // remove unnecessary tables (empty)
        hide_uncessary_qs(list_tables, table_tmp);

    });*/
}