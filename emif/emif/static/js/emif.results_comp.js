var match=true;
var unmatch=true;
var emptyrows=true;
var proximity=true;

function hasFilters(){
  if(match == false || unmatch  == false|| emptyrows == false || proximity == false)
    return true;

  if($('#searchfilter').val().trim() != '')
    return true;

  // else 
  return false;
}

$("#collapseall").bind('click',function(e)
        { 
          //e.preventDefault(); 
          //e.stopPropagation();
          
          collapse_expand(this);
            
          return false;
        });

function collapse_expand(context){
          if ($(context).text().indexOf('Collapse')!==-1)
          {
            $(context).html('<i class="icon-plus"></i>&nbsp; Expand all');
            //change_name_collapse(false);

            $(".collapse:visible").collapse("hide");

          }
          else
          {
              $(context).html('<i class="icon-minus"></i>&nbsp; Collapse all');
              //change_name_collapse(true);
              $(".collapse:visible").collapse("show");
          }  
}
function doublecheck_expansions(){
          context = $("#collapseall");

          if ($(context).text().indexOf('Collapse')!=-1)
          {
              $(".collapse:visible").collapse("show"); 
          }
          else
          {
              $(".collapse.in:visible").collapse("hide");
          } 
}
function reset_empties(){
  $('#database_listings').show();
  $('#no_results').hide();
    
}


/*
 * delayKeyup
 * http://code.azerti.net/javascript/jquery/delaykeyup.htm
 * Inspired by CMS in this post : http://stackoverflow.com/questions/1909441/jquery-keyup-delay
 * Written by Gaten
 * Exemple : $("#input").delayKeyup(function(){ alert("5 secondes passed from the last event keyup."); }, 5000);
 */
(function ($) {
    $.fn.delayKeyup = function(callback, ms){
        var timer = 0;
        $(this).keyup(function(e){
            e.preventDefault(); 
            e.stopPropagation();  

            clearTimeout (timer);
            timer = setTimeout(callback, ms);
        });
        return $(this);
    };
})(jQuery);

$("#searchfilter").delayKeyup(
    function(){
      applyFilters();

      return false;
    }
  , 500);


function hidecheckbox()
{
  console.log("togle");
  $('.checkbox').toggle();
}


myFunc = function(name)
{
  //console.log(this);
  //console.log(name);
  var current = this.id;
  current = current.replace("a_", "");
  current = current.split("_")[0];
  //console.log(this.parent);
  
   $('div[id]').filter(function () {
    return /^collapse.*$/.test(this.id);
}).each(function (name2) {
    //console.log(name2);
});




$("div[id^='collapse']").filter(function(){
    var regexp = /^collapse(.*)$/;
    return (this.id.match(regexp));
}).each(function(){
    //this.innerHTML = this.id;
    //console.log(this.id);
    //console.log(current);
    if (!this.id.indexOf(current))
    { 
      $('#'+this.id).collapse('toggle'); 
    };
});



};
$('body').on('click', '.accordion-toggle', myFunc);

$.fn.textWidth = function() {
  var node, original, width;
  original = $(this).html();
  node = $("<span style='position:absolute;width:auto;left:-9999px'>" + original + "</span>");
  //node.css('font-family', $(this).css('font-family')).css('font-size', $(this).//css('font-size'));
  $('body').append(node);
  width = node.width();
  node.remove();
  return width;
};

