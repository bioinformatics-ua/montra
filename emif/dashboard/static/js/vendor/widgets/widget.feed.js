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

var FeedWidget = function FeedWidget(widgetname, width, height, pos_x, pos_y){

    FeedWidget._base.apply(this, [widgetname, "History", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.content = "";
        self.icon = '<i class="fa fa fa-newspaper-o" />';
        self.header_tooltip = "Track the databases and check what questions have been updated";

        FeedWidget._super.__init.apply(self, [gridster, parent]);

        $.get("api/feed")
        .done(function(data) {
            if(data.hasfeed){
                var renderQuestion = function(entry, pos, collapsable, show_icon){
                    self.content += '<table style="width: 100%;"><tr>';

                    if(entry === undefined){
                        self.content+="<td><center>There's no history on owned or subscribed database changes.</center></td>";
                    }
                    else {
                        if(show_icon){
                            if(entry.icon === 'edit')
                                self.content += '<td style="width:30px;"><i class="fa fa-2x fa-pencil"></i></td>';
                        }

                        self.content += '<td><a href="fingerprint/'+entry.hash+'/1/">'+entry.name + "</a> updated on "+entry.date +".<br />";


                        if(collapsable){
                            self.content += "<small>There are several changes, click to see details.</small>"
                        } else {
                            self.content += "<small> Changes on questions ";

                            var alterations = entry.alterations;
                            for(var j=0; j < alterations.length; j++){
                                self.content += '<a class="popoverit" data-html="true" data-placement="bottom" data-toggle="popover" data-trigger="hover" data-content=\'<strong>Question:</strong> '+ alterations[j].number
                                alterations[j].text+'<br />';

                                if(alterations[j].oldvalue != alterations[j].newvalue){
                                    self.content += '<br /><strong>Old Answer:</strong>'+alterations[j].oldvalue.replace(/'/g, "\\'")+
                                                    '<br /><strong>New Answer:</strong>'+alterations[j].newvalue.replace(/'/g, "\\'");
                                }

                                if(alterations[j].oldcomment != alterations[j].newcomment)
                                    self.content += '<br /><strong>Old Comment:</strong>'+alterations[j].oldcomment.replace(/'/g, "\\'")+
                                                    '<br /> <strong>New Comment:</strong>'+alterations[j].newcomment.replace(/'/g, "\\'");

                                self.content += '\'>'+
                                alterations[j].number + '</a>, ';
                            }
                            self.content += '</small>';
                        }

                        self.content += '</td>';

                        if(collapsable)
                            self.content += '<td style="vertical-align:center;" id="markable'+i+'" class="pull-right markable"><i class="pull-right fa fa-plus"></i></td>';
                    }
                    self.content +='</tr></table><hr />';
                };

                for(var i=0;i<data.feed.length;i++){

                    if(data.feed[i].length == 1){
                        renderQuestion(data.feed[i][0], i, false, true);
                    } else {
                        self.content +='<div data-id="'+i+'" class="aggheader">';

                        renderQuestion(data.feed[i][0], i, true, true);

                        self.content+='</div><div style="margin-left: 30px; display: none;" id="agg'+i+'">';

                        for(var j=0;j<data.feed[i].length;j++){
                            renderQuestion(data.feed[i][j], i, false, false);
                        }

                        self.content +='</div>';
                    }

                }
            } else {
                self.content = '<center><h3>Error Loading Feed... Please refresh, if the problem persists contact the</h3></center>';
            }

            FeedWidget._super.__refresh.apply(self);

            $('.popoverit').popover(
                {
                    container: 'body',
                    template: '<div class="popover popover-small"><div class="arrow"></div><div class="popover-inner"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
                });
            $('.aggheader').click(function(){
                var openid = $(this).data('id');

                var agg = $('#agg'+openid);

                agg.toggle();
                var plus = $('#markable'+openid).find('.fa-plus');

                if(plus.length == 0){
                    $('#markable'+openid, $(this)).html('<i class="pull-right fa fa-plus">');
                } else {
                    $('#markable'+openid, $(this)).html('<i class="pull-right fa fa-minus">');
                }



            });
          })
        .fail(function() {
            self.content = ' Error loading Common Actions Widget';

            FeedWidget._super.__refresh.apply(self);
        });
    }
});
