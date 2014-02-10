/**********************************************************************
# Copyright (C) 2014 Ricardo Ribeiro
#
# Author: Ricardo Ribeiro <ribeiro.r@ua.pt>
#

The MIT License (MIT)


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
# */

(function ($) {
    $.fn.boolrelwidget = function (options) {
        // so we dont lose track of who we are, and used to ensure chainability
        var self = this;
        var loose_variables = [];
        var boolean_definitions = [];
        // Default Options
        var settings = $.extend({
            expand_text:'To define the relations between the terms click here.',
            collapse_text:'Click here to close this panel.'
        }, options);

        // Murphy's law says people will forget to pass a div container, give helpful hint
        if (!this.is('div')) {
            console.error('You must specify a div container to add the boolean relations widget!');
            return this;
        }
        // If its a div lets prepare the widget and add functions to it

        // Lets style the div properly
        self = self.addClass('boolrelwidget-container');
        // Let it be empty
        self = self.html('');
        
        // Now lets add the toolbar
        self = self.append('<ul id="boolrelwidget-expand" class="boolrelwidget-menu-container"><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-l"><div class="boolrelwidget-arrow-up"></div></div></li><li class="boolrelwidget-menu">'+settings.expand_text+'</li><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-r"><div class="boolrelwidget-arrow-up"></div></div></li></ul><ul id="boolrelwidget-collapse" class="boolrelwidget-menu-container-panel"><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-l"><div class="boolrelwidget-arrow-down"></div></div></li><li class="boolrelwidget-menu">'+settings.collapse_text+'</li><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-r"><div class="boolrelwidget-arrow-down"></div></div></li></ul><div id="boolrelwidget-panel">Hidden pannel...</div>');
        
        // Lets add the event handlers
        $( '#boolrelwidget-expand' ).click(function() {
            $('#boolrelwidget-expand').toggle();
            $('#boolrelwidget-collapse').toggle();
            $('#boolrelwidget-panel').toggle();
        });
        $( '#boolrelwidget-collapse' ).click(function() {
            $('#boolrelwidget-expand').toggle();
            $('#boolrelwidget-collapse').toggle();
            $('#boolrelwidget-panel').toggle();
        });
        return {
            push: function (str) {
                loose_variables.push(str);
                console.log('Pushed new variable ' + str + ' to variables pool.');

                return self;
            },
            pop: function (str) {
                loose_variables.pop(str);
                console.log('Popped variable ' + str + ' from variables pool.');

                return self;
            }
        };
    };
}(jQuery));


/*   
 *  Possible Boolean Operations Enumerable and validator
 *  Since i have to support IE7, BOOL['TYPE'] has to be used everywhere instead of BOOL.TYPE
 *  This must be because if we try a BOOL.TYPE that doesn't exist on ie 7 everything crashes (oh my life...)
 */
var BOOL = {
  NOP   : { value: -1,name: "nop"}, // No operation, means its a edge branch 
  AND   : { value: 0, name: "and"}, 
  OR    : { value: 1, name: "or"}, 
  XOR   : { value: 2, name: "xor"}
};

function isBool(op){
    if(!op) return false;
    
        for(var index in BOOL) {
            if(op.value == BOOL[index].value)
                return true;
        }
        return false;
}

/* Defining a unique counter of ids to attribute booleanVariable instances 
 * (this is used to facilitate encountering nested references */

var boolrelwidgetuniqueidcounter=10000;
/* Defining BooleanVariable class 
 *  A BooleanVariable object has:
 *      -   a id to facilitate encountering the element when nested
 *      -   two operators of type either string or BooleanVariable
 *      -   a relation of enum type BOOL
 */

function BooleanGroup(obj1){
    if(!(obj1 instanceof BooleanGroup || typeof obj1 == 'string' || obj1 instanceof String)){
        console.warn('First operator of Boolean Group object must be a BooleanGroup or a string');
        return null;
    }
    this.id = boolrelwidgetuniqueidcounter++;
    this.variables = [];
    this.relations = [];
    
    this.variables.push(obj1);
}
BooleanGroup.prototype = { 
    addBoolean  :   function(op, obj1){
    
        if(!(obj1 instanceof BooleanGroup || typeof obj1 == 'string' || obj1 instanceof String)){
            console.warn('Operator of Boolean Group object must be a BooleanGroup or a string.');
            return null;
        }        
        if(!isBool(op)){
            console.warn('Relation between operators must be of a BOOL valid type.');
            return null;
        }        
        this.variables.push(obj1);
        this.relations.push(op);
    },
        /* This returns a string representation of this object in boole's arithmetic format */
    toString : function(){
        var output=this.variables[0]
        var i=0;
        for(i=1;i<this.variables.length;i++){
            output+=" "+this.relations[i-1].name+" "+this.variables[i].toString();
        }
        if(this.variables.length>1)
            output="("+output+")";
        
        return output;
    },
    removeById : function(other_id){
        return this.removeByIdAux(null, null, other_id); 
    },
  removeByIdAux : function(parent, branch, other_id) {
        if(typeof other_id != 'number'){
            console.warn('When removing by id, a number value must be specified. Found type ' + typeof other_id);
        }
        else {
            if(this.id == other_id){
                // If not on root remove reference
                if(parent){
                    parent.variables.splice(branch,1);
                }
                return this;
            }
            var returnable=null;
            var k = 0;
            for(k=0;k<this.variables.length;k++){
                if(this.variables[k] instanceof BooleanGroup){
                    returnable = this.variables[k].removeByIdAux(this, k, other_id);
                }
            }
            return returnable;
        }
    },    
    destroy : function() {
        this.variables=null;
        this.relations=null;
        this=null;
    }
};