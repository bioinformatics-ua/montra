/* Option to active edit fingerprint option */
if ( $("#edit_db_inputs").val() == '1' ) {
    console.log($("#edit_db_inputs").val());
        $("#qform input").prop("disabled", true);
    }

function edit_db_option(){

    console.log($("#edit_db_inputs").val());
    if ( $("#edit_db_inputs").val() == '0' ) {
        $("#qform input").prop("disabled", true);
        $("#edit_db_inputs").val('1');
    } else if ( $("#edit_db_inputs").val() == '1' ) {
        $("#qform input").prop("disabled", false);
        $("#edit_db_inputs").val('0');
    }
}