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

function PCDraw(chartType)
{
    this.chartType=chartType;
    this.draw = function(filters) {

      console.log(filters);
      PC = new PCAPI();
      fingerprintID = getFingerprintID();
      console.log(fingerprintID);
      var valuesFromGraph = PC.getValuesRow(this.chartType, 
        'Count',fingerprintID );
      console.log('valuesFromGraph: '+this.chartType);
      console.log(valuesFromGraph);
      $("#pc_chart_place").html('');
      $("#pc_chart_place").graphicChart('init');
      $("#pc_chart_place").graphicChart('drawBarChart', valuesFromGraph,valuesFromGraph,valuesFromGraph);

      console.log('Debug vars');

      var pc = new PCAPI();
      $("#pcBarContentRoot").removeClass("hidden");
      $("#pcBarContentRoot").addClass("show");

      $("#pcBarContent").populationChartsBar('init', pc,e.toElement.innerHTML,
        fingerprintID);
      $("#pcBarContent").populationChartsBar('draw', pc);

      $("#pctitle").html("<h2>"+ e.toElement.innerHTML +"</h2>");
      
      if ($(e.toElement.firstChild).hasClass('icon-ok')) 
      {
        $(e.toElement.firstChild).removeClass('icon-ok') 
      }
      else
      {
        $(e.toElement.firstChild).addClass('icon-ok') 
      }

      
    };

    this.refresh = function() {

        this.draw();
    };

};