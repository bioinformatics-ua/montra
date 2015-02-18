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

var TagCloudWidget = function TagCloudWidget(widgetname, width, height, pos_x, pos_y){

    TagCloudWidget._base.apply(this, [widgetname, "Tag Cloud", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.icon = '<i class="fa fa-cloud"></i>';
        self.header_tooltip = "The most common terms in the Catalogue.";

        self.content = "<center><h3>Loading...</h3></center>";

        TagCloudWidget._super.__init.apply(self, [gridster, parent]);

        $.get("api/tagcloud")
        .done(function(data) {
            if(data.tags){
                var tags = data.tags;
                self.content ='<form method="POST" action="resultsdiff/1" style="display: none;">'+
                '<input type="hidden" name="csrfmiddlewaretoken" value="'+csrftoken+'"><div id="hidden'+
                self.widgetname+'"></div></form>';

                self.content += '<div style="text-align: center;" id="tag'+self.widgetname+'">';

                for(var i=0;i<tags.length;i++){
                    self.content += '<a style="margin: 3px; display: inline-block;" data-event="'+tags[i].name+'" rel="'+tags[i].relevance+'">'+tags[i].name+'</a>';
                }
                self.content += "</div>";

            } else {
                self.content = "Error Loading Tag Cloud Widget";
            }

            TagCloudWidget._super.__refresh.apply(self);

            $.fn.tagcloud.defaults = {
              size: {start: 10, end: 24, unit: 'pt'},
              color: {start: '#000000', end: '#00B3FF'}
            };
            var tags = $('#tag'+self.widgetname+' a');
            tags.tagcloud();

            tags.each(function(){
                $(this).click(function(ev){
                    ev.preventDefault();
                    var word = $(this).data('event');

                    $('#hidden'+self.widgetname).html('<input type="text" name="query" value="'+word+'" size="25" maxlength="256">');

                    $('#hidden'+self.widgetname).parent().submit();

                    return false;
                });
            });

          })
        .fail(function() {
            self.content = ' Error loading Tag Cloud Widget';

            TagCloudWidget._super.__refresh.apply(self);
        });
    }
});
