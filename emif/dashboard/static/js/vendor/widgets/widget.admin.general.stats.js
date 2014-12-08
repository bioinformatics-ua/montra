/*
    # -*- coding: utf-8 -*-
    # Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
    #
    # Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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

var FingerprintSchemasStatsWidget = function FingerprintSchemasStatsWidget(widgetname, width, height, pos_x, pos_y){

    FingerprintSchemasStatsWidget._base.apply(this, [widgetname, "Database Types - Statistics", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.icon = '<i class="fa fa-line-chart"></i>';

        self.content = "<center><h3>Loading...</h3></center>";

        FingerprintSchemasStatsWidget._super.__init.apply(self, [gridster, parent]);

        $.get("api/dbtypes")
        .done(function(data) {
            if(data.types){
                self.db_types = data.types;
            } else {
                self.db_types = [];
            }
            self.content = "";
            $.each(data['types'], function (db){

                $.get("api/statistics/"+data['types'][db].id+"/all/all/all")
                .done(function(dataJson) {
                    self.content += "<strong>"+data['types'][db].name+"</strong> <br/>";
                    if(dataJson.stats){

                        self.content += "Total databases: " + dataJson.stats.totalDatabases + "</br>";
                        self.content += "Total Database owners: " + dataJson.stats.totalDatabaseOwners +"</br>";;
                        self.content += "Total Shared Users: " + dataJson.stats.totalDatabaseShared + "</br>";
                        self.content += "Max DB Shared: " + dataJson.stats.maxDatabaseShared + "</br>";
                        self.content += "Avg DB Shared: " + dataJson.stats.avgDatabaseShared + "</br>";
                        self.content += "Total filled questions: " + dataJson.stats.totalFilledQuestions+ "</br>";
                        self.content += "Max filled questions: " + dataJson.stats.maxFilledFingerprints+ "</br>";
                        self.content += "Average filled questions: " + dataJson.stats.avgFilledFingerprints+ "</br>";
                        self.content += "Total databases users (including shared and database owners): " + dataJson.stats.totalDatabaseUsers+ "</br>";
                        self.content += "Total interested users (all profiles): " + dataJson.stats.totalInterested+ "</br>";

                        self.content += "Max Hits: " + dataJson.stats.maxHitsFingerprints + "</br>";
                        self.content += "Avg Hits: " + dataJson.stats.avgHitsFingerprints + "</br>";
                        self.content += "Total hits: " + dataJson.stats.totalHitsFingerprints + "</br>";

                        self.content += "Max Unique views: " + dataJson.stats.maxUniqueViewsFingerprints + "</br>";
                        self.content += "Avg unique views: " + dataJson.stats.avgUniqueViewsFingerprints + "</br>";
                        self.content += "Total unique views: " + dataJson.stats.totalUniqueViewsFingerprints + "</br>";



                    } else {
                        self.content = "Error Loading User Statistics Widget";
                    }
                    FingerprintSchemasStatsWidget._super.__refresh.apply(self);


                  })
                .fail(function() {
                    self.content = ' Error loading User Statistics Widget';
                    FingerprintSchemasStatsWidget._super.__refresh.apply(self);

                });

            });


        })
        .fail(function() {
            self.content = ' Error loading Stats of the Fingerprint Schema Widget';

            FingerprintSchemasStatsWidget._super.__refresh.apply(self);
        });

    }
});
