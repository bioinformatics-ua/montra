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
    $.fn.tabmanager = function(options) {
        // This indicates plugin version, and allows to invalidate any existing caches
        var __version = "0.1";

        var self = this;

        var sorthandle;
        var header = self.children('.nav');
        var bodies = self.children('.tab-content');

        var settings = $.extend({
            showRegistry: null,
            registryTarget: null,
            initial: null
        }, options);

        var timer = 0;

        var initial_widgets = {};
        var registered_widgets = {};
        var in_use = {};

        var widgets = [

        ];

        var private_funcs = {
            __loadExisting: function(){
                console.log($(self).children());
            },
            __init: function(){

            },
            __delay: function(callback, ms) {
                    clearTimeout(timer);
                    timer = setTimeout(callback, ms);
            },
            __renderRegistry: function(){
                if(settings.showRegistry != null && settings.registryTarget != null){
                    var target = $(settings.registryTarget);

                    var to_render = '<a class="btn dropdown-toggle" data-toggle="dropdown" href="#" id="add_list_toolbar"><i class="icon-retweet"></i> Add Tabs <span class="caret"></span></a>'+
                    '<ul class="dropdown-menu">';

                    var no_results = true;
                    for (var key in registered_widgets) {
                        if (registered_widgets.hasOwnProperty(key)) {
                            if(private_funcs.__indexOf(key) == -1){
                                to_render += '<li><a id="'+key+'" class="tabaddwidget" data-widgetname="'+key+'" href="javascript:void(0)">'+registered_widgets[key].header+'</a></li>';
                                no_results=false;
                            }
                        }

                    }

                    if(no_results)
                        to_render+='<li><a id="noresultswidget" href="javascript:void(0)">No more tabs available.</a></li>'
                    to_render+='</ul>';

                    target.html(to_render);

                    $(".tabaddwidget",target).click(function(){
                        var key = $(this).data('widgetname');
                        public_funcs.addWidget(key);
                    });


                }
            },
            __supports_storage: function () {
              try {
                return 'localStorage' in window && window['localStorage'] !== null;
              } catch (e) {
                return false;
              }
            },
            __updatecoords: function(identificator, pos){
                for(var i=0;i<widgets.length;i++){
                    if(widgets[i].widgetname == identificator){
                        // was using data set instead of jquery, but had to changed because of ie9 and ie10 support...
                        widgets[i].pos = parseInt(pos);
                        break;
                    }
                }

                public_funcs.saveConfiguration();
            },
            __indexOf: function(widgetname){
                for(var i=0;i<widgets.length;i++){
                    if(widgets[i].widgetname == widgetname)
                        return i;
                }
                return -1;
            },
             __deepcopy: function(dictionary){
                var copy = {}
                for (var key in dictionary) {
                    if (dictionary.hasOwnProperty(key)) {
                        copy[key] = dictionary[key].copy();
                    }

                }

                return copy;

            }
        };

        var tabcontrol = {
            init: function(){
                header.children('li').addClass('dont-move');

                sorthandle = header.sortable({
                  items: "li:not(.dont-move)",
                  //containment: "parent",
                  //axis: "x",
                  stop: function( event, ui ) {
                    $(header).children('li').each(function(index, elem){
                        var id = $(elem).data('id');
                        private_funcs.__updatecoords(id, index);
                    });
                  }
                });

                sorthandle.disableSelection();
            },
            addLayoutTab: function(id, head, body, pos){

                var inserted = false;
                var to_insert = '<li data-pos="'+pos+'" data-id="'+id+'" id="tab-'+id+'">\
                                    <a href="#'+id+'" data-toggle="tab">'+head+'</a>\
                                </li>';

                header.children('li').each(function(index, elem){
                    var this_pos = $(elem).data('pos');
                    if(!this_pos)
                        return true;

                    if(this_pos > pos){
                        $(elem).before(to_insert);
                        inserted = true;

                        return false;
                    }
                });

                if(!inserted){
                    console.log('inserted after')
                    header.append(to_insert);
                }

                bodies.append(
                '<div class="tab-pane" id="'+id+'">\
                '+body+'\
                </div>');
            },
            remove: function(id){
                $('#tab-'+id, header).remove();
                $('#'+id, bodies).remove();
            },
            destroy: function(){
                for(var i=0;i<widgets.length;i++){
                    tabcontrol.remove(widgets[i].widgetname);
                }
            }
        }

        var public_funcs = {
            order: function(){
                console.log(sorthandle.toArray());
            },
            addWidget: function(widgetname) {
                console.log('add widget');
                var widget = registered_widgets[widgetname];

                if(widget instanceof TabWidget){
                    if (widget.__validate() === true){

                        widget.__init(tabcontrol, public_funcs);
                        widgets.push(widget);
                        console.log(widgets);

                        public_funcs.saveConfiguration();
                    }

                    private_funcs.__renderRegistry();

                } else {
                    console.error("You can only add TabWidget objects to this tab placeholder.");
                }

            },
            register: function(widget){
                initial_widgets[widget.widgetname] = widget;
            },
            update: function(widget){
                registered_widgets[widget.widgetname] = widget;
            },
            unregister: function(widgetname){
                try{
                    delete registered_widgets[widgetname];
                } catch(err){
                    console.error("Couldnt delete registered widget with name "+widgetname);
                }
            },
            removeWidget: function(widgetname) {
                console.log(widgetname);
                for(var i=0;i<widgets.length;i++){
                    if(widgets[i].widgetname == widgetname){
                        widgets.splice(i,1);
                        break;
                    }
                }
                tabcontrol.remove(widgetname);

                public_funcs.saveConfiguration();
                private_funcs.__renderRegistry();

            },
            clear: function(){
                for(var i=0;i<widgets.length;i++)
                    tabcontrol.remove(widgets[i].widgetname);

                widgets = [];

                public_funcs.saveConfiguration();
                private_funcs.__renderRegistry();

            },
            refresh: function() {
                console.log("Refreshing");
            },
            saveConfiguration: function(){
                if(private_funcs.__supports_storage()){

                    var serialization = public_funcs.serialize();

                    localStorage.setItem(self[0].id+"__tabmanager_preferences", serialization);
                    localStorage.setItem(self[0].id+"__tabmanager_version", __version);

                } else {
                    console.error("Your browser doesn't support local storage!");
                    return null;
                }

            },
            loadConfiguration: function(){
                if(private_funcs.__supports_storage()){
                    var stored_version = localStorage.getItem(self[0].id+"__tabmanager_version");
                    console.log("STORED VERSION: "+stored_version);
                    console.log("VERSION CURRENT: "+__version);

                    if(stored_version !== __version)
                        return false;

                    tabcontrol.destroy();

                    widgets = [];
                    private_funcs.__init();

                    try{

                        var parsed_configurations = JSON.parse(localStorage.getItem(self[0].id+"__tabmanager_preferences"));

                        registered_widgets = private_funcs.__deepcopy(initial_widgets);

                        for(var i=0;i<parsed_configurations.length;i++){
                            var this_widget;
                            // I dont know any other generic way of doing this without using eval,
                            // i know eval is evil... but its a controled environment without user input,
                            // dont beat me lol
                            try {
                                var tryme = "this_widget = new "+parsed_configurations[i].type+"();";
                                eval(tryme);

                                this_widget.deserialize(parsed_configurations[i]);

                                public_funcs.update(this_widget);
                                public_funcs.addWidget(this_widget.widgetname);

                            } catch(err){
                                console.log(err);
                                console.error("Couldnt create new widget from serialized input of type "+parsed_configurations[i].type);
                            }
                        }

                        private_funcs.__renderRegistry();

                        return true;

                    } catch(err){
                        console.log(err);
                        console.warn("There seems to be nothing to be loaded, going with default configuration.");
                        return false;
                    }


                } else {
                    console.error("Your browser doesn't support local storage!");
                    return false;
                }

            }, serialize:   function(){
                var serialization = "[";

                for(var i=0;i<widgets.length;i++){
                    if(i == 0)
                        serialization+=widgets[i].serialize();
                    else
                        serialization+=","+widgets[i].serialize();
                }
                serialization+="]";

                return serialization;
            }, initial : function(){

                if(settings.initial !== null && typeof(settings.initial) === 'function'){
                    registered_widgets = private_funcs.__deepcopy(initial_widgets);

                    settings.initial();

                    public_funcs.saveConfiguration();
                    public_funcs.loadConfiguration();
                }
            }, reset   : function(){
                if(private_funcs.__supports_storage()){
                    localStorage.removeItem(self[0].id+"__tabmanager_preferences");

                    public_funcs.clear();

                    public_funcs.initial();
                }
            }
        };

        //$(self).html('<div class="gridster"><ul></ul></div>');
        tabcontrol.init();

        private_funcs.__init();

        private_funcs.__renderRegistry();

        $(window).resize(function() {
            private_funcs.__delay(function() {

                private_funcs.__init();

            }, 700);
        });
        return public_funcs;

    };
}(jQuery));

