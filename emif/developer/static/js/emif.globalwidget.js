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

(function($) {
    $.fn.globalwidget = function(options) {
        // This indicates plugin version, and allows to invalidate any existing caches
        var __version = "0.1";

        var self = this;

        var settings = $.extend({
        }, options);
        var control = {
            addLayout: function(name, head, body){
                console.log('ADD LAYOUT');
                console.log(name);
                self.html(
                    '<div id="'+name+'" style="border: 1px solid #e5e5e5;"><div>\
                         <div class="widget-header">\
                            '+head+'\
                         </div>\
                     </div>\
                     <div class="row">\
                        <div class="span12">\
                            '+body+'\
                        </div>\
                     </div></div>');
            }
        }
        var public_funcs = {
            render: function(global){
                if(global instanceof GlobalWidget)
                    global.__init(control, self);
            }
        };

        return public_funcs;
    };
}(jQuery));

var GlobalWidget = function GlobalWidget(widgetname, header, icon) {
        this.widgetname = widgetname;
        this.header = header || 'New global plugin';
        this.content = "";
        this.icon = icon || '';
        this.header_tooltip = null;
        this.header_style = '';

}.addToPrototype({
    __init  :   function(control, parent){
        var self = this;

        var head = '<span class="lead text-center"><div style="  margin-top: 5px;" class="pull-left">';

        if(this.icon != undefined && this.icon.trim() != '')
            head += this.icon;
        else
            head += '<i class="icon-align-justify"></i>';

        head += '</div>&nbsp;&nbsp;&nbsp;'+this.header+
        '</span>';

        var body = '<div class="accordion-body"><div class="accordion-inner global-body">'+this.content+'</div></div>';

        // LOGIC TO INSERT WIDGET INTO THE LAYOUT
        control.addLayout(self.widgetname, head, body);

    },
    __refresh    : function(){
        //console.log(this.content);
        console.log('#'+this.widgetname+' .global-body');
        console.log($('#'+this.widgetname+' .global-body'));
        $('#'+this.widgetname+' .global-body').html(this.content);
    },
    // private methods
    __validate : function(){
        if (!(typeof this.widgetname == 'string' || this.widgetname instanceof String)) {
            console.warn('Widget name on Dashboard widget must be a string');
            return false;
        }
        if (!(typeof this.header == 'string' || this.header instanceof String)) {
                console.warn('Header on Dashboard must be a string');
                return false;
        }

        if (!(typeof this.pos == 'number' || this.pos instanceof Number)) {
            console.warn('pos on Dashboard widget must be a number.');
            return false;
        }

        return true;
    },
    // public methods
    serialize : function(extra){
        var extra = extra || {};
        var tmp ='{'+
                    '"type": "'+this.constructor.name+'",'+
                    '"widgetname": "'+this.widgetname+'",'+
                    '"pos": '+this.pos+','+
                    '"header": "'+this.header+'",'+
                    '"icon": "'+encodeURI(this.icon)+'",'+
                    '"content": "'+encodeURI(this.content)+'"';


        for(var parameter in extra){
            var eparam = extra[parameter];

            if(typeof eparam == 'function')
                tmp += ',"'+parameter+'": "'+encodeURI(String(eparam))+'"';
            else if(eparam instanceof Array){
                tmp += ',"'+parameter+'": "'+encodeURI(JSON.stringify(eparam))+'"';
            }
        }

        tmp += '}';

        return tmp;
    }, deserialize : function(json){
        this.widgetname = json.widgetname;
        delete json.widgetname

        this.header = json.header;
        delete json.header;

        this.pos = parseInt(json.pos);
        delete json.pos;

        this.content = decodeURI(json.content);
        delete json.content;

        delete json.type;

        this.icon = decodeURI(json.icon);
        delete json.icon;

        for(var parameter in json){
            this[parameter] = decodeURI(json[parameter]);
        }

    },
    copy : function(extra){

        var extra = extra || {};
        var this_widget;
        var tryme = "this_widget = new "+this.constructor.name+"();";
        eval(tryme);

        this_widget.widgetname = this.widgetname;
        this_widget.header = this.header;

        this_widget.pos = this.pos;

        this_widget.content = this.content;
        this_widget.icon = this.icon;

        for(var parameter in extra){
            this_widget[parameter] = extra[parameter];
        }

        return this_widget;
    }
});

var SimpleTextWidget = function SimpleTextWidget(widgetname, header, pos, content){
    SimpleTextWidget._base.apply(this, [widgetname, header, pos]);

    this.content = content;

}.inherit(GlobalWidget).addToPrototype({
    __validate : function(){
        //console.log();
        var success = SimpleTextWidget._super.__validate.apply(this);

        if(success){
            if (!(typeof this.content == 'string' || this.content instanceof String)) {
                console.warn('Content on SimpleTextWidget must be a string');
                return false;
            }

            return true;
        } else {
            return false;
        }
    }
});
