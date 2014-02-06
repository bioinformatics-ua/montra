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


function PCAPI () 
{
    this.getGender = function(){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Gender",
          async: false,
          data: result,
          success: function (data){result=data;},
        });
        return result;
    };

    this.getName1 = function(){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Name1",
          async: false,
          data: result,
          success: function (data){result=data;},
        });
        return result;
    };

    this.getName2 = function(){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Name2",
          async: false,
          data: result,
          success: function (data){result=data;},
        });
        return result;
    };


    this.getValue1 = function(){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Value1",
          async: false,
          data: result,
          success: function (data){result=data;},
        });
        return result;
    };


    this.getValue2 = function(){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/jerboalistvalues/Value2",
          async: false,
          data: result,
          success: function (data){result=data;},
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
          success: function (data){result=data;},
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
          success: function (data){result=data;},
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
          success: function (data){result=data;},
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
          success: function (data){result=data;},
        });
        return result;
    };

};

/********************************************************************
**************** Population Characteristics - Bar (Jquery Plugin) 
*********************************************************************/

 (function( $ )
 {

    var methods = {
        init : function( options ) {

            
            values = options.getGender();
            console.log("Gender values");
            console.log(values);
            if (values===undefined)
            {
                return;
            };
            var self = this;
            self.append("Gender: ");
            var tmpUl = $('<ul class="nav nav-pills nav-stacked">');

            self.append(tmpUl);
            $.each(values.values, function (data){
                if (values.values[data]==="")
                    return;
                tmpUl.append('<li><a class="filterBar" href="#" onclick="return false;"><i id="iproximity" class="icon-ok icon-black active"></i> '+values.values[data]+'</a></li>')
            });
            
            self.append("Name1: ");
            tmpUl = $('<ul class="nav nav-pills nav-stacked">');
            values = options.getName1();
            self.append(tmpUl);
            $.each(values.values, function (data){
                if (values.values[data]==="")
                    return;
                
                tmpUl.append('<li> <a  class="filterBar" href="#" onclick="return false;"><i id="iproximity" class="icon-ok icon-black active"></i> '+values.values[data]+'</a></li>')
            });
            

            self.append("Name2:");
            tmpUl = $('<ul class="nav nav-pills nav-stacked">');
            values = options.getName2();
            self.append(tmpUl);
            $.each(values.values, function (data){
                if (values.values[data]==="")
                    return;
                
                tmpUl.append('<li><a class="filterBar" href="#" onclick="return false;"><i id="iproximity" class="icon-ok icon-black active"></i> '+values.values[data]+'</a></li>')
            });
            
            $(".filterBar").bind('click',function(e)
                    { 
                      e.preventDefault(); 
                      e.stopPropagation();
                      
                      
                      if ($(e.toElement.firstChild).hasClass('icon-ok')) 
                      {
                        $(e.toElement.firstChild).removeClass('icon-ok') 
                      }
                      else
                      {
                        $(e.toElement.firstChild).addClass('icon-ok') 
                      }
                      return false;
                    });

            var match=false;

        },
        draw : function( options ) {
            
        },

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

    var methods = {
        init : function( options ) {

            
            var self = this;
            self.append("Var: ");
            tmpUl = $('<ul class="nav nav-pills nav-stacked">');
            values = options.getVar();
            self.append(tmpUl);
            $.each(values.values, function (data){
                if (values.values[data]==="")
                    return;
                
                tmpUl.append('<li><a class="filterBar" href="#" onclick="return false;"><i id="iproximity" class="icon-ok icon-black active"></i> '+values.values[data]+'</a></li>')
            });

            var myPC = options;

            $(".filterBar").bind('click',function(e)
                    { 
                      e.preventDefault(); 
                      e.stopPropagation();
                      
                      console.log(myPC);
                      if ($(e.toElement.firstChild).hasClass('icon-ok')) 
                      {
                        $(e.toElement.firstChild).removeClass('icon-ok') 
                      }
                      else
                      {
                        $(e.toElement.firstChild).addClass('icon-ok') 
                      }
                      return false;
                    });
        },
        draw : function( options ) {
            
        },

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

        var pc = new PCAPI();

        $("#pcBarContent").populationChartsBar(pc);
        $("#pcBarContent").populationChartsBar('draw', pc); 


        $("#pc_list").populationChartsTypes(pc);
        $("#pc_list").populationChartsTypes('draw', pc); 

    }
);

