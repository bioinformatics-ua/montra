/**********************************************************************
# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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
***********************************************************************/


/********************************************************
**************** Population Characteristics API 
*********************************************************/




// This is the mode 
var PAGE_TYPE = "PC";
// This is the mode that exists right now
var PC_NORMAL = "PC_NORMAL"; // Population Characteristics for one database
var PC_COMPARE = "PC_compare"; // Population Characteristics for many databases

var filter_dropdown;

function getPageType()
{
  var url = document.URL;
  if (url.indexOf("compare")!=-1)
  {
    PAGE_TYPE =PC_COMPARE;
  }
  else
  {
    PAGE_TYPE = PC_NORMAL;
  }
};

getPageType();
var defaultFingerprintID = "NONE";
if (PAGE_TYPE==PC_COMPARE)
{
  defaultFingerprintID = "COMPARE"
}
function getFingerprintID(){
  var url = document.URL;
  var fingerprint_id='abcd';

  try{
    fingerprint_id = global_fingerprint_id;
  }
  catch(err){
    fingerprint_id=defaultFingerprintID;
  };
  return fingerprint_id;

};

function getRevision(){
  var url = document.URL;
  var revision='-1';

  try{
    revision = global_revision;
  }
  catch(err){
    console.error('Error retrieving revision from pop.char.');
  };
  return revision;

};

var filtersMap = {};
var translations = {};
var translationsBack = {};
var activeChart='';

var actualChart = null; 


/** TODO: there are a lot of static and hardcore parameters in this function
  * This need to be fixed */ 
function PCAPI (endpoint) 
{

    if (endpoint==null)
    {
      this.endpoint="population/jerboalistvalues";  
    }
    else {
      this.endpoint=endpoint;
    }
    
    // This was already globally defined, but ie8, for some obscure reason cant find it...
    $.ajaxSetup({
                crossDomain: false, // obviates need for sameOrigin test
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
                        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                    }
                }
    });
    
    this.getValuesRow = function(Var, Row, fingerprintID, revision){
        var result = {}

        console.log(result);
          
        $.ajax({
          dataType: "json",
          url: this.endpoint+"/"+Var+"/"+Row+"/" + fingerprintID+"/"+revision,

          async: false,
          type: "POST",
          data: { publickey: global_public_key, result: result },
          success: function (data){result=data;}
        });
        return result;
    };
     this.getValuesRowWithFilters = function(Var, Row, fingerprintID, revision, filters){
        var result = {}

        console.log(filters);


        $.ajax({
          dataType: "json",
          url: this.endpoint+"/"+Var+"/"+Row+"/" + fingerprintID + "/" + revision,
          async: false,
          type: "POST",
          data: { publickey: global_public_key, filters: filters },
          success: function (data){
            result=data;
          }
        });

        

        return result;
    };

    this.getFilter = function(Var, fingerprintID){
        var result = {} ;
        $.ajax({
          dataType: "json",
          url: "population/filters/"+Var+"/" + fingerprintID,
          async: false,
          type: "POST",
          data: { publickey: global_public_key, result: result },        
          success: function (data){result=data;}
        });
        return result;
    };

};