var TabWidget = function TabWidget(widgetname, header, pos, icon) {
        this.widgetname = widgetname;
        this.header = header || 'New plugin';
        this.pos = pos || 1;
        this.content = "";
        this.icon = icon || '';
        this.header_tooltip = null;
        this.header_style = '';

}.addToPrototype({
    __init  :   function(tabcontrol, parent){
        var self = this;

        var head = '<div title="Drag to change widget position" class="dragtooltip pull-left">';

        if(this.icon != undefined && this.icon.trim() != '')
            head += this.icon;
        else
            head += '<i class="icon-align-justify"></i>';

        head += '</div>&nbsp;<div class="pull-left">&nbsp;&nbsp;'+this.header+
        '&nbsp;&nbsp;</div><div class="pull-right removewidget"><i class="icon-remove"></i></div>';

        var body = '<div><div class="span12">'+this.content+'</div></div>';

        // LOGIC TO INSERT WIDGET INTO THE LAYOUT
        tabcontrol.addLayoutTab(self.widgetname, head, body, this.pos);

        $('#'+this.widgetname+" .dragtooltip").tooltip({'container': 'body'});

        $('#tab-'+this.widgetname+" .removewidget").click(function(){

            if(typeof bootbox !== 'undefined'){
                bootbox.confirm("Are you sure you want to remove this tab ?", function(confirmation){
                    if (confirmation)
                    parent.removeWidget(self.widgetname);
                });
            } else {
                var confirmation = confirm("Are you sure you want to remove this tab ?");
                if ( confirmation === true)
                    parent.removeWidget(self.widgetname);
            }
        });

        if(self.header_tooltip != null){
            $('#'+this.widgetname+' .widget-header').tooltip({
                'trigger': 'hover',
                'placement': 'top',
                'title': self.header_tooltip,
                'container': 'body',
                'html': true
            });
        }

    },
    __refresh    : function(){
        //console.log(this.content);
        $('#'+this.widgetname+' .accordion-inner').html(this.content);
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

}.inherit(TabWidget).addToPrototype({
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
