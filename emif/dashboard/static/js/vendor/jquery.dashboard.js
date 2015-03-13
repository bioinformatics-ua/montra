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
    $.fn.dashboard = function(options) {
        // This indicates plugin version, and allows to invalidate any existing caches
        var __version = "0.1";

        var self = this;

        var settings = $.extend({
            showRegistry: null,
            registryTarget: null,
            initial: null
        }, options);

        var gridster;
        var timer = 0;

        var initial_widgets = {};
        var registered_widgets = {};
        var in_use = {};

        var widgets = [

        ];

        var private_funcs = {
            __init: function() {
                var width = (parseFloat($(self).width()) / 6) - 10;

                var cols, rows;



                if (width < 130) {
                    width = (parseFloat($(self).width()) / 4) - 10;

                    cols = 4;
                    rows = 4;
                } else {
                    cols = 6;
                    rows = 4;
                }

                gridster = $(".gridster > ul").gridster({
                    widget_base_dimensions: [width, 200],
                    widget_margins: [5, 5],
                    helper: 'clone',
                    max_cols: cols,
                    max_rows: rows,
                    min_cols: cols,
                    min_rows: rows,
                    resize: {
                        enabled: true,
                        max_size: [cols, rows],
                        min_size: [2, 1],
                        stop: function(e, ui, $widget) {
                            console.log("invoking stop from resize");
                            private_funcs.__clampHeight($widget);
                            public_funcs.saveConfiguration();
                        }
                    },
                    draggable: {
                        handle: '.widget-header',
                        stop: function(event, ui) {
                            public_funcs.saveConfiguration();
                        }
                    },
                }).data('gridster');

            },
            __delay: function(callback, ms) {
                    clearTimeout(timer);
                    timer = setTimeout(callback, ms);
            },
            __clampHeight: function(context) {
                $('[data-clampedheight]', context).each(function() {
                    var elem = $(this);
                    var parentPanel = elem.data('clampedheight');
                    if (parentPanel) {
                        var sideBarNavWidth = $(parentPanel).height() - 40 - parseInt(elem.css('paddingTop')) - parseInt(elem.css('paddingBottom')) - parseInt(elem.css('marginTop')) - parseInt(elem.css('marginBottom')) - parseInt(elem.css('borderTopWidth')) - parseInt(elem.css('borderBottomWidth'));

                        elem.css('height', sideBarNavWidth);
                    }

                });
            }, __supports_storage: function () {
              try {
                return 'localStorage' in window && window['localStorage'] !== null;
              } catch (e) {
                return false;
              }
            },
            __updateAllcoords:  function(){
                var this_widgets = gridster.$widgets;
                for(var i=0;i<this_widgets.length;i++){
                    private_funcs.__updatecoords($(this_widgets[i]));
                }
            },
            __updatecoords: function(widget){
                for(var i=0;i<widgets.length;i++){
                    if(widgets[i].widgetname == widget.attr('id')){
                        // was using data set instead of jquery, but had to changed because of ie9 and ie10 support...
                        widgets[i].width = parseInt($(widget[0]).attr('data-sizex'));
                        widgets[i].height = parseInt($(widget[0]).attr('data-sizey'));
                        widgets[i].pos_x = parseInt($(widget[0]).attr('data-col'));
                        widgets[i].pos_y = parseInt($(widget[0]).attr('data-row'));
                        break;
                    }
                }
            },
            __indexOf: function(widgetname){
                for(var i=0;i<widgets.length;i++){
                    if(widgets[i].widgetname == widgetname)
                        return i;
                }
                return -1;
            },
            __renderRegistry: function(){
                if(settings.showRegistry != null && settings.registryTarget != null){
                    var target = $(settings.registryTarget);

                    var to_render = '<a class="btn dropdown-toggle" data-toggle="dropdown" href="#" id="add_list_toolbar"><i class="icon-retweet"></i> Add Widgets <span class="caret"></span></a>'+
                    '<ul class="dropdown-menu">';

                    var no_results = true;
                    for (var key in registered_widgets) {
                        if (registered_widgets.hasOwnProperty(key)) {
                            if(private_funcs.__indexOf(key) == -1){
                                to_render += '<li><a id="'+key+'" class="dashboardaddwidget" data-widgetname="'+key+'" href="javascript:void(0)">'+registered_widgets[key].header+'</a></li>';
                                no_results=false;
                            }
                        }

                    }

                    if(no_results)
                        to_render+='<li><a id="noresultswidget" href="javascript:void(0)">No more widgets available.</a></li>'
                    to_render+='</ul>';

                    target.html(to_render);

                    $(".dashboardaddwidget",target).click(function(){
                        var key = $(this).data('widgetname');
                        public_funcs.addWidget(key);
                        private_funcs.__clampHeight($('#'+key));
                    });


                }
            }, __deepcopy: function(dictionary){
                var copy = {}
                for (var key in dictionary) {
                    if (dictionary.hasOwnProperty(key)) {
                        copy[key] = dictionary[key].copy();
                    }

                }

                return copy;

            }

        };

        var public_funcs = {
            addWidget: function(widgetname) {
                var widget = registered_widgets[widgetname];

                if(widget instanceof DashboardWidget){
                    if (widget.__validate() === true){

                        widget.__init(gridster, public_funcs);
                        widgets.push(widget);

                        private_funcs.__clampHeight($('#'+widget.widgetname));

                        public_funcs.saveConfiguration();

                    }

                    private_funcs.__renderRegistry();

                } else {
                    console.error("You can only add DashboardWidget objects to this dashboard.");
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
                    console.error("Couldnt delete registered widget with name"+widgetname);
                }
            },
            removeWidget: function(widgetname) {
                for(var i=0;i<widgets.length;i++){
                    if(widgets[i].widgetname == widgetname){
                        widgets.splice(i,1);
                        break;
                    }
                }

                gridster.remove_widget.apply(gridster, $('#'+widgetname));

                public_funcs.saveConfiguration();
                private_funcs.__renderRegistry();

            },
            clear: function(){
                widgets = [];
                gridster.remove_all_widgets.apply(gridster);

                public_funcs.saveConfiguration();
                private_funcs.__renderRegistry();

            },
            refresh: function() {
                console.log("Refreshing");
            },
            saveConfiguration: function(){
                if(private_funcs.__supports_storage()){

                    private_funcs.__updateAllcoords();

                    var serialization = public_funcs.serialize();

                    localStorage.setItem(self[0].id+"_preferences", serialization);
                    localStorage.setItem(self[0].id+"__dashboard_version", __version);

                } else {
                    console.error("Your browser doesn't support local storage!");
                    return null;
                }

            },
            loadConfiguration: function(){
                if(private_funcs.__supports_storage()){
                    var stored_version = localStorage.getItem(self[0].id+"__dashboard_version");
                    console.log("STORED VERSION: "+stored_version);
                    console.log("VERSION CURRENT: "+__version);

                    if(stored_version !== __version)
                        return false;

                    gridster.destroy();
                    $(self).html('<div class="gridster"><ul></ul></div>');
                    widgets = [];
                    private_funcs.__init();

                    try{
                        var parsed_configurations = JSON.parse(localStorage.getItem(self[0].id+"_preferences"));

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

                                private_funcs.__clampHeight($('#'+this_widget.widgetname));

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
                    localStorage.removeItem(self[0].id+"_preferences");

                    public_funcs.clear();

                    public_funcs.initial();
                }
            }
        };

        $(self).html('<div class="gridster"><ul></ul></div>');

        private_funcs.__init();

        private_funcs.__renderRegistry();

        $(window).resize(function() {
            private_funcs.__delay(function() {
                gridster.destroy();

                private_funcs.__init();

            }, 700);
        });
        return public_funcs;

    };
}(jQuery));

