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

var RecommendationsWidget = function RecommendationsWidget(widgetname, width, height, pos_x, pos_y){

    RecommendationsWidget._base.apply(this, [widgetname, "Database Recommendations", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.icon = '<i class="fa fa-bullhorn"></i>';

        self.header_tooltip = "The databases that are recommended to you.";

        self.content = "<center><h3>Loading...</h3></center>";

        RecommendationsWidget._super.__init.apply(self, [gridster, parent]);

        $.get("api/recommendations")
        .done(function(data) {
           self.content = '<table class="table">';
            if(data.mlt){
                for(var i=0;i<data.mlt.length;i++){
                    self.content += '<tr><td style="word-break: break-all;"><small><a href="'+data.mlt[i].href+'">'+data.mlt[i].name+ "</a></small></td></tr>";
                }

                if(data.mlt.length ==0){
                    self.content += '<tr><td style="text-align: justify;text-justify: inter-word;">There\'s no recommendations yet.<br /> To have recommendations you need to have databases subscribed.</td></tr>'
                }
            }

            RecommendationsWidget._super.__refresh.apply(self);

            $('.table', $('#'+self.widgetname)).parent().css('padding', '0px');
          })
        .fail(function() {
            self.content = ' Error loading Recommendations Widget';

            RecommendationsWidget._super.__refresh.apply(self);
        });
    }
});
