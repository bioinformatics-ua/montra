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

var __loadLibs = function(array,callback, i){
    if(!i)
        i=0;
    var lib = array[i];
    if (lib.match(".js$")) {
        yepnope.injectJs(lib, function () {
              console.log("Loaded "+lib);
              if(i < (array.length-1)){
                __loadLibs(array, callback, i+1);
              } else {
                callback();
              }
        }, {
              charset: "utf-8"
        }, 2000);
    } else {
        yepnope.injectCss(lib, function () {
              console.log("Loaded "+lib);
              if(i < (array.length-1)){
                __loadLibs(array, callback, i+1);
              }
        }, {
              charset: "utf-8"
        }, 2000);
    }
}

var PlugShellWidget = function PlugShellWidget(confs, show){
    if(confs){
        PlugShellWidget._base.apply(this, [confs.id, confs.name, confs.width, confs.height, confs.x, confs.y, confs.icon]);
    }
    else{
        PlugShellWidget._base.apply(this, [undefined, undefined, undefined, undefined, undefined, undefined]);
        confs = {};
    }
    this.show = show;

    this.extracss = confs.extracss || [];
    this.extralibs = confs.extralibs || [];

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.content = "<center><h3>Loading...</h3></center>";

        var go = function(){
            PlugShellWidget._super.__init.apply(self, [gridster, parent]);

            if(typeof self.show === 'function'){
                self.show(self);
                //self.refresh();
            }
        }

        var all_scripts = this.extracss.slice();
        all_scripts = $.merge(all_scripts, this.extralibs);

        if(all_scripts.length > 0){
            __loadLibs(all_scripts, function(){
                go();
            });
        }else {
            go();
        }

    },
    refresh: function(){
        PlugShellWidget._super.__refresh.apply(this);
    },
    html: function(content){
        this.content = content;
    },
    append: function(content){
        if(this.content == undefined)
            this.content = content;
        else
            this.content += content;
    },
    copy: function(){
        return PlugShellWidget._super.copy.apply(this, [{
            show: this.show,
            extracss: this.extracss,
            extralibs: this.extralibs
        }]);
    },
    serialize: function(){
        return PlugShellWidget._super.serialize.apply(this, [{
            show: this.show,
            extracss: this.extracss,
            extralibs: this.extralibs
        }]);
    },
    deserialize:function(json){
        PlugShellWidget._super.deserialize.apply(this, [json]);

        eval("this.show = "+this.show+";");

        this.extracss = JSON.parse(this.extracss);
        this.extralibs = JSON.parse(this.extralibs);
    }
});