function DatabaseSelector(container, num_visible, options){

  if(isNaN(num_visible)){
    console.error('-- Error: You must pass the number of visible databases at a time to the DatabaseSelector');
  }

  this.list = {};
  this.container = container;
  this.showing = [];
  this.reference = null;
  this.dropdown_subcontainer = null;
  this.visible = num_visible; 

  // optional configurations
  this.configs =  $.extend({
                    dropdown_subcontainer: null,
                    select_callback: null
                  }, options );
}
DatabaseSelector.prototype = {
  // Add the new database to the possibilities
  addDatabase: function(fingerprint_id, meta){
    this.list[fingerprint_id] = meta;

    // If we didn't yet fill the showing array up to visible size, add the new database to it
    if(this.showing.length < this.visible){
      this.showing.push(fingerprint_id);
    }
    if(this.reference == null){
      this.reference = fingerprint_id;
    }
  },
  // Delete the database from possibilities
  deleteDatabase: function(fingerprint_id){
    try {
      delete this.list[fingerprint_id];
    } catch(err) {
      console.warn('There was no database with id '+fingerprint_id+' to delete.');
    }
  },
  selectDatabase: function(old_fingerprint_id, new_fingerprint_id){

    var index_new = this.indexOfShowing(new_fingerprint_id);
    var index_list = this.indexOfList(new_fingerprint_id);

    var index_old = this.indexOfShowing(old_fingerprint_id);

    /* If the database to remove from showing is on the showing list */
    if( index_old != -1){
      /* if the new fingerprint isnt already showing and is on the list of possible databases*/
      if((index_new == -1 && index_list != null)){

        this.showing.splice(index_old, 1,  new_fingerprint_id);

      } 
      /* If the fingerprint is already showing and we just want to swap places */
      else if (index_new != -1 && index_list != null) {
        var temp = this.showing[index_old];
        this.showing[index_old] = this.showing[index_new];
        this.showing[index_new] = temp;        
      }

      if(old_fingerprint_id == this.reference){
        this.reference = new_fingerprint_id;
      } else if(new_fingerprint_id == this.reference){
        this.reference = old_fingerprint_id;
      }
      if(this.configs.select_callback){
        this.configs.select_callback();
      }
    } 

  },

  indexOfShowing: function(fingerprint_id){
    for(var i=0;i<this.showing.length;i++){
      if(this.showing[i] == fingerprint_id)
        return i;
    }

    return -1;
  },
  indexOfList: function(fingerprint_id){

    // ECMA5, only supported on IE>9, not a problem since we dropped support below IE9
    var list_keys = Object.keys(this.list);

    for(var i=0;i<list_keys.length;i++){
      if(list_keys[i] == fingerprint_id)
        return list_keys[i];
    }

    return null;
  },
  draw: function(){
    var self = this;
    var nodes = {};

    $(this.container).children().each(function(){
      $(this).removeClass('database_listing_away');
      if(self.configs.dropdown_subcontainer != null){
        $(this).find(self.configs.dropdown_subcontainer).html('');
      }
      nodes[$(this).attr('id').replace('db_','')] = $(this).remove();
    });

    // generate dropdowns, if possible
    if(self.configs.dropdown_subcontainer != null){
      for (var node in nodes) {
        if (nodes.hasOwnProperty(node)) {
          if(node == this.reference){
            nodes[node].find(self.configs.dropdown_subcontainer).html(this.__inverseintersectDropdown(node, true));
          } else {
            nodes[node].find(self.configs.dropdown_subcontainer).html(this.__inverseintersectDropdown(node, false));
          }
        }
      }
    }

    // They must be inserted in order, to maintain order synchronization
    for(var i=0;i<this.showing.length;i++){
      $(this.container).append(nodes[this.showing[i]]);
      delete nodes[this.showing[i]];
    }

    for (var node in nodes) {
      if (nodes.hasOwnProperty(node)) {
        var set_away = nodes[node];
        set_away.addClass('database_listing_away');
        $(this.container).append(set_away);
      }
    }

    $('.link_switch', self.container).click(function (event){
      event.preventDefault();

      var old_fingerprint = $(this).data('old');
      var new_fingerprint = $(this).data('new');

      self.selectDatabase(old_fingerprint, new_fingerprint);
      self.draw();

      return false;
    });
  },
  changeVisible: function(count){
    if(isNaN(count)){
      console.error('-- Error: You must pass a number to visibility');
    }
    this.visible = count;

    this.showing = this.showing.splice(0,count);

    this.draw();
  },
  __inverseintersectDropdown: function(not_fingerprint_id, reference){
    var temp = $.extend({}, this.list);
    delete temp[not_fingerprint_id];

    var dropdown=[];
    if(reference){
      dropdown.push('<div class="btn-group"><a style="font-size: 12px; font-weight: normal;" class="btn btn-success dropdown-toggle" data-toggle="dropdown" href="#">');
      dropdown.push('Reference');
    } else{
      dropdown.push('<div class="btn-group"><a style="font-size: 12px; font-weight: normal;" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#">');
      dropdown.push('Compared');
    }
    dropdown.push('&nbsp;<span class="caret"></span></a><ul class="pull-right dropdown-menu">');


    var tempkeys = Object.keys(temp);
    for(var i=0;i<tempkeys.length;i++){
      if(this.list[tempkeys[i]].label)
        dropdown.push('<li><a href="#" class="link_switch" data-old="'+not_fingerprint_id+'" data-new="'+tempkeys[i]+'">'+this.list[tempkeys[i]].label+'</a></li>');
      else
        dropdown.push('<li><a href="#" class="link_switch" data-old="'+not_fingerprint_id+'" data-new="'+tempkeys[i]+'">'+tempkeys[i]+'</a></li>');
    }
    dropdown.push('</ul></div>');

    return dropdown.join('');
  }
};
