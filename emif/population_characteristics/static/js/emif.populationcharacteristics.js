/**********************************************************************
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


  if (url.indexOf("compare")==-1)
  {
    try{
      revision = global_revision;
    }
    catch(err){
      console.error('Error retrieving revision from pop.char.');
    };
  }
  return revision;

};

var filtersMap = {};
var translations = {};
var translationsBack = {};
var activeChart='';

var actualChart = null;

var cache_json = {};
var hashCode = function(s){
  return s.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);
}
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


        var destiny = this.endpoint+"/"+Var+"/"+Row+"/" + fingerprintID+"/"+revision;
        var key = hashCode(destiny);
         if(cache_json.hasOwnProperty(key)){
          result = cache_json[key];


         } else {
            $.ajax({
              dataType: "json",
              url: destiny,

              async: false,
              type: "POST",
              data: { publickey: global_public_key, result: result },
              success: function (data){result=data;}
            });

            cache_json[key] = result;
          }

            return result;
    };
     this.getValuesRowWithFilters = function(Var, Row, fingerprintID, revision, filters){
        var result = {}
        var destiny = this.endpoint+"/"+Var+"/"+Row+"/" + fingerprintID + "/" + revision;

        var key = hashCode(destiny + JSON.stringify(filters));

         if(cache_json.hasOwnProperty(key)){
          result = cache_json[key];

         } else {
            $.ajax({
              dataType: "json",
              url: destiny,
              async: false,
              type: "POST",
              data: { publickey: global_public_key, filters: filters },
              success: function (data){
                result=data;
              }
            });

            cache_json[key] = result;
         }



          return result;
    };

    this.getFilter = function(Var, fingerprintID){
        var result = {};
        var destiny = "population/filters/"+Var+"/" + fingerprintID;

        var key = hashCode(destiny);

         if(cache_json.hasOwnProperty(key)){
          result = cache_json[key];

         } else {
        $.ajax({
          dataType: "json",
          url: "population/filters/"+Var+"/" + fingerprintID,
          async: false,
          type: "POST",
          data: { publickey: global_public_key, result: result },
          success: function (data){result=data;}
        });

        cache_json[key] = result;
      }
        return result;
    };

};

/********************************************************************
**************** Population Characteristics - Bar (Jquery Plugin) v2 (using dyndropdown)
*********************************************************************/
var stuff;
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
            var default_options = {};

            values.values.forEach(function(_value){

              var xFilter = JSON.parse(_value);

              filters_tmp.push(xFilter);
              if (!xFilter.show)
                return;

              self.append(xFilter.name+": ");
              var options = [];

              //var tmpUl = $('<ul class="nav nav-pills nav-stacked">');

              //self.append(tmpUl);

              // This code is only for comparison mode
              //console.log(xFilter);
              if (xFilter.name == "Gender")
              {
                  if (xFilter.translation.hasOwnProperty("ALL"))
                  {
                    xFilter.values.push("ALL");
                    //options.push({'ALL': 'ALL'});
                  }

              }

              xFilter.values.sort();
              xFilter.values.reverse();

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
                  options.push({'key': xFilter.values[data], 'value': originalValue});

                  // if('ALL' in default_option[xFilter.values[data]]){

                  // }

              });
              JSON_OUTPUT[xFilter.value] = {values: options, name: xFilter.name};
              if($.inArray( 'ALL', xFilter.values ) != -1){
                default_options[xFilter.value] = 'ALL';
              } else if($.inArray( 'T', xFilter.values ) != -1){
                default_options[xFilter.value] = 'T';
              }
            });
            //console.log('JSON_OUTPUT');
            //console.log(JSON.stringify(JSON_OUTPUT));


            filter_dropdown = $(this).dyndropdown({
                    label: "Filter",
                    dropup: false,
                    alwaysOneOption: true,
                    defaultOptions: default_options,
                    onSelectionChanged: function(selection){

                        var charDraw = new PCDraw(actualChart, activeChart, null);
                        $.each(selection, function(filter, options){
                          var options_translated = [];

                          $.each(options, function(index, value){
                            options_translated.push(value);
                          });

                          filtersMap['values.'+filter] = options_translated;

                        });
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

                      var this_title = e.target.innerHTML;

                      chartTypes.forEach(function(a){


                          if (a.title.fixed_title== this_title)

                          {
                              actualChart = a;
                          }

                      });


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

                      //var filterbar = $(".filterBar");
                      //filterbar.last().click();
                      //filterbar.first().click();


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

                var tooltip = "";
                if(values[data].tooltip != null)
                  tooltip = 'title="'+values[data].tooltip+'"';
                tmpUl.append('<li '+tooltip+' class="graphLine"><a class="graphTypes" href="#" onclick="return false;">'+values[data].title+'</a></li>')
            });

            var myPC = options;

            filters = new Filters();
            filters.bindFilters();

        },
        draw : function( options ) {
          $('.graphLine').tooltip({'container': 'body'});
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

function generatePng(){
       // Zoom! Enhance!
       // $('#chart > svg').attr('transform', 'scale(2)');

       // Copy CSS styles to Canvas

       // Remove all defs, which botch PNG output
       //$('defs', $('#pc_chart_place')).remove();

       inlineAllStyles($('#pc_chart_place'));
       // Create PNG image
       var canvas = $('.preview-pane').empty()[0];
       canvas.width = $('#pc_chart_place').width()*1.8;
       canvas.height = $('#pc_chart_place').height()*1.8;

       var canvasContext = canvas.getContext('2d');
       var svg = $.trim($('#pc_chart_place svg').prop('outerHTML'));
       canvasContext.drawSvg(svg, 0, 0,canvas.width, canvas.height);
       $("#downloadpng").attr("href", canvas.toDataURL("png"))
           .attr("download", function() {
               return db_name + " - " +$('#pctitle').text();
        });
}
function generateSvg(){
       inlineAllStyles($('#pc_chart_place'));

       var svg = $.trim($('#pc_chart_place svg').prop('outerHTML'));

       var data = new Blob([svg], {type: 'image/svg+xml'});

       var svgfile = window.URL.createObjectURL(data);

       $("#downloadsvg").attr("href", svgfile)
           .attr("download", function() {
               return db_name + " - " +$('#pctitle').text()+'.svg';
        });
}
function generatePdf(){
  generatePng();

  var doc = new jsPDF('l', 'pt', 'a4');
  var canvas = $('.preview-pane');
  doc.setFontSize(20);
  doc.text(35, 65, db_name + " - " +$('#pctitle').text());
  doc.addImage($("#downloadpng").attr('href'), 'png', 15, 90, 750, 376);

  doc.save(db_name + " - " +$('#pctitle').text()+'.pdf');
}
var styles;
   var inlineAllStyles = function(context) {
       var chartStyle, selector;
       // Get rules from c3.css
       for (var i = 0; i <= document.styleSheets.length - 1; i++) {
           if (document.styleSheets[i].href && document.styleSheets[i].href.indexOf('c3.css') !== -1) {
               if (document.styleSheets[i].rules !== undefined) {
                   chartStyle = document.styleSheets[i].rules;
               } else {
                   chartStyle = document.styleSheets[i].cssRules;
               }
           }

       }
       if (chartStyle !== null && chartStyle !== undefined) {
           // SVG doesn't use CSS visibility and opacity is an attribute, not a style property. Change hidden stuff to "display: none"
           var changeToDisplay = function() {
               if ($(this).css('visibility') === 'hidden' || $(this).css('opacity') === '0') {
                   $(this).css('display', 'none');
               }
           };
           // Inline apply all the CSS rules as inline
           for (i = 0; i < chartStyle.length; i++) {

               if (chartStyle[i].type === 1) {
                   selector = chartStyle[i].selectorText;
                   styles = makeStyleObject(chartStyle[i]);
                   $('svg *').each(changeToDisplay);
                   // $(selector).hide();
                   $(selector).not($('.c3-chart path')).css(styles);
               }
               $('.c3-chart path')
                   .filter(function() {
                       return $(this).css('fill') === 'none';
                   })
                   .attr('fill', 'none');

               $('.c3-chart path')
                   .filter(function() {
                       return !$(this).css('fill') === 'none';
                   })
                   .attr('fill', function() {
                       return $(this).css('fill');
                   });
           }
       }
   };
   // Create an object containing all the CSS styles.
   // TODO move into inlineAllStyles
   var makeStyleObject = function(rule) {
       var styleDec = rule.style;
       var output = {};
       var s;
       for (s = 0; s < styleDec.length; s++) {
           output[styleDec[s]] = styleDec[styleDec[s]];
       }
       return output;
   };
