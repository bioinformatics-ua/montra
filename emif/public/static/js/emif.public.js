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
#*/

$(function(){
    var cbtns = $('.copy-button');

    cbtns.each(function (i){

      addClipboard(this);
    });
});

function addClipboard(element){
    if(hasFlash()){
    var base = $('#base_link').attr('href');

    $(element).attr('data-clipboard-text', base+$(element).data('clipboard-text'))
    var client = new ZeroClipboard($(element));
    } else {
        $(element).hide();
    }
}
function hasFlash(){
    try {
        if( new ActiveXObject('ShockwaveFlash.ShockwaveFlash') ) return true;
    } catch(e){
      if(navigator.mimeTypes ["application/x-shockwave-flash"] != undefined) return true;
    }
    return false;
}
