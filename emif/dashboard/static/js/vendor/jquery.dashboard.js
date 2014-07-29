/*
 * Author: Ricardo Ribeiro <ribeiro.r@ua.pt>
 * Dashboard plugin that uses gridster for the grid, and is bootstrap 2 styled
 */

(function($) {
    $.fn.dashboard = function(options) {
        var self = this;

        var settings = $.extend({

        }, options);

        var gridster;
        var timer = 0;

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
                            private_funcs.__clampHeight($widget);
                        }
                    },
                    draggable: {
                        handle: '.widget-header'
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
            }
        };

        var public_funcs = {
            addWidget: function(widget) {
                console.log('Add new widget');

                if(widget instanceof DashboardWidget){
                    widget.__init(gridster);
                } else {    
                    console.error("You can only add DashboardWidget objects to this dashboard.");
                }

            },
            removeWidget: function() {
                console.log('Remove widget');
            },
            refresh: function() {
                console.log("Refreshing");
            }
        };

        $(self).html('<div class="gridster"><ul></ul></div>');

        private_funcs.__init();

        $(window).resize(function() {
            private_funcs.__delay(function() {
                gridster.destroy();

                private_funcs.__init();

            }, 700);
        });

        //private_funcs.__clampHeight($('body'));

        return public_funcs;

    };
}(jQuery));

DashboardWidget = function DashboardWidget(widget_name, width, height, pos_x, pos_y) {
        this.widget_name = widget_name;
        this.width = width;
        this.height = height;
        this.pos_x = pos_x;
        this.pos_y = pos_y;
        this.header = "";
        this.content = "";
    
}.addToPrototype({
    __init  :   function(gridster){
        var widget = ['<li id="'+ this.widget_name+'"><div class="widget-header"><div title="Drag to change widget position" class="dragtooltip pull-left"><i class="icon-align-justify"></i></div>'+this.header+
        '</div><div class="accordion-body"><div style="overflow:auto; height: auto;" data-clampedheight="#'+
        this.widget_name+'" class="accordion-inner">'+this.content+'</div></div></li>', this.width, this.height, this.pos_x, this.pos_y];

        gridster.add_widget.apply(gridster, widget)

        $(".dragtooltip", $('#'+this.widget_name)).tooltip({'container': 'body'});
    },
    __validate : function(){
        if (!(typeof this.widget_name == 'string' || widget_name instanceof String)) {
            console.warn('Widget name on Dashboard widget must be a string');
            return null;
        }
        if (!(typeof this.width == 'number' || this.width instanceof Number)) {
            console.warn('Width on Dashboard widget must be a number.');
            return null;
        }
        if (!(typeof this.height == 'number' || this.height instanceof Number)) {
            console.warn('Height on Dashboard widget must be a number.');
            return null;
        }
        if (!(typeof this.pos_x == 'number' || this.pos_x instanceof Number)) {
            console.warn('pos_x on Dashboard widget must be a number.');
            return null;
        }
        if (!(typeof this.pos_y == 'number' || this.pos_y instanceof Number)) {
            console.warn('pos_y on Dashboard widget must be a number.');
            return null;
        }
    }
});

var SimpleTextWidget = function(widget_name, header, content, width, height, pos_x, pos_y){
    SimpleTextWidget._base.apply(this, [widget_name, width, height, pos_x, pos_y]);

    this.header = header;
    this.content = content;

}.inherit(DashboardWidget).addToPrototype({
    __validate   :   function(){

        SimpleTextWidget._super.validate();

        if (!(typeof this.header == 'string' || this.header instanceof String)) {
            console.warn('Header on SimpleTextWidget must be a string');
            return null;
        }
        if (!(typeof this.content == 'string' || this.content instanceof String)) {
            console.warn('Content on SimpleTextWidget must be a string');
            return null;
        }
    }
});