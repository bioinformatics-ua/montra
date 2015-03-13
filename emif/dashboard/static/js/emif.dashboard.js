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
var dashzone;
var loaded_arr = [];
var arr_len;


/* this may seem dumb, but we can only run the dashboard after all plugins finished loading
event remote one's with external dependencies that could potentially take a bit.
*/
var dashFull = function(insert){
    loaded_arr.push(insert);

    if(arr_len == loaded_arr.length)
        loadDash();
}
$(function(){
    dashzone = $("#playground").dashboard(
        {
            showRegistry: true,
            registryTarget: "#dashboardselectbox",
            initial: function () {
                dashzone.addWidget("feed");
                dashzone.addWidget("actions");
                dashzone.addWidget("userstats");
                //dashzone.addWidget("mostviewed");
                dashzone.addWidget("mostviewedfingerprint");
                dashzone.addWidget("tagcloud");
            }
        });


    // Registering plugins on dashboard
    dashzone.register(new RecommendationsWidget("recommendations",  2, 1, 6, 6));
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

});

function sandbox(id, data){
    var confs, plugin;
    var self;

    try {
        if(typeof data === 'string'){
            eval(data);
            self = {confs: confs, plugin: plugin};
        }
        else{
            data(function(confs, plugin){
                self = {confs: confs, plugin: plugin};
            })
        }

        if(checkIntegrity(self)){
            self.confs.id = id;
            registerShell(self);
        }
    } catch(exc){
        console.error("The code contains one or several errors, and doesn't execute, please double check your code. Errors are available on console.");
        console.error(exc);
    }
};

function registerShell(closure){
    dashzone.register(
        new PlugShellWidget(
            closure.confs, closure.plugin
        )
    );

    dashFull(closure.confs.id);
}

function checkIntegrity(closure){
    if(!closure.confs || !(typeof closure.confs == 'object'))
        throw 'You must specify a \'confs\' dictionary for the plugin.';

    if(!closure.plugin || !(typeof closure.plugin == 'function'))
        throw 'You must specify a \'plugin\' function for the plugin.';

    return true;
}

function loadDash(){
    console.log('loaddash');
    var any_configuration = dashzone.loadConfiguration();

    if(any_configuration == false){
        dashzone.initial();
    }

    $('#dashboardreset').tooltip({
        'container': 'body'
    });
}
