var match=true;
var unmatch=true;
var emptyrows=true;
var proximity=true;

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
function check_empties(){
  var dbs_visible = $('#database_listings .database_listing:not(.database_listing_away) .accordion-group:visible').length;

  if(dbs_visible == 0){
    $('#database_listings').hide();
    $('#no_results').show();

  } else {
    $('#database_listings').show();
    $('#no_results').hide();

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

/*

function highlight(text, text_to_highlight)
{
    inputText = document.getElementById("inputText")
    var innerHTML = inputText.innerHTML
    var index = innerHTML.indexOf(text);
    if ( index >= 0 )
    { 
        innerHTML = innerHTML.substring(0,index) + "
<span class='highlight'>" + innerHTML.substring(index,index+text.length) + "</span>
" + innerHTML.substring(index + text.length);
        inputText.innerHTML = innerHTML 
    }

}

*/

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

function CustomSort( a ,b ){

     if($(a).find('.set_reference').first().hasClass('btn-primary'))
      return -1;
     if($(b).find('.set_reference').first().hasClass('btn-primary'))
      return 1;  

     else return 0;
}

// Ref from : http://dotnetspeak.com/2013/05/creating-simple-please-wait-dialog-with-twitter-bootstrap/comment-page-1
var loading_modal;
loading_modal = loading_modal || (function () {
    var pleaseWaitDiv = $('<div class="modal hide" id="pleaseWaitDialog" data-backdrop="static" data-keyboard="false"><div class="modal-header"><h3>Comparing databases, please wait...</h3></div><div class="modal-body"><div class="progress progress-striped active"><div class="bar" style="width: 100%;"></div></div></div></div>');
    return {
        showPleaseWait: function() {
            pleaseWaitDiv.modal();
        },
        hidePleaseWait: function () {
            pleaseWaitDiv.modal('hide');
        },

    };
})();

$('#database_listings .database_listing').sort(CustomSort).appendTo('#database_rows');


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
                    dropdown_subcontainer: null
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

    /* If the database to remove from showing is on the showing list, and
     * if the new fingerprint isnt already showing and is on the list of possible databases*/
    if( index_old != -1 && 
        (index_new == -1 && index_list != null)){
      this.showing.splice(index_old, 1,  new_fingerprint_id);

      /*if(old_fingerprint_id == this.reference){
        this.setAsReference(new_fingerprint_id);
      }*/

    }

  },
  setAsReference: function(new_fingerprint_id){
    var is_new = this.indexOfShowing(new_fingerprint_id);

    /* If the database is new to the showing display, 
     * we must first add it to the showing display and remove the old reference */
    if(is_new == -1){
      this.selectDatabase(this.reference, new_fingerprint_id);
    }
    /* Otherwise, we must make it swap places with the old reference without removing anything */
    else {
      // swap places
      var old_reference_index = this.indexOfShowing(old_fingerprint_id);
      var new_reference_index = this.indexOfShowing(new_fingerprint_id);

      var temp = this.showing[old_reference_index];
      this.showing[old_reference_index] = this.showing[new_reference_index];
      this.showing[new_reference_index] = temp;
    }
    this.reference = new_fingerprint_id;

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

      console.log('INDEX OLD:'+new_fingerprint);
      console.log('INDEX NEW:'+old_fingerprint);

      self.selectDatabase(old_fingerprint, new_fingerprint);
      self.draw();

      return false;
    });
  },
  __inverseintersectDropdown: function(not_fingerprint_id, reference){
    var temp = $.extend({}, this.list);
    delete temp[not_fingerprint_id];

    var dropdown=[];
    dropdown.push('<div class="btn-group"><a style="font-size: 12px; font-weight: normal;" class="btn btn-info dropdown-toggle" data-toggle="dropdown" href="#">');
    if(reference)
      dropdown.push('Reference');
    else
      dropdown.push('Compared');

    dropdown.push('&nbsp;<span class="caret"></span></a><ul class="dropdown-menu">');


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
