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
var dashzone;
$(function(){
    dashzone = $("#playground").dashboard(
        {
            showRegistry: true, 
            registryTarget: "#dashboardselectbox"
        });  
    // Registering plugins on dashboard
    dashzone.register(new SimpleTextWidget("feed", "Feed", "Feednews<hr /> Feedanother <hr /> Feed me crazy<hr />Feednews<hr /> Feedanother <hr /> Feed me crazy", 4, 3, 1, 1));
    dashzone.register(new SimpleTextWidget("actions", "Common Actions", "Feednews<hr /> Feedanother <hr /> Feed me crazy", 2, 2, 5, 2));
    dashzone.register(new SimpleTextWidget("concepts", "Concepts", "Feednews<hr /> Feedanother <hr /> Feed me crazy", 2, 1, 5, 3));
    
    var any_configuration = dashzone.loadConfiguration();

    if(any_configuration == false){
        dashzone.addWidget("feed");
        dashzone.addWidget("actions");
        dashzone.addWidget("concepts");
    }
});

/** Emif specific plugins, since they are not part of the isolated generic jquery.dashboard plugin, i put them here */

var CommonActionsWidget = function SimpleTextWidget(widgetname, width, height, pos_x, pos_y){

    CommonActionsWidget._base.apply(this, [widgetname, "Common Actions", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(){



        CommonActionsWidget._super.__init.apply(this);
    }
});
