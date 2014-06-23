/******* All Databases data table specific Javascript ****/
// Global variable that nows if the checkboxes are all selected or not
selected_checkboxes = false;

$(document).ready(function() {
    $('#db_type').selectpicker();
    // Add handlers to the db type selector
    $('#db_type').change(function() {
        var value_selected = $(this).val();
        if (value_selected == '0') {
            $('.qsets').each(function() {
                $(this).addClass('depon_class');
                $('#update_table_button').addClass('depon_class');
            });
        } else {
            $('.qsets').each(function() {
                if ($(this).attr('id') == 'q_select_' + value_selected.replace(/\s+/g, '')) {
                    $(this).removeClass('depon_class');
                    //$(this).val('0');
                    $('#update_table_button').removeClass('depon_class');
                } else
                    $(this).addClass('depon_class');
            });
        }
        $('#tabular_container').html('<div class="well pull-center">To see a tabular view of all databases, please choose a database type and questionsets.</div>');
    });

    $('.dropdown-menu').on('click', function(e) {
        if ($(this).hasClass('dropdown-menu-form')) {
            e.stopPropagation();
        }
    });
    $('#update_table_button').click(function() {
        // get db type
        var db_selected = $('#db_type').val();
        // get qsets
        var qsets_selected = [];

        $('.qsets').each(function() {

            if (!$(this).hasClass('depon_class')) {
                $('.qset_option', this).each(function() {
                    if ($(this).prop('checked'))
                        qsets_selected.push(parseInt($(this).val()));
                });
            }

        });

        if (qsets_selected.length == 0) {
            alert("There's no questionsets selected. Please select at least one to see the datatable view.");
            $('#tabular_container').html('<div class="well pull-center">To see a tabular view of all databases, please choose a database type and the questionsets.</div>');
        } else {
            $('#tabular_container').html('<div class="well pull-center">Loading...</div>');
            $.post("qs_data_table", {
                db_type: db_selected,
                qsets: qsets_selected
            })
                .done(function(data) {
                    $('#tabular_container').html(data);
                });
        }

    });

    $('#exportdatatable').click(function() {
        var type_selected = $('#db_type').val();  
        if(type_selected != 0){
            console.log('SELECTED:'+type_selected);

            var selected_options = [];
            $('.qsets').each(function() {

                if (!$(this).hasClass('depon_class')) {
                    $('.qset_option', this).each(function() {
                        if ($(this).prop('checked'))
                            selected_options.push($(this).val());
                    });
                }
            }); 

            console.log(selected_options);  
            var dtform = $('#senddatatable');
            dtform.html($('#senddatatablemodel').html());
            dtform.append('<input type="hidden" name="db_type" value="'+type_selected+'">');
            for(var i=0;i<selected_options.length;i++){
                dtform.append('<input type="hidden" name="qsets[]" value="'+selected_options[i]+'">');
            }
            dtform.submit();


        } else {
            alert('Please, choose a database type and questionsets, before trying to export.')
        }
           
    });

});

function selectall(selectid) {
    if (selected_checkboxes) {

        $('.qset_option', $(selectid)).prop("checked", false);
        selected_checkboxes = false;
    } else {
        $('.qset_option', $(selectid)).prop("checked", true);
        selected_checkboxes = true;
    }
}