/********************************************************************
**************** Population Characteristics - Bar (Jquery Plugin) v2 (using dyndropdown)
*********************************************************************/

 (function( $ )
 {

    /** Draft code */ 
    function getFiltersSelected(){

      return filtersMap;

    };

    
    translations = {};
    translationsBack = {};
    

    var methods = {
        init : function( options, name, fingerprintId ) {

            
            /** Get a list of filters */
            values = options.getFilter(name,fingerprintId);

            if (values===undefined)
            {
                return;
            };

            filtersMap = {}
            var self = this;
            /*self.html('');*/


            filters_tmp = [];
            
            JSON_OUTPUT = {};

            values.values.forEach(function(_value){

              var xFilter = JSON.parse(_value);

              filters_tmp.push(xFilter);
              if (!xFilter.show)
                return;
              
              self.append(xFilter.name+": ");
              var options = {};

              //var tmpUl = $('<ul class="nav nav-pills nav-stacked">');

              //self.append(tmpUl);

              // This code is only for comparison mode 
              //console.log(xFilter);
              if (xFilter.name == "Gender")
              {
                  if (xFilter.translation.hasOwnProperty("ALL"))
                  {
                    xFilter.values.push("ALL");  
                    options['ALL'] = 'ALL';               
                  }
                  
              }


              $.each(xFilter.values, function (data){
                  
                  if (xFilter.values[data]==="")
                      return;


                  var fType = xFilter.name;
                  if (xFilter.key!= null)
                  {
                    fType = xFilter.value;

                  }
                  var originalValue = xFilter.values[data];
                  //console.log("originalValue");
                  //console.log(originalValue);
                  if (xFilter['translation'] != null)
                  {
                    if (xFilter['translation'].hasOwnProperty(originalValue))
                    {
                        translations[originalValue] = xFilter['translation'][originalValue];
                        translationsBack[xFilter['translation'][originalValue]] = originalValue;
                        originalValue = xFilter['translation'][originalValue];
                    }
                      
                  }
                  
                 
                  //tmpUl.append('<li><a class="filterBar '+fType+'" id=_'+fType+'_'+xFilter.values[data]+' href="#" onclick="return false;"> '+originalValue+'</a></li>')
                  options[xFilter.values[data]] = originalValue;                  
                    
              });
              JSON_OUTPUT[xFilter.value] = {values: options, name: xFilter.name};
            });
            //console.log('JSON_OUTPOUT');
            //console.log(JSON.stringify(JSON_OUTPUT));
            

            filter_dropdown = $(this).dyndropdown({
                    label: "Filter", 
                    dropup: false, 
                    alwaysOneOption: true,
                    onSelectionChanged: function(selection){
                        //console.log('callback called');
                        //console.log(selection);
                        
                        var charDraw = new PCDraw(actualChart, activeChart, null);

                        for(filter in selection){
                          var options_translated = [];

                          for(var i=0;i<selection[filter].length;i++){
                            var _value = selection[filter][i];
                            
                            options_translated.push(_value);

                          }

                          filtersMap['values.'+filter] = options_translated;
                        }
                        //console.log('NEW FILTERS:');
                        //console.log(filtersMap);
                        charDraw.refresh(filtersMap);
                    }
            });

            filter_dropdown.setStructure(JSON.stringify(JSON_OUTPUT));

            actualChart.filters = filters_tmp;

            var match=false;

        },
        draw : function( options ) {
            
        }
    };

    $.fn.populationChartsBar2 = function(method) {
        // Method calling logic
        if ( methods[method] ) {
        return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
        return methods.init.apply( this, arguments );
        } else {
        $.error( 'Method ' + method + ' does not exist on jQuery.populationCharts2' );
        }
        return this;
    };
}( jQuery ));

/********************************************************************
**************** Population Characteristics - Bar (Jquery Plugin) 
*********************************************************************/

 (function( $ )
 {

    /** Draft code */ 
    function getFiltersSelected(){

      return filtersMap;

    };

    
    translations = {};
    translationsBack = {};
    

    var methods = {
        init : function( options, name, fingerprintId ) {

            
            /** Get a list of filters */
            values = options.getFilter(name,fingerprintId);

            if (values===undefined)
            {
                return;
            };

            filtersMap = {}
            var self = this;
            self.html('');


            filters_tmp = [];
            
            values.values.forEach(function(_value){

              var xFilter = JSON.parse(_value);

              filters_tmp.push(xFilter);
              if (!xFilter.show)
                return;
              
              self.append(xFilter.name+": ");
              var tmpUl = $('<ul class="nav nav-pills nav-stacked">');

              self.append(tmpUl);

              // This code is only for comparison mode 
              console.log(xFilter);
              if (xFilter.name == "Gender")
              {
                  if (xFilter.translation.hasOwnProperty("ALL"))
                  {
                    xFilter.values.push("ALL");                  
                  }
                  
              }


              $.each(xFilter.values, function (data){
                  
                  if (xFilter.values[data]==="")
                      return;


                  var fType = xFilter.name;
                  if (xFilter.key!= null)
                  {
                    fType = xFilter.value;

                  }
                  var originalValue = xFilter.values[data];
                  console.log("originalValue");
                  console.log(originalValue);
                  if (xFilter['translation'] != null)
                  {
                    if (xFilter['translation'].hasOwnProperty(originalValue))
                    {
                        translations[originalValue] = xFilter['translation'][originalValue];
                        translationsBack[xFilter['translation'][originalValue]] = originalValue;
                        originalValue = xFilter['translation'][originalValue];
                    }
                      
                  }
                  
                 
                  tmpUl.append('<li><a class="filterBar '+fType+'" id=_'+fType+'_'+xFilter.values[data]+' href="#" onclick="return false;"> '+originalValue+'</a></li>')
                    
                  
                    
              });


            });
            
            actualChart.filters = filters_tmp;


            /** The magic of the filters will happen here */ 
            $(".filterBar").bind('click',function(e)
                    { 
                      e.preventDefault(); 
                      e.stopPropagation();

                      console.log()

                      var charDraw = new PCDraw(actualChart, activeChart, null);

                      var str = e.target.id;
                      var filterType =str.substring(str.indexOf("_")+1,str.lastIndexOf("_"));

                      console.log('filterType:'+filterType);

                      var _value = e.target.innerHTML.trim();
                      if (translationsBack.hasOwnProperty(_value))
                      {
                          _value = translationsBack[_value];
                      } 
                      /*if(filtersMap['values.'+filterType])
                      {
                        filtersMap['values.'+filterType] = [_value, filtersMap['values.'+filterType][0]];
                      }
                      else
                      {
                        filtersMap['values.'+filterType] = [_value];  
                      }*/
                      filtersMap['values.'+filterType] = [_value];  
                      console.log("filtersSelected:");
                      console.log(getFiltersSelected());
                      charDraw.refresh(getFiltersSelected());
                      
                      
                      $("." + filterType).closest('li').removeClass("active");
                      $(this.parentNode).closest('li').addClass("active");
                      

                      return false;
                    });

            var match=false;

        },
        draw : function( options ) {
            
        }
    };

    $.fn.populationChartsBar = function(method) {
        // Method calling logic
        if ( methods[method] ) {
        return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
        return methods.init.apply( this, arguments );
        } else {
        $.error( 'Method ' + method + ' does not exist on jQuery.populationCharts' );
        }
        return this;
    };
}( jQuery ));


