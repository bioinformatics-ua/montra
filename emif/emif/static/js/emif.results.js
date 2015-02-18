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
#
*/
var counter = 0;
var a;
var fingerprints_ids = null;
var bool_container;

function initializePaginatorSorter(base_filter, selected_name, selected_value, extra){
    a = new PaginatorSorter("table_databases", base_filter, selected_name, selected_value, extra);

    //TO Be Applied in future releases.
    a.atachPlugin(new SelectPaginatorPlugin());

  if(a != undefined && a.plugin != undefined){

    var dbcount = updateSelectCount();

    counter = dbcount;

    if(dbcount >= 2){
        $("#comparabtn").removeAttr('disabled');
        $("#comparabtn").bind('click',function(e)
        {
          $('#compare_form').attr('action', 'resultscomp');
          postComparison(true);
          return false;
        });

    }

  }

    $('a[href="#"]').attr('href', function(i, val){
        return window.location + val;
    });

    $('.help_selectresults').tooltip({container: 'body', 'html': true});


}
function setRefineEvent(is_advanced, query_type, query_id){
      $("#refine_search_btn").click( function(){
      if(is_advanced)
        window.location.replace($('#base_link').prop('href')+"advancedSearch/"+query_type+"/1/"+query_id);
      else
        $("input[name=query]").focus();

    });
}

function setBooleanPlugin(serialization_query, query_type, query_id){
    bool_container = $('#bool_container').boolrelwidget({view_only: true, view_serialized_string: serialization_query, link_back: $('#base_link').prop('href')+"advancedSearch/"+query_type+"/1/"+query_id });

    window.setTimeout(function(){window.location.hash = "#back";}, 100);
    window.setTimeout(function(){window.location.hash = "#search";}, 100);

      /* This is a trick, to be able to redirect on back button since browsers try to prevent us to do so
       I must do this, because the back url is different from the url on history */
    window.onhashchange = function(){
       if (location.hash == "#back") {
            window.location.replace($('#base_link').prop('href')+"advancedSearch/"+query_type+"/1/"+query_id);
        }

    }
}

function updateSelectCount(){

    try{
    var dbs = a.plugin.getExtraObjects().selectedList;
    fingerprints_ids = a.plugin.getExtraObjects().selectedList;
    var type = a.plugin.typedb;

    if(type)
      $('#selected_dbstype').text(type);
    else
      $('#selected_dbstype').text("---");

    $('#selected_dbscount').text(dbs.length);

    return dbs.length;

    } catch(err){
      $('#selected_dbscount').text(0);
    }

    return 0;
    }
function updateSelectCountJs(type, count){

    if(type)
      $('#selected_dbstype').text(type);

    if(count)
      $('#selected_dbscount').text(count);

}
function hidecheckbox()
{
  $('.checkbox').toggle();
}

$("#comparabtn").bind('click',function(e)
        {

          e.preventDefault();
          e.stopPropagation();
          return false;
        });

//$("#comparabtn").unbind();
function postComparison(isdbs){
  //$('#result_form').submit();
  //console.log('A: '+a);
  //console.log('A-plugin: '+a.plugin);
  if(a != undefined && a.plugin != undefined){
    $('#comparedbs').html('');

    var dbs = a.plugin.getExtraObjects().selectedList;
    //console.error(dbs.length);
    for(var i=0;i<dbs.length;i++){
      $('#comparedbs').append('<input type="checkbox" name="chks_'+dbs[i]+'" checked>');
    }
    var ids = [];
    $('[name^="chks_"]').each(function(){

      var id = $(this).attr('name').split('_')[1];

      ids.push(id);

    });
    if(!isdbs)
      checkExistsPopulation(ids);
    else $('#submitdbsimulate').click();
  }

}
$('.checkbox').click(function()
{

    if($(this).is(':checked')){
        counter++;
    } else
    {
        counter--;
    }



    if(counter == 0){
      updateSelectCountJs("---", ""+counter);
      $('input.checkbox').prop("disabled", false);

      $("#comparabtn").attr("disabled", true);
    }
    else if(counter == 1){
    console.log('cai here');

      $("#comparabtn").attr('disabled', true);

      var checkedtype;
      if(a != undefined && a.plugin != undefined && a.plugin.typedb !=undefined){
        checkedtype = a.plugin.typedb;
      } else {
        checkedtype = $('.checkbox:checked').first().attr('typedb');
      }
      updateSelectCountJs(checkedtype, counter);

      $('input.checkbox').prop("disabled", false);

      $('input.checkbox:not([typedb="' + checkedtype
      + '"])').prop('disabled', true);


    }
    else if (counter >= 2){
      updateSelectCountJs(null, counter);
      $("#comparabtn").attr('disabled', false);
         $("#comparabtn").bind('click',function(e)
        {
          $('#compare_form').attr('action', 'resultscomp');
          postComparison(true);
          return false;
        });
    }

});
$('[rel=tooltip]').tooltip({container: 'body', 'html': true});

$('.popover').popover({
    container: 'body'
});
$('.accordion-body.collapse').hover(
function () {
$(this).css('overflow','visible');
},
function () {
$(this).css('overflow','hidden');
}
);
