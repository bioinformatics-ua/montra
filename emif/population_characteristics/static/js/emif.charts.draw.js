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
          filters['fingerprint_ids'] = fingerprint_store;
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
          else if (fV=="Male") fV = "(Male)";
          else if (fV=="Female") fV = "(Female)";
          else if (fV.indexOf('M') >= 0 &&  fV.indexOf('F') >= 0 && fV.indexOf('T') >= 0) //convert M/F/T to Male/Female
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

      var pc_chart_place = $("#pc_chart_place");
      pc_chart_place.html('');
      pc_chart_place.graphicChart('init');
      pc_chart_place.graphicChart('drawBarChart', valuesFromGraph,valuesFromGraph,valuesFromGraph);


      var pcBarContentRoot = $("#pcBarContentRoot");

      pcBarContentRoot.removeClass("hidden");
      pcBarContentRoot.addClass("show");


      var actual_chart = this.actualChart;

      $("#pctitle").html("<h2>"+ actual_chart.title.fixed_title + valuefilt +"</h2>");
      if(actual_chart.hint != undefined)
        $("#pchint").html("<center><h4>"+ actual_chart.hint +"</h4></center>");
      else
        $("#pchint").html("<center><h4></h4></center>");

      $('#pc_tabular_place').trigger('refresh_tabular');

      if (this.e != null )
      {
          var firstChild = $(this.e.target.firstChild);

          if (firstChild.hasClass('icon-ok'))
          {
            firstChild.removeClass('icon-ok')
          }
          else
          {
            firstChild.addClass('icon-ok')
          }
      }

    };

    this.refresh = function(filters) {

        this.draw(filters);
    };

};
