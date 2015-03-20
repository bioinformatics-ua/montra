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
function codeError(message, exc){
    $("#playground_test").append('<center>'+message+'</center>');
    console.log(exc);
}
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
                            loadDashTest(self);
                        }
                    } catch(exc){
                        codeError("The code contains one or several errors, and doesn't execute, please double check your code. Errors are available on console.", exc);
                    }
};
function checkIntegrity(closure){
    if(!closure.confs || !(typeof closure.confs == 'object'))
        throw 'You must specify a \'confs\' dictionary for the plugin.';

    if(!closure.plugin || !(typeof closure.plugin == 'function'))
        throw 'You must specify a \'plugin\' function for the plugin.';

    return true;
}
function loadDashTest(closure){
    dashzone = $("#playground_test").dashboard(
        {
            initial: function () {
                dashzone.addWidget(closure.confs.id);
            }
        });

    dashzone.register(
        new PlugShellWidget(
            closure.confs, closure.plugin
        )
    );

    dashzone.initial();
};

