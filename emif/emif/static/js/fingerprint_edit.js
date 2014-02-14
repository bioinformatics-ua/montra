/* Option to active edit fingerprint option */
if ( $("#edit_db_inputs").val() == '1' ) {
   // console.log($("#edit_db_inputs").val());
    $("#qform input").prop("disabled", true);

    $("#qform textarea").attr("disabled","disabled");
    
}

function edit_db_option(){

//    console.log($("#edit_db_inputs").val());
    if ( $("#edit_db_inputs").val() == '0' ) {
        $("#qform input").prop("disabled", true);
        $("#edit_db_inputs").val('1');

	$("#qform textarea").attr("disabled","disabled");
    } else if ( $("#edit_db_inputs").val() == '1' ) {
        $("#qform input").prop("disabled", false);
	   $("#qform textarea").removeAttr("disabled");
        $("#edit_db_inputs").val('0');
    }
}
