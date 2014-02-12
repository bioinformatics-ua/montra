/**********************************************************************
#
# Author: Ricardo Ribeiro <ribeiro.r@ua.pt>
#
# */
(function ($) {
    $.fn.boolrelwidget = function (options) {
        // so we dont lose track of who we are, and used to ensure chainability
        var self = this;
        var basic_blocks = [];
        var used_blocks = [];
        var mastergroup=null;
        // Default Options
        var settings = $.extend({
            expand_text:'To define the relations between the terms click here.',
            collapse_text:'Click here to close this panel.'
        }, options);
        /*
        var bg1 = new BooleanGroup('teste de nome muito grande mesmo');
        var bg2 = new BooleanGroup('outro name ainda maior que o anterior, mas nao muito');
        var bg3 = new BooleanGroup('nome curto');
        
        var bg4 = new BooleanGroup(bg1);
        bg4.addBoolean(BOOL['OR'], bg2);
        
        mastergroup = new BooleanGroup(bg4);
        mastergroup.addBoolean(BOOL['AND'], bg3);
        
        basic_blocks.push(new BooleanGroup('outro nome grande, mas mesmo bue grande para ficar aqui para eu depois arranjar isto com ...'));
        */
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
            pushBooleanGroup: function (obj) {
                if(!(obj instanceof BooleanGroup && obj.variables.length == 1)){
                    console.warn('When adding, a valid simple BooleanGroup child must be found.');
                    return false;
                }
                if(!((typeof obj.variables[0] == 'string' || obj.variables[0] instanceof String)
                   && this.getIndex(obj.variables[0])== -1)){
                    console.warn('Variable ' + obj + ' already on basic blocks pool.');  
                    return false;
                }
                
                basic_blocks.push(obj);
                console.log('Pushed new variable ' + obj + ' to basic blocks pool.');

                this.draw();
                
                return true
            },
            splice: function (str) {
                var block;
                var id = this.getIndex(str)
                if(id < 0){
                    
                    // If it fails, lets check if its being used
                    var other_id = this.getUsedIndex(str);
                    if(other_id <0){
                        console.warn('No basic block ' + str + ' from basic blocks pool to slice out.');
                        return null;
                    }
                    
                    console.log('Variable is being used, removing it from mastergroup and removing it from used variables');
                    block = used_blocks.splice(other_id, 1)[0];
                    mastergroup.removeById(block.id);
                    
                    this.draw();
                    
                    return block;
                }
                block = basic_blocks.splice(id,1)[0];
                console.log('Sliced out variable ' + str + ' from basic blocks pool.');
                                
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
            getUsedIndex: function(element){
                var i = 0;
                for(i=0;i<used_blocks.length;i++){
                    // We must check this is a "empty" container with only one element (the one we want).
                    if(used_blocks[i].containsOnly(element))
                        return i;
                }
                return -1;
            },
            spliceById: function (number) {
                var id = this.getIndexById(number)
                if(id < 0){
                   console.warn('No basic block with id ' + number + ' from basic blocks pool to slice out.');
                   return null; 
                }
                var block = basic_blocks.splice(id, 1)[0];
                console.warn('Sliced out variable with id ' + number + ' from basic blocks pool.');
                
                this.draw();
                
                return block;
            },
            // I define this manually because IE<=8 js lists doesnt have the method indexOF()
            getIndexById: function(id){
                var i = 0;
                for(i=0;i<basic_blocks.length;i++){
                    // We must check this is a "empty" container with only one element (the one we want).
                    if(basic_blocks[i].id==id)
                        return i;
                }
                return -1;
            },
            draw: function(){
                // Drawing concepts
                var little_boxes = [];

                var i=0;
                for(i=0;i<basic_blocks.length;i++){
                    little_boxes.push('<span unselectable="on" class="btn-group boolrelwidget-block">');
                    little_boxes.push('<span id="boolrelwidget-bb-');
                    little_boxes.push(basic_blocks[i].id);
                    little_boxes.push('" class="btn boolrelwidget-block-inner">');
                    if(basic_blocks[i].variables[0].length > 10){
                        little_boxes.push('<div class="boolrelwidget-simple" data-toggle="tooltip" title="'+
                                     basic_blocks[i].variables[0]+'">');
                    }
                    little_boxes.push(basic_blocks[i].variables[0]);
                    if(basic_blocks[i].variables[0].length > 10){
                        little_boxes.push('</div>');
                    }
                    little_boxes.push('</span>');
                    //little_boxes.push('<span class="btn btn-danger boolrelwidget-delete">');
                    //little_boxes.push('X');
                    //little_boxes.push('</span>');
                    little_boxes.push('</span>');

                }
                
                if(little_boxes.length == 0){
                    $('#boolrelwidget-basicblocks').html("You must add concepts before manipulating their logic.");             
                } else{
                    $('#boolrelwidget-basicblocks').html(little_boxes.join(''));
                                    // Make them draggable
                    
                $(".boolrelwidget-block-inner").draggable({containment: "#boolrelwidget-panel", 
                                                           revert: true, opacity: 0.9, helper: "clone", cursor: "move", cursorAt: { top: 10, left: 50 }}); 
                }                
                
                // Drawing query itself(if any already)                
                if(mastergroup && mastergroup.variables.length>0){
                    var big_box = [];
                    var i = 0;
                    this.harvest(mastergroup, big_box, 0);
                    
                    $('#boolrelwidget-query').html(big_box.join(''));
                    
                    var master = this;
                    $( ".boolrelwidget-query-dropper" ).droppable({
                      drop: function( event, ui ) {
                        var droper = Number(ui.draggable.attr('id').replace('boolrelwidget-bb-',''));
                        var dropee = Number($(this).attr('id').replace('boolrelwidget-dp-',''));
                        console.log("Event drop: "+droper+" on "+dropee);
                        
                        var sliced = master.spliceById(droper);
                            
                          used_blocks.push(sliced);
                        // Try to add this to the master group
                        // If we cant, we insert the basic block back into the basic_blocks list
                        if(!mastergroup.addById(dropee, sliced)){
                            master.pushBooleanGroup(sliced);
                        }               
                        master.draw(); 

                      }
                    });
                        // Add 
                        $(".boolrelwidget-query-delete").click(function(){
                            var removed = Number($(this).attr('id').replace('boolrelwidget-dl-',''));
                            
                            var removed_bool = mastergroup.removeById(removed);
                            var contained = removed_bool.extractAllSimple();
                            
                            for(var j=0;j<contained.length;j++){
                                master.pushBooleanGroup(contained[j]);
                                
                                var other_id = master.getUsedIndex(contained[j].variables[0]);
                                if(other_id >0){
                                    console.log('Removing from used variables');
                                    used_blocks.splice(other_id, 1);
                                }
                            }

                            master.draw();
                        });
                        $(".boolrelwidget-simple").tooltip({container: 'body'});
                    
                        $(".boolrelwidget-select").change(function(){
                            console.log(mastergroup);
                            
                            var changed = $(this).attr('id').replace('boolrelwidget-query-sl-','');
                            changed = changed.split('-');
                            if(changed.length == 2){
                                console.log('Changed relationship to ' + $(this).val() + ' in ' + changed[0] + ' at position '+ changed[1]);
                                
                                mastergroup.changeRelation(Number(changed[0]), Number(changed[1]), BOOL[$(this).val()]);
                                
                                console.log(mastergroup);
                                
                            } else {
                                console.error('Impossible to select correctly a relation');
                            }
                        }); 
                        $(".boolrelwidget-collapser").click(function(){
                           
                            var collapsing = Number($(this).attr('id').replace('boolrelwidget-cl-',''));
                            if($(this).hasClass("boolrelwidget-collapsed")){
                                $(this).removeClass('boolrelwidget-collapsed');
                                $(this).addClass('boolrelwidget-expanded');
                                $(this).text('See nested relations');
                                $("#"+$(this).parent().attr('id')+' > .boolrelwidget-expandable').fadeOut('fast');
                                
                            } else {
                                $(this).removeClass('boolrelwidget-expanded');
                                $(this).addClass('boolrelwidget-collapsed');
                                $(this).text('Hide this relation');
                                $("#"+$(this).parent().attr('id')+' > .boolrelwidget-expandable').fadeIn('fast');
                                $("#"+$(this).parent().attr('id')+' > .boolrelwidget-expandable').css("display","table-cell");
                            }
                        }); 
                } else {
                    var master = this;
                    mastergroup=null;
                    $('#boolrelwidget-query').html('<div class="boolrelwidget-first-droppable">Drag and Drop concepts here to start building a query...</div>');
                                        
                  $( ".boolrelwidget-first-droppable" ).droppable({
                      drop: function( event, ui ) {
                        var droper = Number(ui.draggable.attr('id').replace('boolrelwidget-bb-',''));
                        console.log("Event drop: "+droper+" on empty space, creating new booleangroup.");
                        
                          var sliced = master.spliceById(droper);
                        
                        // Try to add this to the master group
                        // If we cant, we insert the basic block back into the basic_blocks list
                        mastergroup = new BooleanGroup(sliced);
                        
                        // Put in used blocks
                        used_blocks.push(sliced);

                        master.draw();  
                      }
                    });  
                }
                    // If we have collapsing preferences, apply them
                if(this.getCookie('boolrelwidget-collapse-preferences')){
                    console.log(this.getCookie('boolrelwidget-collapse-preferences'));
                    if(this.getCookie('boolrelwidget-collapse-preferences') == 'expanded'){
                        var context = $('boolrelwidget-collapseall');
                        $('#boolrelwidget-collapseall').text('Collapse All');
                        $('#boolrelwidget-collapseall').addClass('boolrelwidget-all-expanded');

                        this.collapseAll(context);  
                    } 
                }
            },
            // This recursive functions runs down in the BooleanGroups and puts everything on the big box.
            // I pass a counter to be able to style differently (so i know the recursion level couldnt find a better way to style it different
            harvest: function(something, big_box, counter){
                if(typeof something == 'string' || something instanceof String){
                    if(something.length > 10){
                        big_box.push('<div class="boolrelwidget-simple" data-toggle="tooltip" title="'+
                                     something+'">');
                    }
                    big_box.push(something);
                    if(something.length > 10){
                        big_box.push('</div>');
                    }
                }
                else if(something instanceof BooleanGroup){
                    var k = 0;
                    
                    // First one doesnt have a operator associated
                    big_box.push('<span class="btn-group boolrelwidget-query-box-outer" id="boolrelwidget-ob-');
                    big_box.push(something.id);
                    big_box.push('">');
                    if(counter%2 == 0){
                        if(!something.isSimple() && counter >0){
                            big_box.push('<div class="btn boolrelwidget-collapser boolrelwidget-collapsed" id="boolrelwidget-cl-');
                            big_box.push(something.id);
                            big_box.push('">See nested relations</div>');
                        }
                        big_box.push('<div class="btn boolrelwidget-odd boolrelwidget-query-box');
                        if( counter >0 && !something.isSimple())
                            big_box.push(' boolrelwidget-expandable');
                        big_box.push('">');
                    } else {
                        if(!something.isSimple() && counter >0){
                            big_box.push('<div class="btn btn-inverse boolrelwidget-collapser" id="boolrelwidget-cl-');
                            big_box.push(something.id);
                            big_box.push('">See nested relations</div>');
                        }
                        big_box.push('<div class="btn btn-inverse boolrelwidget-even boolrelwidget-query-box');
                        if( counter >0 && !something.isSimple())
                            big_box.push(' boolrelwidget-expandable');
                        big_box.push('">');
                    }
                    this.harvest(something.variables[k++], big_box, counter+1);
   
                    // All others in the big box have
                    for(k=1;k<something.variables.length;k++){
                        // Add relation box
                        big_box.push(this.operator_selectbox(something, k-1, counter));
                        
                        this.harvest(something.variables[k], big_box, counter+1);
                    }
                    big_box.push("</div>");
                    
                        big_box.push('<div id="boolrelwidget-dp-');
                        big_box.push(something.id);
                        if(counter%2 == 0){
                            big_box.push('" class="btn boolrelwidget-query-dropper');
                            if(!something.isSimple()  && counter >0)
                                big_box.push(' boolrelwidget-expandable');
                            big_box.push('"><div class="boolrelwidget-query-dropper-odd">&nbsp;&nbsp;</div></div>');
                        } else {
                            big_box.push('" class="btn btn-inverse boolrelwidget-query-dropper');
                            if(!something.isSimple() && counter >0)
                                big_box.push(' boolrelwidget-expandable');
                            big_box.push('"><div class="boolrelwidget-query-dropper-even">&nbsp;&nbsp;</div></div>');
                        }
                    
                    // Cant delete mastergroup, other can be deleted
                    if(counter!=0){
                        if(counter%2 == 0)
                            big_box.push('<div class="btn boolrelwidget-query-delete');
                        else
                            big_box.push('<div class="btn btn-inverse boolrelwidget-query-delete');
                        
                        if(!something.isSimple())
                            big_box.push(' boolrelwidget-expandable');
                        
                        big_box.push('" id="boolrelwidget-dl-');                        
                        big_box.push(something.id);
                        
                        if(counter%2 == 0)
                            big_box.push('"><div class="boolrelwidget-query-delete-odd"></div></div>');
                        else 
                            big_box.push('"><div class="boolrelwidget-query-delete-even"></div></div>');
                    }
                    
                    big_box.push('</span>');
                } else {
                    console.error(something+' cant be put in the big_box, because its not of type string nor BooleanGroup.');
                }
            },
            operator_selectbox: function(something, selected, counter){
                var select = [];
                var relation = something.relations[selected].name;
                
                select.push('<span class="boolrelwidget-query-operator"><select id="boolrelwidget-query-sl-');
                select.push(something.id);
                select.push('-');
                select.push(selected);
                select.push('" class="boolrelwidget-select">');

                for(var index in BOOL) {
                    if(BOOL[index].name == relation)
                        select.push('<option selected="selected">');
                    else
                        select.push('<option>');
                    select.push(BOOL[index].name);
                    select.push('</option>');
                }                
                select.push('</select></span>');
                
                return select.join('');
            },
            reset: function(){
                if(mastergroup != null){
                    var simples = mastergroup.extractAllSimple();
                    mastergroup=null;
                    used_blocks=[];
                    for(var i=0;i<simples.length;i++)
                        this.pushBooleanGroup(simples[i]);
                }
            },
            opAll: function(func){
                if(!isBool(func)){
                    console.error('Tried to make a op_all operatiom with a invalid bool enum');
                    return false;
                }    
                // First we reset
                    this.reset();
                
                // Then we add all to a new mastergroup
                if(basic_blocks.length>0){
                    var j=0;
                    mastergroup = new BooleanGroup(basic_blocks[j++]);
                    for(var j=1;j<basic_blocks.length;j++){
                        mastergroup.addBoolean(func, basic_blocks[j]);
                    }
                    
                used_blocks=basic_blocks;
                basic_blocks=[];                
                }
                this.draw();
                    
                return true;
            },
            /* Ref on this on : http://stackoverflow.com/questions/1458724/how-to-set-unset-cookie-with-jquery */
            setCookie: function(key, value){
                var expires = new Date();
                expires.setTime(expires.getTime() + (1 * 24 * 60 * 60 * 1000));
                document.cookie = key + '=' + value + ';path=/' + ';expires=' + expires.toUTCString();
            },
            getCookie: function(key){
                var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
                return keyValue ? keyValue[2] : null;            
            },
            collapseAll: function(context){
            
                if($(context).hasClass('boolrelwidget-all-expanded')){
                
                    $('.boolrelwidget-expandable').fadeOut('fast');
                    $("#"+$('.boolrelwidget-expandable').parent().attr('id')+' > .boolrelwidget-collapser').text('See nested relations');

                    $(context).text('Expand All');
                    $(context).removeClass('boolrelwidget-all-expanded');
                    
                    funcs.setCookie('boolrelwidget-collapse-preferences','collapsed');
                } else {
                    
                    $('.boolrelwidget-expandable').fadeIn('fast').css('display','table-cell');
                    $("#"+$('.boolrelwidget-expandable').parent().attr('id')+' > .boolrelwidget-collapser').text('Hide this relation');
                    $(context).text('Collapse All');
                    $(context).addClass('boolrelwidget-all-expanded');
                    
                    funcs.setCookie('boolrelwidget-collapse-preferences','expanded');
                }
            
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
        self = self.append('<ul id="boolrelwidget-expand" class="boolrelwidget-menu-container"><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-l"><div class="boolrelwidget-arrow-up"></div></div></li><li class="boolrelwidget-menu">'+settings.expand_text+'</li><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-r"><div class="boolrelwidget-arrow-up"></div></div></li></ul><ul id="boolrelwidget-collapse" class="boolrelwidget-menu-container-panel"><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-l"><div class="boolrelwidget-arrow-down"></div></div></li><li class="boolrelwidget-menu">'+settings.collapse_text+'</li><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-r"><div class="boolrelwidget-arrow-down"></div></div></li></ul><div id="boolrelwidget-panel"><strong>Concepts</strong><div id="boolrelwidget-basicblocks" class="well well-small">Loading...</div><div class="clearfix"><div class="boolrelwidget-menu pull-left"><strong>Boolean Query</strong></div><div class="pull-right boolrelwidget-menu btn-group"><button id="boolrelwidget-collapseall" class="btn">Expand All</button><button class="btn" id="boolrelwidget-orall">Or All Concepts</button><button class="btn" id="boolrelwidget-andall">And All Concepts</button><button class="btn" id="boolrelwidget-clear">Reset</button></div></div><div id="boolrelwidget-query" class="well well-small">Loading...</div></div>');
        
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
        
        $( '#boolrelwidget-collapseall' ).click(function() {
            funcs.collapseAll(this);
        });
        $( '#boolrelwidget-orall' ).click(function() {
            funcs.opAll(BOOL['OR']);          
        });   
        $( '#boolrelwidget-andall' ).click(function() {
            funcs.opAll(BOOL['AND']);
        });
        $( '#boolrelwidget-clear' ).click(function() {
            funcs.reset();
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
  NOP   : { value: -1, name: "NOP"}, // No operation, means its a edge branch 
  AND   : { value: 0, name: "AND"}, 
  OR    : { value: 1, name: "OR"}, 
  XOR   : { value: 2, name: "XOR"}
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
    /* While i realize this approach isnt the best, i was having problems with the recursivity and this worked
     * Maybe to review with more time at a later time
    */
    removeById : function(other_id){
        var returnable = []
        this.removeByIdAux(null, null, other_id,returnable);
        
        if(returnable.length==1)
            return returnable[0]
            
        else 
            return null;

    },
    removeByIdAux : function(parent, branch, other_id, returnable) {
        if(typeof other_id != 'number'){
            console.warn('When removing by id, a number value must be specified. Found type ' + typeof other_id);
        }
        else {
            if(this.id == other_id){
                // If not on root remove reference
                if(parent){
                    parent.variables.splice(branch,1);
                    if(branch=0)
                        parent.relations.splice(branch,1);
                    else 
                        parent.relations.splice(branch-1,1);
                }
                
                returnable.push(this);
            }
            var k = 0;
            for(k=0;k<this.variables.length;k++){
                if(this.variables[k] instanceof BooleanGroup){
                    this.variables[k].removeByIdAux(this, k, other_id, returnable);
                }
            }
        }
    },     
    addById : function(parent_id, child){
        if(!(child instanceof BooleanGroup)){
            console.warn('When adding, a valid BooleanGroup child must be found.');
        }
        return this.addByIdAux(parent_id, child); 
    },    
    addByIdAux : function(parent_id, child) {
        if(typeof parent_id != 'number'){
            console.warn('When adding by id, a number value must be specified. Found type ' + typeof parent_id);
        }
        else {
            if(this.id == parent_id){
                //Add reference
                this.relations.push(BOOL['OR']);
                this.variables.push(child);
                return true;
            }
            var returnable=false;
            var k = 0;
            for(k=0;k<this.variables.length;k++){
                if(this.variables[k] instanceof BooleanGroup){
                    returnable = this.variables[k].addByIdAux(parent_id, child);
                }
            }
            return returnable;
        }
    }, 
    changeRelation: function(container_id, index, new_value){
        if(typeof container_id != 'number'){
            console.warn('When changing a relation the id must be a number. Found type ' + typeof parent_id);
        }
        else if(typeof index != 'number'){
            console.warn('When changing a relation the index must be a number. Found type ' + typeof parent_id);
        }   
        else if(!isBool(new_value)){
            console.warn('When changing a relation the new value must be a valid BOOL enum.');
            
        } else {
            console.log("IDs: "+this.id+'=='+ container_id);

            if(this.id == container_id){
            
              if(this.variables.length > index){
                this.relations[index] = new_value;
                //  this.relations.splice(index,1,new_value);
              }  
                return;
            }     
            for(var k=0;k<this.variables.length;k++){
                if(this.variables[k] instanceof BooleanGroup){
                    this.variables[k].changeRelation(container_id, index, new_value);
                }
            }            
        }
    },
    containsOnly : function(str){
        if(this.variables.length>1)
            return false;
        
        if(this.variables[0] == str)
            return true;
        
        return false;
    },
    isSimple : function(){
        if(this.variables.length == 1 && (typeof this.variables[0] == 'string' || this.variables[0] instanceof String))
            return true;
        
        return false;
    },
    extractAllSimple : function(){
        var returnable = [];
        
        if(this.isSimple())
            returnable.push(this);
        else
            this.extractAllSimpleAux(returnable);
        
        return returnable;
    }, 
    extractAllSimpleAux : function(returnable){
           
        var k=0;    
        for(k=0;k<this.variables.length;k++){
            if(this.variables[k].isSimple())
                returnable.push(this.variables[k]);
            else
                this.variables[k].extractAllSimpleAux(returnable);
        } 
            
    },
    destroy : function() {
        this.variables=null;
        this.relations=null;
    }
};