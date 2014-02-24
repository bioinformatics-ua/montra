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
    this.draw = function(filters) {

      console.log(filters);
      PC = new PCAPI();
      fingerprintID = getFingerprintID();
      console.log('filters++');
      console.log(filters);
      
      
      var valuesFromGraph = null;
      
      if (filters!==null)
      {

        tfilter = new TransformFilter(filters);
        filters = tfilter.transform();
        valuesFromGraph = PC.getValuesRowWithFilters(this.chartType, 
          this.actualChart.y_axis.var,fingerprintID, filters );

      }
      
      /*valuesFromGraph = PC.getValuesRow(this.chartType, 
        'Count',fingerprintID );*/
    
      $("#pc_chart_place").html('');
      $("#pc_chart_place").graphicChart('init');
      $("#pc_chart_place").graphicChart('drawBarChart', valuesFromGraph,valuesFromGraph,valuesFromGraph);

      var pc = new PCAPI();
      $("#pcBarContentRoot").removeClass("hidden");
      $("#pcBarContentRoot").addClass("show");

      $("#pcBarContent").populationChartsBar('init', pc,this.chartType,
        fingerprintID);
      $("#pcBarContent").populationChartsBar('draw', pc);

      $("#pctitle").html("<h2>"+ this.chartType +"</h2>");
      if (this.e != null ) 
      {
          if ($(this.e.toElement.firstChild).hasClass('icon-ok')) 
          {
            $(this.e.toElement.firstChild).removeClass('icon-ok') 
          }
          else
          {
            $(this.e.toElement.firstChild).addClass('icon-ok') 
          }
      }
      
    };

    this.refresh = function() {

        this.draw();
    };

};