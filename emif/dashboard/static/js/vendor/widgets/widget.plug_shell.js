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

var PlugShellWidget = function PlugShellWidget(confs, show){
    if(confs)
        PlugShellWidget._base.apply(this, [confs.id, confs.name, confs.width, confs.height, confs.x, confs.y]);
    else
        PlugShellWidget._base.apply(this, [undefined, undefined, undefined, undefined, undefined, undefined]);

    this.show = show;

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.icon = '<i class="fa fa-line-chart"></i>';

        self.content = "<center><h3>Loading...</h3></center>";

        PlugShellWidget._super.__init.apply(self, [gridster, parent]);

        if(typeof this.show === 'function'){
            this.show(self);
            self.refresh();
        }

    },
    refresh: function(){
        PlugShellWidget._super.__refresh.apply(this);
    },
    copy: function(){
        return PlugShellWidget._super.copy.apply(this, [{
            show: this.show
        }]);
    },
    serialize: function(){
        return PlugShellWidget._super.serialize.apply(this, [{
            show: this.show
        }]);
    },
    deserialize:function(json){
        PlugShellWidget._super.deserialize.apply(this, [json]);

        eval("this.show = "+this.show+";");
    }
});
