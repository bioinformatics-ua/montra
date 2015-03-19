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
*/
$(function(){
    $('.notification_detail').click(function(){
        var link = $(this).parent().data('link');
        var ident = $(this).parent().data('ident');
        if(link && ident){
            var readindicator = $(this).parent().find('.notification_read');

            if(readindicator.hasClass('muted')){
                readindicator.removeClass('muted');
            } else {
                readindicator.addClass('muted');
            }

            handleClick(ident, link);

        }
    });

    $('.notification_delete').click(function(){
        var self = $(this);
        var ident = self.parent().parent().data('ident');
        var read = self.parent().find('.notification_read').hasClass('muted');

        var r = true;
        if (!read) {
            r = confirm("You are trying to delete a unread notification, are you sure?");
        }

        if (r) {
            $.post("api/removenotification", {
                notification: ident,
                value: true
            })
                .done(function(data) {
                    if (data.success) {
                        location.reload(true);
                    }
                })
                .fail(function() {
                    console.log("Failed removing notification");
                });
        }
    });
    $('.notification_read').click(function(){
        var self = $(this);
        var ident = self.parent().parent().data('ident');
        var value = self.hasClass('muted');


        $.post("api/readnotification", {
            notification: ident,
            value: !value
        })
            .done(function(data) {
                if (data.success) {
                    location.reload(true);
                }
            })
            .fail(function() {
                console.log("Failed marking as read notification");
            });
    });
});
