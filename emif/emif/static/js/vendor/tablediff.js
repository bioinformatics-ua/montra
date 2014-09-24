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
function cleanup(string){

    return string.replace(/\n\s*\n/g, '\n').replace(/(  )/gm,"").trim();
}

compare_cell = function(table, cell_name, value) {
    var result_final = 0;
    var row = "";
    //console.log("Cellname: " + cell_name.data);
    //console.log("Value: " + value.data);
    $('#' + table).each(function() {
        $(this).children().eq(1).children().each(function() {
            

            //$('#t11').addClass("warning");
            //$(this.childNodes[1]).addClass("success");
            //try {
                var question = $(this.childNodes[1].childNodes[0]);
                var response = $(this.childNodes[3].childNodes[0]);

                if ($(this).data('qid') === cell_name) {

                    row = discoverRowId($(this));

                    var this_response;
                    var reference_response;
                    try {
                        var this_response = cleanup(response[0].parentElement.textContent).split('\n');
                    } catch(err){
                        this_response = [];
                    }
                    try {
                        var reference_response = cleanup(value.parentElement.textContent).split('\n');
                    } catch(err){
                        reference_response = [];
                    }
                    if (this_response.length == 0 && reference_response.length == 0) {
                        result_final = 3;

                        return {'value': result_final, 'row': row};
                    }
                    else if(this_response.length == 1 && reference_response.length == 1){
                        if (this_response[0].toLowerCase().trim() === reference_response[0].toLowerCase().trim()) {
                            result_final = 1;

                            return {'value': result_final, 'row': row};
                        }
                        else if ( this_response[0].length != 0 && reference_response[0].length != 0 
                                    && (this_response[0].indexOf(reference_response[0]) >= 0 || reference_response[0].indexOf(this_response[0]) >= 0 )
                            ) {

                            result_final = 2;

                            return {'value': result_final, 'row': row};
                        }
                    }
                    else {
                        var matches = 0;
                        for(var i = 0; i < this_response.length;i++){
                            var pos = $.inArray(this_response[i], reference_response);
                            if (pos != -1)
                                matches++;
                        }

                        if(matches === this_response.length && matches === reference_response.length){
                            result_final = 1;

                            return {'value': result_final, 'row': row};

                        } else if(matches > 0){
                            result_final = 2;

                            return {'value': result_final, 'row': row};
                        }
                    }

                    //$(this.childNodes[1]).add("found");
                }	

        });
    });
    return {'value': result_final, 'row': row};
}





/**
 * Compare the table and change the colours according to the differencess
 * @param  {[type]} table1 [description]
 * @param  {[type]} table2 [description]
 * @return {[type]}        [description]
 */
