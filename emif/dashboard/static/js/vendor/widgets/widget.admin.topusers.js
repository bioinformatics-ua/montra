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

var TopUsersWidget = function TopUsersWidget(widgetname, width, height, pos_x, pos_y){

    TopUsersWidget._base.apply(this, [widgetname, "Top Users", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.icon = '<i class="fa fa-user"></i>';

        self.header_tooltip = "Users with most unique views on their databases.<br /><strong> (Only staff can see this widget)</strong>";

        self.header_style = "background-color: #d79494; border: 1px solid #b74c4c;";

        self.content = "<center><h3>Loading...</h3></center>";

        TopUsersWidget._super.__init.apply(self, [gridster, parent]);

        $.get("api/topusers")
        .done(function(data) {
           self.content = '<table class="nomargins table table-bordered">';
            if(data.topusers){
                for(var i=0;i<data.topusers.length;i++){
                    self.content += '<tr><td title="Count: '+data.topusers[i].count+'" style="word-break: break-all;"><small>'+data.topusers[i].user + "</small></td></tr>";
                }
            }

            TopUsersWidget._super.__refresh.apply(self);

            $('.table', $('#'+self.widgetname)).parent().css('padding', '0px');

            $('#'+self.widgetname+' td').tooltip({'container': 'body'});

          })
        .fail(function() {
            self.content = ' Error loading Top Users admin Widget';

            TopUsersWidget._super.__refresh.apply(self);
        });
    }
});
