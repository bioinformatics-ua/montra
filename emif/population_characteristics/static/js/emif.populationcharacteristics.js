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

function getFingerprintID(){
  var url = document.URL;
  var fingerprint_id='abcd';

  try{
    fingerprint_id = url.split("fingerprint/")[1].split("/1")[0];
  }
  catch(err){
    fingerprint_id='abcde'
  };
  return fingerprint_id;

};

var filtersMap = {};
var translations = {};
var translationsBack = {};
var activeChart='';

var actualChart = null; 


/** TODO: there are a lot of static and hardcore parameters in this function
  * This need to be fixed */ 
function PCAPI () 
{
    // This was already globally defined, but ie8, for some obscure reason cant find it...
    $.ajaxSetup({
                crossDomain: false, // obviates need for sameOrigin test
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
                        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                    }
                }
    });
    this.getGender = function(){
        var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Active patients/Gender/abcd",
          async: false,
          data: result,
          success: function (data){result=data;}
        });
        return result;
    };

    this.getName1 = function(){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Active patients/Name1/abcd",
          async: false,
          data: result,
          success: function (data){result=data;}
        });
        return result;
    };

    this.getName2 = function(){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Active patients/Name2/abcd",
          async: false,
          data: result,
          success: function (data){result=data;}
        });
        return result;
    };


    this.getValue1 = function(){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Active patients/Value1/abcd",
          async: false,
          data: result,
          success: function (data){result=data;}
        });
        return result;
    };


    this.getValue2 = function(){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Active patients/Name2/abcd",
          async: false,
          data: result,
          success: function (data){result=data;}
        });
        return result;
    };

    this.getNameN = function(nameN){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/" + nameN,
          async: false,
          data: result,
          success: function (data){result=data;}
        });
        return result;
    };

    this.getValueN = function(valueN){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/" + valueN,
          async: false,
          data: result,
          success: function (data){result=data;}
        });
        return result;
    };

    this.getVar = function(){
        var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Var",
          async: false,
          data: result,
          success: function (data){result=data;}
        });
        return result;
    };

    this.getChart = function(){
        var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Var",
          async: false,
          data: result,
          success: function (data){result=data;}
        });
        return result;
    };
    this.getValuesRow = function(Var, Row, fingerprintID){
        var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/"+Var+"/"+Row+"/" + fingerprintID,
          async: false,
          data: result,
          success: function (data){result=data;}
        });
        return result;
    };
     this.getValuesRowWithFilters = function(Var, Row, fingerprintID, filters){
        var result = {}


        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/"+Var+"/"+Row+"/" + fingerprintID,
          async: false,
          type: "POST",
          data: filters,
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
          data: result,
          success: function (data){result=data;}
        });
        return result;
    };

};

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

            values.values.forEach(function(_value){

              var xFilter = JSON.parse(_value);

              
              self.append(xFilter.name+": ");
              var tmpUl = $('<ul class="nav nav-pills nav-stacked">');

              self.append(tmpUl);

              // This code is only for comparison mode 
              console.log(xFilter);
              if (xFilter.name == "Gender")
              {
                  xFilter.values.push("ALL");                
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
            


            /** The magic of the filters will happen here */ 
            $(".filterBar").bind('click',function(e)
                    { 
                      e.preventDefault(); 
                      e.stopPropagation();

                      console.log()

                      var charDraw = new PCDraw(actualChart, activeChart, null);

                      var str = e.target.id;
                      var filterType =str.substring(str.indexOf("_")+1,str.lastIndexOf("_"));

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
                      console.log("filterMap:");
                      console.log(filtersMap);
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
            if(e.target.innerText == 'Population Characteristics'){
              $(".graphTypes").first().click();

              $(".filterBar").first().click(); 
            }
          });

        }
    
);