var DashboardWidget = function DashboardWidget(widgetname, header, width, height, pos_x, pos_y, icon) {
        this.widgetname = widgetname;
        this.width = width || 2;
        this.height = height || 1;
        this.pos_x = pos_x || 1;
        this.pos_y = pos_y || 1;
        this.header = header || 'New plugin';
        this.content = "";
        this.icon = icon || '';
        this.header_tooltip = null;
        this.header_style = '';

}.addToPrototype({
    __init  :   function(gridster, parent){
        var self = this;

        var __widgetentry = '<li id="'+ this.widgetname+'"><div style="'+this.header_style+'" class="widget-header"><div title="Drag to change widget position" class="dragtooltip pull-left">';

        if(this.icon != undefined && this.icon.trim() != '')
            __widgetentry += this.icon;
        else
            __widgetentry += '<i class="icon-align-justify"></i>';

        __widgetentry += '</div>'+this.header+
        '<div class="pull-right removewidget"><i class="icon-remove"></i></div></div><div class="accordion-body"><div style="overflow-y:auto; height: auto;" data-clampedheight="#'+
        this.widgetname+'" class="accordion-inner">'+this.content+'</div></div></li>';

        var widget = [__widgetentry, this.width, this.height, this.pos_x, this.pos_y];

        gridster.add_widget.apply(gridster, widget);

        $('#'+this.widgetname+" .dragtooltip").tooltip({'container': 'body'});

        $('#'+this.widgetname+" .removewidget").click(function(){
            if(typeof bootbox !== 'undefined'){
                bootbox.confirm("Are you sure you want to remove this widget ?", function(confirmation){
                    if (confirmation)
                    parent.removeWidget(self.widgetname);
                });
            } else {
                var confirmation = confirm("Are you sure you want to remove this widget ?");
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
        if (!(typeof this.width == 'number' || this.width instanceof Number)) {
            console.warn('Width on Dashboard widget must be a number.');
            return false;
        }
        if (!(typeof this.height == 'number' || this.height instanceof Number)) {
            console.warn('Height on Dashboard widget must be a number.');
            return false;
        }
        if (!(typeof this.pos_x == 'number' || this.pos_x instanceof Number)) {
            console.warn('pos_x on Dashboard widget must be a number.');
            return false;
        }
        if (!(typeof this.pos_y == 'number' || this.pos_y instanceof Number)) {
            console.warn('pos_y on Dashboard widget must be a number.');
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
                    '"width": '+this.width+','+
                    '"height": '+this.height+','+
                    '"pos_x": '+this.pos_x+','+
                    '"pos_y": '+this.pos_y+','+
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
        this.width = parseInt(json.width);
        delete json.width;
        this.height = parseInt(json.height);
        delete json.height;
        this.pos_x = parseInt(json.pos_x);
        delete json.pos_x;
        this.pos_y = parseInt(json.pos_y);
        delete json.pos_y;
        this.header = json.header;
        delete json.header;
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
        this_widget.width = this.width;
        this_widget.height = this.height;
        this_widget.pos_x = this.pos_x;
        this_widget.pos_y = this.pos_y;
        this_widget.header = this.header;
        this_widget.content = this.content;
        this_widget.icon = this.icon;

        for(var parameter in extra){
            this_widget[parameter] = extra[parameter];
        }

        return this_widget;
    }
});

var SimpleTextWidget = function SimpleTextWidget(widgetname, header, content, width, height, pos_x, pos_y){
    SimpleTextWidget._base.apply(this, [widgetname, header, width, height, pos_x, pos_y]);

    this.content = content;

}.inherit(DashboardWidget).addToPrototype({
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
