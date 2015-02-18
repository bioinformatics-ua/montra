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

var CommonActionsWidget = function CommonActionsWidget(widgetname, width, height, pos_x, pos_y){

    CommonActionsWidget._base.apply(this, [widgetname, "Common Actions", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.icon = '<i class="fa fa-cogs"></i>';

        self.content = "<center><h3>Loading...</h3></center>";

        CommonActionsWidget._super.__init.apply(self, [gridster, parent]);

        $.get("api/dbtypes")
        .done(function(data) {
            if(data.types){
                self.db_types = data.types;
            } else {
                self.db_types = [];
            }

            self.content=   '<div style="min-width: 180px; vertical-align: top; display: inline-block;"><span class="lead"><i class="fa fa-eye"></i> View</span><br />'+
                        ' <span style="margin-left: 30px;"><a href="databases">Personal Databases</a></span><br />'+
                        ' <span style="margin-left: 30px;"><a href="alldatabases">All Databases</a></span><br />';

            if(hasDatatable)
                self.content += ' <span style="margin-left: 30px;"><a href="alldatabases/data-table">All Databases Datatable</a></span><br />';

            if(hasGeo)
                self.content += ' <span style="margin-left: 30px;"><a href="geo">Databases Geolocation</a></span><br />';

            if(hasPrivate)
                self.content += ' <span style="margin-left: 30px;"><a href="public/fingerprint">Private Links</a></span><br />';

            if(hasExtra)
                self.content += ' <span style="margin-left: 30px;"><a href="api-info">API Information</a></span><br />';

            self.content += '</div><div style="min-width: 200px; vertical-align: top; display: inline-block;"><span class="lead"><i class="fa fa-plus-circle"></i> Add New </span><br />';

            for(var i=0;i<self.db_types.length;i++){
                self.content+= ' <span style="margin-left: 30px;"><a href="add/'+self.db_types[i].id+'/0">'+self.db_types[i].name+'</a></span><br />';
            }


            self.content+=  '</div><div style="min-width: 200px; vertical-align: top; display: inline-block;"><span class="lead"><i class="fa fa-search"></i> Search </span><br />';

            for(var i=0;i<self.db_types.length;i++){
                self.content+= ' <span style="margin-left: 30px;"><a href="advancedSearch/'+self.db_types[i].id+'/1">'+self.db_types[i].name+'</a></span><br />';
            }

            self.content+=  ' <span style="margin-left: 30px;"><a href="advsearch/history">Search History</a></span></div>';

            //console.log(self.content);

            CommonActionsWidget._super.__refresh.apply(self);
          })
        .fail(function() {
            self.content = ' Error loading Common Actions Widget';

            CommonActionsWidget._super.__refresh.apply(self);
        });
    }
});
