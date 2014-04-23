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
        
      
      
      $("#pcBarContent").populationChartsBar('init', pc,this.actualChart.title.fixed_title,
        fingerprintID);
      $("#pcBarContent").populationChartsBar('draw', pc);

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
          this.actualChart.y_axis['var'],fingerprintID, filters );
      }
      if (PAGE_TYPE==PC_COMPARE)
      {
          delete filters['fingerprint_ids'];
      }
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
        valueFilters += " " + fV;
      });
      
    
      $("#pc_chart_place").html('');
      $("#pc_chart_place").graphicChart('init');
      $("#pc_chart_place").graphicChart('drawBarChart', valuesFromGraph,valuesFromGraph,valuesFromGraph);

      
      $("#pcBarContentRoot").removeClass("hidden");
      $("#pcBarContentRoot").addClass("show");

      
      

      $("#pctitle").html("<h2>"+ this.actualChart.title.fixed_title + valueFilters +"</h2>");
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