/*
 * This widget, marks up patterns, in a plugin-defined manner
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

var PatternRecognizer = function(pattern, target){
    this.pattern = pattern;
    this.target = target;
    this.matches = [];
}.addToPrototype({
    "match": function(){
        var self = this;

        self.matches = [];

        $(self.target).filter(function() {
            var result = $(this).html().match(self.pattern);
            return result;
        }).each(function() {
            //$(this).html($(this).html().replace(this.pattern, "<a href=\"mailto:$1\">$1</a>"));
            self.matches.push(this);
        });
        //console.log('-- Match '+ self.pattern + ' into '+self.target+', found '+ this.matches.length +' matches.');

        return this.matches.length;
    },
    "applyMasks": function(){
        //console.log('-- Applying masks');

        for(var i=0;i<this.matches.length;i++){
            this.mask(this.matches[i]);
        }
    },
    "mask": function(element){
        console.error('This is an abstract method, the method \'mask\' must be overriden.');
    }
});

/* Plugin for email recognizing */
var EmailRecognizer = function(target){
    EmailRecognizer._base.apply(this, [/([\w_\-.]+@[\w_\-.]+)/g, target]);
}.inherit(PatternRecognizer).addToPrototype({
    // override mask
    "mask": function(element){
        $(element).html($(element).html().replace(this.pattern, "<a href=\"mailto:$1\">$1</a>"));
    }
});
/* Plugin for link recognizing */
var LinkRecognizer = function(target){
    LinkRecognizer._base.apply(this, [/(http:\/\/[\w_\-.\/]+)/g, target]);
}.inherit(PatternRecognizer).addToPrototype({
    // override mask
    "mask": function(element){
        if(!$(element).is('a'))
            $(element).html($(element).html().replace(this.pattern, "<a href=\"$1\">$1</a>"));
    }
});
