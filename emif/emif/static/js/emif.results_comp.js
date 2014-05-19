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


function DatabaseSelector(num_visible){

  if(isNan(num_visible)){
    console.error('You must pass the number of visible databases at a time to the DatabaseSelector');
  }

  this.list = {};
  this.showing = [];
  this.visible = num_visible;
}
DatabaseSelector.prototype = {
  addDatabase: function(fingerprint_id, identificator){
    this.list[fingerprint_id] = identificator;
  }
  deleteDatabase: function(fingerprint_id){
    try {
    del this.list[fingerprint_id];
    } catch(err) {
      console.warn('There was no database with id '+fingerprint_id+' to delete.');
    }
};
