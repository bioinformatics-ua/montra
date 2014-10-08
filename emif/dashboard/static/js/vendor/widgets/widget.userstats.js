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

var UserStatsWidget = function UserStatsWidget(widgetname, width, height, pos_x, pos_y){

    UserStatsWidget._base.apply(this, [widgetname, "My Statistics", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.icon = '<i class="fa fa-line-chart"></i>';

        self.content = "<center><h3>Loading...</h3></center>";

        UserStatsWidget._super.__init.apply(self, [gridster, parent]);

        $.get("api/userstats")
        .done(function(data) {
           
            if(data.stats){
                self.content = "<strong>Last Login: </strong>"+data.stats.lastlogin+"<br />"+
                "<strong>Databases owned:</strong> "+data.stats.numberownerdb+"<br />"+
                "<strong>Databases shared with me:</strong> "+data.stats.numbershareddb+"<br />";

                var mostpop = data.stats.mostpopulardb;
                if(mostpop.name != '---'){
                    self.content += '<strong>Most Popular:</strong> <a href="fingerprint/'+mostpop.hash+'/1/">'+
                    mostpop.name +"</a> ("+mostpop.hits+" hits)<br />";
                }

                console.log(data.stats);

                if(data.stats.populartype != '---'){
                    self.content += '<strong>Most Used Quest. Type: </strong>'+data.stats.populartype;
                }

            } else {
                self.content = "Error Loading User Statistics Widget";
            }

            UserStatsWidget._super.__refresh.apply(self);
          })
        .fail(function() {
            self.content = ' Error loading User Statistics Widget';

            UserStatsWidget._super.__refresh.apply(self);
        });
    }
});