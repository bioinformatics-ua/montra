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
      var pc = new PCAPI();
      $("#pcBarContent").populationChartsBar('init', pc,this.actualChart.title.fixed_title,
        fingerprintID);
      $("#pcBarContent").populationChartsBar('draw', pc);

    };
    this.draw = function(filters) {


      PC = new PCAPI();
      fingerprintID = getFingerprintID();
      
      
      var valuesFromGraph = null;
      
      if (filters!==null)
      {

        tfilter = new TransformFilter(filters);
        filters = tfilter.transform();
        valuesFromGraph = PC.getValuesRowWithFilters(this.actualChart.title.fixed_title, 
          this.actualChart.y_axis['var'],fingerprintID, filters );
      }
      var valueFilters = "";
      $.each(filters, function (data){
        var fV = filters[data];
        console.log(translations);
        console.log('do'+translations);
        if (translations.hasOwnProperty(filters[data]))
        {
          console.log('do'+filters[data]);
            fV = translations[filters[data]];
        }
        if (fV=="Total") fV = "";
        if (fV=="Male") fV = "(Male)";
        if (fV=="Female") fV = "(Female)";
        valueFilters += " " + fV;
      });
      /*valuesFromGraph = PC.getValuesRow(this.chartType, 
        'Count',fingerprintID );*/
    
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