/********************************************************************
**************** Population Characteristics Types
*********************************************************************/

 (function( $ )
 {

    var PC = null;
    var chartTypes = null; 
    function Filters()
    {
      this.drawFilters = function(){
      };
      this.bindFilters = function(){

            /*** The magic of the changing of the type of the graph happens here */

            $(".graphTypes").bind('click',function(e)
                    { 
                      e.preventDefault(); 
                      e.stopPropagation();

                      // This code is needed for comparison zone
                      filtersMap = {};
                      translations = {};
                      translationsBack = {};

                      $("#pc_comments_placeholder").html("");

  
                      
                      // Anyone have a better suggestion to do it?
                      // I'm more focuses in other staff right now.
                      // Bastiao, 2014.Feb.09
                      $('.graphTypes').closest('li').removeClass('active')
                      $(this.parentNode).closest('li').addClass('active')

                      chartTypes.forEach(function(a){
                          
                          if (a.title.fixed_title==e.target.innerHTML) 
                          {
                              actualChart = a;
                          }
                          
                      });
                      if (actualChart==null)
                      {
                          // do something here like an abort or shit! 
                      }

                      // Comments ids
                      var fid = getFingerprintID();
                      $("#pc_chart_comment_id").val(actualChart.uid);
                      $("#pc_chart_comment_fingerprint_id").val(fid);

                      cm = new CommentsManager();
                      cm.listComments(fid, actualChart.uid);
                      
                      var charDraw = new PCDraw(actualChart, actualChart.title['var'], e);
                      var _filters = {};
                      charDraw.draw(_filters);
                      charDraw.drawBar();
                      $(".filterBar").last().click();   
                      $(".filterBar").first().click(); 

                      
                      return false;
                    });
      };
      this.drawScales = function(){
      };
      this.bindScales = function(){
      };   
    };

    var methods = {
        init : function( options, api ) {

            var self = this;
            self.append("Characteristic Type: ");
            tmpUl = $('<ul class="nav nav-list nav-pills nav-stacked">');
            values = options.getChartTitles(getFingerprintID());
            var configs = new PCConfs();
            var charts = configs.getSettings(getFingerprintID());
            chartTypes = charts;
            self.append(tmpUl);
            $.each(values, function (data){
                if (values[data]==="")
                    return;

                tmpUl.append('<li class=""><a class="graphTypes" href="#" onclick="return false;">'+values[data]+'</a></li>')
            });

            var myPC = options;
            
            filters = new Filters();
            filters.bindFilters();

        },
        draw : function( options ) {
            
        }
    };

    $.fn.populationChartsTypes = function(method) {
        // Method calling logic
        if ( methods[method] ) {
        return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
        return methods.init.apply( this, arguments );
        } else {
        $.error( 'Method ' + method + ' does not exist on jQuery.populationChartsTypes' );
        }
        return this;
    };
}( jQuery ));


$(document).ready(
    function(){


        var chartLayout = new ChartLayout();

        $("#pc_list").populationChartsTypes(chartLayout, PCAPI);
        $("#pc_list").populationChartsTypes('draw', chartLayout); 

          $('.tabbable a[data-toggle="tab"]').on('shown', function (e) {
            if($(e.target).text().indexOf('Population Characteristics')>-1){
              $(".graphTypes").first().click();

              $(".filterBar").first().click(); 
            }
          });

        }
    
);
