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
#
*/
function clean(x){
    if (x== undefined) {
        return 'not defined yet';
    }
    return x;
}

function renderPopup(zone){
    var contentHTML = "";

    contentHTML += '<h4>';
    contentHTML += '<a href="fingerprint/'+zone.id + '/1">' + clean(zone.name) + '</a>';
    contentHTML += '</h4>';


    contentHTML += '<div class="organization-address">';
    //if (_db.institution !='')
    contentHTML += 'Institution name: <b>' + clean(zone.institution) + '</b><br/>';
    //if (_db.contact !='')
    contentHTML += 'Contact: <b>' + clean(zone.contact) + '</b><br/>';
    //if (_db.ttype !='')
    contentHTML += 'DB Type: <b>' + clean(zone.ttype) + '</b><br/>';
    //if (_db.number_patients !='')
    contentHTML += 'Number of patients: <b>' + clean(zone.number_patients) + '</b><br/>';

//# Administrative
//if(!(_db.admin_name =='' && _db.admin_address =='' && _db.admin_email=='' && _db.admin_phone =='')){
    contentHTML += '<div class="geo-well well">';
    contentHTML += '<div class="row">';
    //if (_db.admin_name !='')
    contentHTML += '<i class="icon-user icon"></i> Administrative contact: <b>' + clean(zone.admin_name) + '</b><br />';
    //if (_db.admin_address !='')
    contentHTML += '<i class="icon-home icon"></i> Address: <b>' + clean(zone.admin_address) + '</b><br/>';
    //if (_db.admin_email !='')
    contentHTML += '<i class="icon-envelope icon"></i> Email: <b>' + clean(zone.admin_email) + '</b><br/>';
    //if (_db.admin_phone !='')
    contentHTML += '<i class="icon-phone icon"></i> Phone: <b>' + clean(zone.admin_phone) + '</b><br/>';
    contentHTML += '</div>';
    contentHTML += '</div>';

    contentHTML += '<br />';
//}
//# Scientific
//if(!(_db.scien_name =='' && _db.scien_address =='' && _db.scien_email =='' && _db.scien_phone =='')){
    contentHTML += '<div class="geo-well well">';
    contentHTML += '<div class="row">';
    //if (_db.scien_name !='')
    contentHTML += '<i class="icon-user icon"></i> Scientific contact: <b>' + clean(zone.scien_name) + '</b><br />';
    //if (_db.scien_address !='')
    contentHTML += '<i class="icon-home icon"></i> Address: <b>' + clean(zone.scien_address) + '</b><br/>';
    //if (_db.scien_email !='')
    contentHTML += '<i class="icon-envelope icon"></i> Email: <b>' + clean(zone.scien_email) + '</b><br/>';
    //if (_db.scien_phone !='')
    contentHTML += '<i class="icon-phone icon"></i>  Phone: <b>' + clean(zone.scien_phone) + '</b><br/>';
    contentHTML += '</div>';
    contentHTML += '</div>';
    contentHTML += '<br />';
//}
//# Tecnical
//if(!(_db.tec_name =='' && _db.tec_address =='' && _db.tec_email =='' && _db.tec_phone =='')){
    contentHTML += '<div class="geo-well well">';
    contentHTML += '<div class="row">';
    //if (_db.tec_name !='')
    contentHTML += '<i class="icon-user icon"></i> Tecnical contact: <b>' + clean(zone.tec_name) + '</b><br/>';
    //if (_db.tec_address !='')
    contentHTML += '<i class="icon-home icon"></i> Address: <b>' + clean(zone.tec_address) + '</b><br/>';
    //if (_db.tec_email !='')
    contentHTML += '<i class="icon-envelope icon"></i> Email: <b>' + clean(zone.tec_email) + '</b><br/>';
    //if (_db.tec_phone !='')
    contentHTML += '<i class="icon-phone icon"></i> Phone: <b>' + clean(zone.tec_phone) + '</b><br/>';
    contentHTML += '</div>';
    contentHTML += '</div>';

    contentHTML += '</div>';


    contentHTML += '<br/>';

    return contentHTML;
}

function refreshcontent(pos){
    var internalind = parseInt($('#select'+pos).val());

    console.log("POS X:"+pos);
    console.log('POS Y'+internalind);
    console.log(list_pos[pos][internalind]);
    $('#marker'+pos ).html(renderPopup(list_pos[pos][internalind]));
}

function initialize(list_db) {

    var latlng = new google.maps.LatLng(40, -40);
    var myOptions = {
        zoom: 3,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),myOptions);


    $(list_pos).each(function(pos_tmp)
    {
                        var _list = list_pos[pos_tmp];
                        var marker = new google.maps.Marker({
                                                map: map,
                                                position: new google.maps.LatLng(_list[0].lat, _list[0].long),
                                                title: ''
                                        });




                        google.maps.event.addListener(marker, 'click', (function (marker) {
            return function () {



                // Build content
                var output = '<div id="info-window">';

                if(_list.length > 1){
                    output += '<select id="select'+pos_tmp+'" onchange="refreshcontent('+pos_tmp+')" style="width: 100%;">';
                    for(var i=0;i<_list.length;i++){
                        output += '<option value="'+i+'">'+_list[i].name+'</option>'
                    }
                    output += '</select>';
                }

                output += '<div id="marker'+pos_tmp+'">'+renderPopup(_list[0])+'</div>';

                //}
                output += '</div><br/>';
                infowindow.setContent(output);
                infowindow.open(map, marker);
            }
        })(marker));


    });

}

load_map = function(db_list)
{
    initialize(db_list);
};
