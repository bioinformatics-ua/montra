/* Option to active edit fingerprint option */
if ( $("#edit_db_inputs").val() == '1' ) {
    console.log('INITIAL VAL == 1');
   // console.log($("#edit_db_inputs").val());
    $('[id^="qform"] input').prop("disabled", true);

    $('[id^="qform"] textarea').attr("disabled","disabled");
    
}

function edit_db_option(){
    console.log('EDITING')
//    console.log($("#edit_db_inputs").val());
    if ( $("#edit_db_inputs").val() == '0' ) {
        $('[id^="qform"] input').prop("disabled", true);
        $("#edit_db_inputs").val('1');

	$('[id^="qform"] textarea').attr("disabled","disabled");
    } else if ( $("#edit_db_inputs").val() == '1' ) {
        $('[id^="qform"] input').prop("disabled", false);
	   $('[id^="qform"] textarea').removeAttr("disabled");
        $("#edit_db_inputs").val('0');
    }
}

function edit_db_option_enforce(){
    if ( $("#edit_db_inputs").val() == '1' ) {
        console.log('ENFORCE 1');
        $('[id^="qform"] input').prop("disabled", true);

    $('[id^="qform"] textarea').attr("disabled","disabled");
    } else if ( $("#edit_db_inputs").val() == '0' ) {
        console.log('ENFORCE 0');

        $('[id^="qform"] input').prop("disabled", false);
       $('[id^="qform"] textarea').removeAttr("disabled");
    }
}
