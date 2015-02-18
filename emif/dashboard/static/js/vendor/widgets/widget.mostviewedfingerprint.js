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

var MostViewedFingerprintWidget = function MostViewedFingerprintWidget(widgetname, width, height, pos_x, pos_y){

    MostViewedFingerprintWidget._base.apply(this, [widgetname, "Most Viewed Databases", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.icon = '<i class="fa fa-star"></i>';

        self.header_tooltip = "The databases that have more views in your account";

        self.content = "<center><h3>Loading...</h3></center>";

        MostViewedFingerprintWidget._super.__init.apply(self, [gridster, parent]);

        $.get("api/mostviewedfingerprint")
        .done(function(data) {
           self.content = '<table class="table">';
            if(data.mostviewed){
                if(data.mostviewed.length == 0){
                    self.content+='<tr><td><center>No history yet. Start navigating in the databases.</center></td></tr>'
                }

                for(var i=0;i<data.mostviewed.length;i++){
                    self.content += '<tr><td style="word-break: break-all;"><small><a href="fingerprint/'+data.mostviewed[i].hash+'/1">'+data.mostviewed[i].name+ "</a></small></td><!--td>" + data.mostviewed[i].count+"</td--></tr>";
                }
            }

            MostViewedFingerprintWidget._super.__refresh.apply(self);

            $('.table', $('#'+self.widgetname)).parent().css('padding', '0px');
          })
        .fail(function() {
            self.content = ' Error loading Most Viewed admin Widget';

            MostViewedFingerprintWidget._super.__refresh.apply(self);
        });
    }
});
