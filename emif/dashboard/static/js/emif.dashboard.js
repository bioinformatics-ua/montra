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
            registryTarget: "#dashboardselectbox",
            initial: function () {

                dashzone.register(new RecommendationsWidget("recommendations",  2, 1, 6, 6));

                dashzone.addWidget("feed");
                dashzone.addWidget("actions");
                dashzone.addWidget("userstats");
                //dashzone.addWidget("mostviewed");
                dashzone.addWidget("mostviewedfingerprint");
                dashzone.addWidget("tagcloud");
            }
        });


    // Registering plugins on dashboard
    dashzone.register(new FeedWidget("feed", 4, 2, 1, 1));
    dashzone.register(new CommonActionsWidget("actions", 2, 2, 5, 2));
    dashzone.register(new UserStatsWidget("userstats",  2, 1, 5, 3));

    dashzone.register(new MostViewedWidget("mostviewed",  2, 1, 6, 4));
    dashzone.register(new MostViewedFingerprintWidget("mostviewedfingerprint",  2, 1, 6, 4));

    if(typeof(is_staff) != 'undefined' && is_staff == true){
        dashzone.register(new LastUsersWidget("lastusers",  2, 1, 6, 5));
        dashzone.register(new TopUsersWidget("topusers",  2, 1, 6, 5));
        dashzone.register(new TopNavigatorsWidget("topnavigators",  2, 1, 6, 5));
        dashzone.register(new FingerprintSchemasStatsWidget("fingerprintschemasstats",  2, 1, 6, 5));
    }

    dashzone.register(new TagCloudWidget("tagcloud",  2, 1, 6, 6));

    var any_configuration = dashzone.loadConfiguration();

    if(any_configuration == false){
        dashzone.initial();
    }

    $('#dashboardreset').tooltip({
        'container': 'body'
    });
});