comparetable = function(table1, table2) {
    // Compare two tables: highlight the differences
        $('#' + table1).each(function() {
            $(this).children().eq(1).children().each(function() {
                    //console.log($(this.childNodes[1].childNodes[0]).context);
                    //console.log($(this.childNodes[3].childNodes[0]).context);

                    var result = compare_cell(table2, $(this.childNodes[1].childNodes[0]).context, $(this.childNodes[3].childNodes[0]).context);
                    //console.log('Result: ' + result);
                    if (result == 1) {

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
};

paint_table2 = function(table2, tag, nameClass) {

    $('#'+table2+" "+"."+tag).addClass(nameClass);

    $('.database_listing_names .'+tag).addClass(nameClass);

    // $('#' + table2).each(function() {
    //     $(this).children().eq(1).children().each(function() {

    //         //console.log($(this.childNodes[1].childNodes[0]).context.data);
    //         //console.log(tag);
    //         //if ($(this.childNodes[1].childNodes[0]).context.nodeValue.indexOf(tag)!==-1)
    //         try {
    //             //  console.log(tag);
    //             if (tag.indexOf($(this.childNodes[1].childNodes[0]).context.data) === 0) {
    //                 $(this).addClass(nameClass);
    //                 $('.database_listing_names .'+discoverRowId(this)).addClass(nameClass);

    //             }
    //         } catch (err) {}

    //     });
    // });

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

        $('#' + table1).each(function() {
            $(this).children().eq(1).children().each(function() {

                    var question = $(this.childNodes[1].childNodes[0]);
                    //var question = $(this).children().first().contents();
                    var response;
                    try {
                        response = $(this.childNodes[3].childNodes[0]);
                    } catch (err) {}
                    //console.log(question);
                    var result = -2;
                    // if (response && response.length !== 0)
                    result = compare_cell(table2, $(this).data('qid'), response.context);
                    //console.log(result);

                    if (result.value == 1) {
                        //console.log($('#' + table2));
                        //console.log($('#' + table1));
                        paint_table2(table2, result.row, "success");

                        //$('#' + table2).childNodes[1].childNodes[0]).addClass("success")
                        //$($('#' + table2).childNodes[1].childNodes[0]).addClass("success");
                        /*$(this).addClass("success"); */
                    } else if (result.value == 2) {
                        //$($('#' + table2).childNodes[1].childNodes[0]).addClass("warning");
                        
                        /*$(this).addClass("warning");*/

                        paint_table2(table2, result.row, "warning");
                    } else if (result.value == 3) {

                        paint_table2(table2, result.row, "emptycells");
                        $(this).addClass("emptycells");

                    } else {
                        //console.log("fail");
                        //$($('#' + table2).childNodes[1].childNodes[0]).addClass("error");
                        /*$(this).addClass("error");*/

                        paint_table2(table2, result.row, "error");
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

    //$('.hide_me').removeClass('hide_me');

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

            var fullfills_condition = checkConditions('.rowid_'+row, class_to_check, databases);
            if(fullfills_condition){
                $('.rowid_'+row).hide();
            }
           
        });
    }
}
function showMinimumDenominatorWord(word, table, databases){  

        $(table).find('.entry').each(function(){
            var row = $(this).data('rowid');

            var fullfills_condition = checkWords('.rowid_'+row, word, databases);
            if(fullfills_condition){
                $('.rowid_'+row).hide();
            }
           
        });
    
}
function dbindexOf(entry, array){
    for(var i=0;i<array.length;i++){
        if(array[i] == entry)
            return i;
    }
    return -1;
}
function checkConditions(context, class_to_check, databases){
    var fullfills_condition = true;

    $(context).each(function(){
                // If the row is not the base table, nor the header, and is in the showing list
                // we can consider it for the minimum denominator
                if(!$(this).hasClass('basetable') && $(this).data('fingerprintid') != 'HEADER'

                    && dbindexOf($(this).data('fingerprintid'), databases) != -1

                    ){
                    if(!$(this).hasClass(class_to_check)){
                        fullfills_condition = false;
                        return false;
                    }
                }
    });

    return fullfills_condition;
}
function checkWords(context, word, databases){
    var fullfills_condition = true;

    $(context).each(function(){
                // If the row is not the base table, nor the header, and is in the showing list
                // we can consider it for the minimum denominator
                if(!$(this).hasClass('basetable') && $(this).data('fingerprintid') != 'HEADER'

                    && dbindexOf($(this).data('fingerprintid'), databases) != -1

                    ){
                        var cell = $.trim($($(this).find('td')[0]).text()).toLowerCase();
                        //console.log(cell + "==" + word +"?");
                        if (cell.indexOf(word.toLowerCase()) != -1)
                            fullfills_condition = false;
                        return false;
                    }
    });

    return fullfills_condition;
}
function filter_results(databases, reference, word, show_match, show_unmatch, show_emptyrows, show_proximity) {
    //console.log('filtering show_match, show_unmatch, show_emptyrows, show_proximity');
    //console.log(show_match+" - "+show_unmatch+" - "+show_emptyrows+" - "+show_proximity);
    // reset results
    reset_results(databases, reference);

        var tables = $('table[id^="'+reference+'_"] ');

        tables.each(function(){

            // emptyrows
            showMinimumDenominator(show_emptyrows,  'emptycells',  this, databases);    

            // match
            showMinimumDenominator(show_match,      'success',     this, databases);

            // unmatch
            showMinimumDenominator(show_unmatch,    'error',       this, databases);

            // proximity
            showMinimumDenominator(show_proximity,  'warning',     this, databases);

            // filter by word
            showMinimumDenominatorWord(word, this, databases);

            // remove empty containers (not necessary)
            hide_uncessary_qs(this, databases);

        });
    
        // remove unnecessary tables (empty)
        

    /*$(list_tables).each(function(table_tmp) {

        // filter
        hideTableCell(list_tables, table_tmp, word);

        // remove unnecessary tables (empty)
        hide_uncessary_qs(list_tables, table_tmp);

    });*/
}
function hide_uncessary_qs(table, databases) {
    var visibles_left = $(table).find('tr:visible').length;

    //console.log('visibles_left: '+visibles_left);

    if (visibles_left <= 0) {
        var super_parent = $(table).parent().parent().parent();

        var block = super_parent.data('block');

        //console.log(block);

        $('.block_'+block).hide();
    }
}