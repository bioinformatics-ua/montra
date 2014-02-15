/******* All Databases data table specific Javascript ****/
            $(document).ready(function() {

                // Add handlers to the db type selector
                $('#db_type').change(function(){
                    var value_selected = $(this).val();
                    if(value_selected == '0'){
                        $('.qsets').each(function(){
                            $(this).addClass('depon_class');
                        });
                    } else {
                        $('.qsets').each(function(){
                            if($(this).attr('id') == 'q_select_'+value_selected){
                                $(this).removeClass('depon_class');
                                $(this).val('0');
                            } else 
                                $(this).addClass('depon_class');
                        });
                    }
                                            $('#tabular_container').html('<div class="well pull-center">To see a tabular view of all databases, please choose a database type and a questionset.</div>'); 
                });
                $('.qsets').change(function(){
                    var db_selected = $('#db_type').val();
                    var qset_selected = $(this).val();
                    if(qset_selected=='0'){
                        $('#tabular_container').html('<div class="well pull-center">To see a tabular view of all databases, please choose a database type and a questionset.</div>'); 
                    } else {
                    $('#tabular_container').html('<div class="well pull-center">Loading...</div>');
                    $.post( "qs_data_table", {db_type: db_selected, qset: qset_selected })
                      .done(function( data ) {
                        $('#tabular_container').html(data);
                      });
                    }
                });
            });
            