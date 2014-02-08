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
function BooleanVariable(obj1, op, obj2) {
    
    if(!(obj1 instanceof BooleanVariable || typeof obj1 == 'string' || obj1 instanceof String)){
        console.warn('First operator of Boolean Variable object must be a BooleanVariable or a string');
        return null;
    }
    if(!(obj2 instanceof BooleanVariable || typeof obj2 == 'string' || obj2 instanceof String)){
        console.warn('Second operator of Boolean Variable object must be a BooleanVariable or a string');
        return null;
    }    
    if(!isBool(op)){
        console.warn('Relation between operators must be of a BOOL valid type.');
        return null;
    }
    this.id = boolrelwidgetuniqueidcounter++;
    this.oper1 = obj1;
    this.relation= op;
    this.oper2 = obj2;
    
};

/* 
 *  Elaborating prototypes for BooleanVariable
 */
BooleanVariable.prototype = { 
    setRelation : function(op){
        // We must check the enum type exists
        if(!isBool(rel)){
            console.warn('Relation between operators must be of a BOOL valid type.');
            return false;
        }
        this.relation = op;   
        return true;
    },
    setOper1 : function (obj1){
        if(!(obj1 instanceof BooleanVariable || typeof obj1 == 'string' || obj1 instanceof String)){
            console.warn('First operator of Boolean Variable object must be a BooleanVariable or a string');
            return null;
        }    
        this.oper1= obj1;
    },
    setOper2 : function (obj1){
        if(!(obj2 instanceof BooleanVariable || typeof obj2 == 'string' || obj2 instanceof String)){
            console.warn('Second operator of Boolean Variable object must be a BooleanVariable or a string');
            return null;
        }    
        this.oper2= obj1;
    },
    removeById : function(other_id){
        this.removeByIdAux(null, null, other_id);
    },
    removeByIdAux : function(parent, branch, other_id) {
        if(typeof other_id != 'number'){
            console.warn('When removing by id, a number value must be specified. Found type ' + typeof other_id);
        }
        else {
            console.log('value :'+this);
            if(this.id == other_id){
                // If not on root remove reference
                if(parent && branch){
                    if(branch == 1)
                        parent.clearOper1();
                    if(branch == 2)
                        parent.clearOper2();
                }
                return this;
            }
            
            if(this.oper1 instanceof BooleanVariable){
                this.oper1.removeByIdAux(this,1, other_id);
            }
            if(this.oper2 instanceof BooleanVariable){
                this.oper2.removeByIdAux(this,2, other_id);
            }
        }
    },
    clearOper1 : function (){
        this.oper1=null;
    },
    clearOper2 : function (){
        this.oper2=null;
    },    
    /* This returns a string representation of this object in boole's arithmetic format */
    toString : function(){
        // single operators either oper1 or oper2 only
        if(this.oper1 == null && this.oper2 == null)
            return "";        
        else if(this.oper1 == null)
            return this.oper2.toString();
        else if(this.oper2 == null)
            return this.oper1.toString();
        
        return "("+this.oper1.toString()+' '+this.relation.name+' '+this.oper2.toString()+")";
    },
    destroy : function() {
        this.oper1=null;
        this.oper2=null;
        this=null;
    }
};