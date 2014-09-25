/*
    # -*- coding: utf-8 -*-
    # Copyright (C) 2014 Ricardo F. Gonçalves Ribeiro and Universidade de Aveiro
    #
    # Authors: Ricardo F. Gonçalves Ribeiro <ribeiro.r@ua.pt>
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

var MostViewedWidget = function MostViewedWidget(widgetname, width, height, pos_x, pos_y){

    MostViewedWidget._base.apply(this, [widgetname, "Most Viewed Pages", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.content = "<center><h3>Loading...</h3></center>";

        MostViewedWidget._super.__init.apply(self, [gridster, parent]);

        $.get("api/mostviewed")
        .done(function(data) {
           self.content = '<table class="table">';
            if(data.mostviewed){
                for(var i=0;i<data.mostviewed.length;i++){
                    self.content += '<tr><td style="word-break: break-all;"><small>'+data.mostviewed[i].page + "</small></td><td>" + data.mostviewed[i].count+"</td></tr>";
                }
            }

            MostViewedWidget._super.__refresh.apply(self);

            $('.table', $('#'+self.widgetname)).parent().css('padding', '0px');
          })
        .fail(function() {
            self.content = ' Error loading Most Viewed admin Widget';

            MostViewedWidget._super.__refresh.apply(self);
        });
    }
});