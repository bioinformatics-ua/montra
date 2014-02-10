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
        var basic_blocks = [];
        var mastergroup=null;
        // Default Options
        var settings = $.extend({
            expand_text:'To define the relations between the terms click here.',
            collapse_text:'Click here to close this panel.'
        }, options);
        
        var group1 = new BooleanGroup('A');
        var group2 = new BooleanGroup('B');
        var group3 = new BooleanGroup('C');

        var group_xpto = new BooleanGroup(group1);
        group_xpto.addBoolean(BOOL['OR'],group2);
        group_xpto.addBoolean(BOOL['OR'],group3);
        var group_xpto2 = new BooleanGroup(new BooleanGroup('Z'));
        group_xpto2.addBoolean(BOOL['XOR'],group_xpto);

        
        mastergroup = new BooleanGroup(group_xpto2);
        
        var funcs = {
            push: function (str) {
                
                if(this.getIndex(str)!= -1){
                    console.warn('Variable ' + str + ' already on basic blocks pool.');  
                    return null;
                }
                
                var block = new BooleanGroup(str);
                basic_blocks.push(block);
                console.warn('Pushed new variable ' + str + ' to basic blocks pool.');

                this.draw();
                
                return block;
            },
            splice: function (str) {
                var id = this.getIndex(str)
                if(id < 0){
                   console.warn('No basic block ' + str + ' from basic blocks pool to slice out.');
                   return null; 
                }
                var block = basic_blocks.splice();
                console.warn('Sliced out variable ' + str + ' from basic blocks pool.');

                this.draw();
                
                return block;
            },
            // I define this manually because IE<=8 js lists doesnt have the method indexOF()
            getIndex: function(element){
                var i = 0;
                for(i=0;i<basic_blocks.length;i++){
                    // We must check this is a "empty" container with only one element (the one we want).
                    if(basic_blocks[i].containsOnly(element))
                        return i;
                }
                return -1;
            },
            draw: function(){
                // Drawing concepts
                var little_boxes = [];
                
                var i=0;
                for(i=0;i<basic_blocks.length;i++){
                    little_boxes.push('<span unselectable="on" id="boolrelwidget-block');
                    little_boxes.push(basic_blocks[i].id);
                    little_boxes.push('" class="boolrelwidget-block">');
                    little_boxes.push('<span class="boolrelwidget-block-inner">');
                    little_boxes.push(basic_blocks[i].variables[0]);
                    little_boxes.push('</span>');
                    little_boxes.push('<span class="boolrelwidget-delete">');
                    little_boxes.push('X');
                    little_boxes.push('</span>');
                    little_boxes.push('</span>');

                }
                
                if(little_boxes.length == 0)
                    $('#boolrelwidget-basicblocks').html("You must add concepts before manipulating their logic.");    
                else
                    $('#boolrelwidget-basicblocks').html(little_boxes.join(''));
                
                // Drawing query itself(if any already)
                
                if(mastergroup && mastergroup.variables.length>0){
                    var big_box = [];
                    var i = 0;
                    this.harvest(mastergroup, big_box, 0);
                    
                    $('#boolrelwidget-query').html(big_box.join(''));
                    
                } else {
                    $('#boolrelwidget-query').html('Drag and Drop concepts here to start building a query...');
                }
            },
            // This recursive functions runs down in the BooleanGroups and puts everything on the big box.
            // I pass a counter to be able to style differently (so i know the recursion level couldnt find a better way to style it different
            harvest: function(something, big_box, counter){
                if(typeof something == 'string' || something instanceof String){
                    big_box.push(something);
                }
                else if(something instanceof BooleanGroup){
                    var k = 0;
                    
                    // First one doesnt have a operator associated
                    big_box.push('<div class="boolrelwidget-query-box-outer">');
                    if(counter%2 == 0)
                        big_box.push('<div class="boolrelwidget-odd boolrelwidget-query-box">');
                    else big_box.push('<div class="boolrelwidget-even boolrelwidget-query-box">');
                    this.harvest(something.variables[k++], big_box, counter+1);
   
                    // All others in the big box have
                    for(k=1;k<something.variables.length;k++){
                        // Add relation box
                        big_box.push(this.operator_selectbox(something.relations[k-1].name, counter));
                        
                        this.harvest(something.variables[k], big_box, counter+1);
                    }
                    big_box.push("</div>");
                    if(counter%2 == 0)
                        big_box.push('<div class="boolrelwidget-odd boolrelwidget-query-dropper">[drop]</div><div class="boolrelwidget-odd boolrelwidget-query-delete">X</div>');
                    else 
                        big_box.push('<div class="boolrelwidget-even boolrelwidget-query-dropper">[drop]</div><div class="boolrelwidget-even boolrelwidget-query-delete">X</div>');
                    
                    big_box.push('</div>');
                } else {
                    console.error(something+' cant be put in the big_box, because its not of type string nor BooleanGroup.');
                }
            },
            operator_selectbox: function(selected, counter){
                var select = [];

                select.push('<span class="boolrelwidget-query-operator"><select class="boolrelwidget-select">');

                
                for(var index in BOOL) {
                    if(BOOL[index].name == selected)
                        select.push('<option selected="selected">');
                    else
                        select.push('<option>');
                    select.push(BOOL[index].name);
                    select.push('</option>');
                }                
                select.push('</select></span>');
                
                return select.join('');
            }
        };

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
        self = self.append('<ul id="boolrelwidget-expand" class="boolrelwidget-menu-container"><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-l"><div class="boolrelwidget-arrow-up"></div></div></li><li class="boolrelwidget-menu">'+settings.expand_text+'</li><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-r"><div class="boolrelwidget-arrow-up"></div></div></li></ul><ul id="boolrelwidget-collapse" class="boolrelwidget-menu-container-panel"><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-l"><div class="boolrelwidget-arrow-down"></div></div></li><li class="boolrelwidget-menu">'+settings.collapse_text+'</li><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-r"><div class="boolrelwidget-arrow-down"></div></div></li></ul><div id="boolrelwidget-panel"><strong>Concepts</strong><div id="boolrelwidget-basicblocks">Loading...</div><strong>Boolean Query</strong><div id="boolrelwidget-query">Loading...</div></div>');


        
        // Lets add the event handlersx
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
        // Draw things up
        funcs.draw();
        
        return funcs;
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
    containsOnly : function(str){
        if(this.variables.length>1)
            return false;
        
        if(this.variables[0] == str)
            return true;
        
        return false;
    },
    destroy : function() {
        this.variables=null;
        this.relations=null;
        this=null;
    }
};