/*
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
/* Option to active edit fingerprint option */
if ( $("#edit_db_inputs").val() == '1' ) {
    console.log('INITIAL VAL == 1');
   // console.log($("#edit_db_inputs").val());
    var vinputs = $('[id^="qform"] input');
    vinputs.prop("disabled", true);
    vinputs.css('color', 'rgb(0, 136, 204)');
    var vtarea = $('[id^="qform"] textarea');
    vtarea.attr("disabled","disabled");
    vtarea.css('color', 'rgb(0, 136, 204)');
    $('.checkbox-label').css('color', 'rgb(0, 136, 204)');

    var sbox = $('input[type="checkbox"]:checked').parent();
    sbox.next().css('color', 'rgb(0, 136, 204)');
    sbox.find('.tick').addClass('tick_disabled');
        var rbox = $('input[type="radio"]:checked').parent();
        rbox.next().css('color', 'rgb(0, 136, 204)');
        rbox.find('.tick').addClass('tick_radio_disabled');
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
        var vinputs = $('[id^="qform"] input');
        vinputs.prop("disabled", true);
        vinputs.css('color', 'rgb(0, 136, 204)');
        var vtarea = $('[id^="qform"] textarea');
        vtarea.attr("disabled","disabled");
        vtarea.css('color', 'rgb(0, 136, 204)');

        var sbox = $('input[type="checkbox"]:checked').parent();
        sbox.next().css('color', 'rgb(0, 136, 204)');
        sbox.find('.tick').addClass('tick_disabled');
        var rbox = $('input[type="radio"]:checked').parent();
        rbox.next().css('color', 'rgb(0, 136, 204)');
        rbox.find('.tick').addClass('tick_radio_disabled');


    } else if ( $("#edit_db_inputs").val() == '0' ) {
        console.log('ENFORCE 0');

        $('[id^="qform"] input').prop("disabled", false);
       $('[id^="qform"] textarea').removeAttr("disabled");
    }
}
