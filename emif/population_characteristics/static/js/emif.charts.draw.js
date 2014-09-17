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

function PCDraw(actualChart,chartType, e)
{
  this.actualChart = actualChart;
    this.chartType=chartType;
    this.e = e;
    this.drawBar = function() {
      if (PAGE_TYPE==PC_NORMAL)
      {
        var pc = new PCAPI(null);
      }
      else if (PAGE_TYPE==PC_COMPARE)
      {
        var pc = new PCAPI("population/compare/values");
      }
        
      
      
      $("#pcBarContent").populationChartsBar2('init', pc,this.actualChart.title.fixed_title,
        fingerprintID);

      $("#pcBarContent").populationChartsBar2('draw', pc);


    };
    this.draw = function(filters) {


      if (PAGE_TYPE==PC_NORMAL)
      {
        var PC = new PCAPI(null);
      }
      else if (PAGE_TYPE==PC_COMPARE)
      {
        var PC = new PCAPI("population/compare/values");
      }

      
      fingerprintID = getFingerprintID();
      revision = getRevision();
      
      
      var valuesFromGraph = null;
      
      if (filters!==null)
      {

        tfilter = new TransformFilter(filters);
        filters = tfilter.transform();
        
        if (PAGE_TYPE==PC_COMPARE)
        {
          
          
          filters['fingerprint_ids'] = $("#fingerprints_store").text();  
          
          
        }
        valuesFromGraph = PC.getValuesRowWithFilters(this.actualChart.title.fixed_title, 
          this.actualChart.y_axis['var'],fingerprintID, revision, filters );
      }
      if (PAGE_TYPE==PC_COMPARE)
      {
          delete filters['fingerprint_ids'];
      }
      var valuefilt;
      var gender_values;
      var handleFilters = function(filters){
        var valueFilters = "";

        $.each(filters, function (data){
          var fV = filters[data];
          
          if (translations.hasOwnProperty(filters[data]))
          {
            
              fV = translations[filters[data]];
          }
          if (fV=="Total") fV = "";
          if (fV=="Male") fV = "(Male)";
          if (fV=="Female") fV = "(Female)";
          if (fV.indexOf('M') >= 0 &&  fV.indexOf('F') >= 0 && fV.indexOf('T') >= 0) //convert M/F/T to Male/Female
          {
            fV = translations["ALL"];
          }
          valueFilters += " " + fV;
        });

        return valueFilters;
      };
        // gender always comes last as per specification
        if( filters != undefined && 'values.Value1' in filters){
          gender_values = {'filters.values.Gender': filters['values.Gender']};
          delete filters['values.Gender'];
        }
        valuefilt = handleFilters(filters);

        if(gender_values != undefined){
          valuefilt += handleFilters(gender_values);
        }      
    
      $("#pc_chart_place").html('');
      $("#pc_chart_place").graphicChart('init');
      $("#pc_chart_place").graphicChart('drawBarChart', valuesFromGraph,valuesFromGraph,valuesFromGraph);

      
      $("#pcBarContentRoot").removeClass("hidden");
      $("#pcBarContentRoot").addClass("show");

      
      

      $("#pctitle").html("<h2>"+ this.actualChart.title.fixed_title + valuefilt +"</h2>");
      if(this.actualChart.hint != undefined)
        $("#pchint").html("<center><h4>"+ this.actualChart.hint +"</h4></center>");
      else
        $("#pchint").html("<center><h4></h4></center>");
      if (this.e != null ) 
      {
          if ($(this.e.target.firstChild).hasClass('icon-ok')) 
          {
            $(this.e.target.firstChild).removeClass('icon-ok') 
          }
          else
          {
            $(this.e.target.firstChild).addClass('icon-ok') 
          }
      }
      
    };

    this.refresh = function(filters) {
        
        this.draw(filters);
    };

};