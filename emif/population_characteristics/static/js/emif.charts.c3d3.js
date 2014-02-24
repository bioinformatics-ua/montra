/**********************************************************************
# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
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



function GraphicChartC3D3(divArg, dataArg)
{
  /** Passes the initial arguments required to start and d3
  Also , this should be used to know if 
  */
  this.div = divArg; 
  this.dataValues = dataArg;
  this.xscale = null ;
  this.yscale = null ;
  this.self = this;
  this.init = function(){
    
    console.log('this in GraphicChartC3D3'  + this);
  };

  this.translateData = function(objects){
    
    console.log(objects);
    /*** Lets translate our data model to the d3 support data model */ 
    xscale = {'bins':5}
    xscale.bins = 25;
    var i = 1;
    datasetY = ['data1'];
    datasetX = ['x1'];

    objects.values.forEach(function(row){
      /*datasetX.push(parseInt(row.Value1));
      datasetY.push(parseInt(row.Count));*/
      console.log('actualChart');
      console.log(actualChart);
      if (actualChart.x_axis.categorized )
      {
        if ( row[actualChart.x_axis.var] != ""){
          datasetX.push(row[actualChart.x_axis.var]);  
          datasetY.push(parseInt(row[actualChart.y_axis.var]));  
        }
        
      }
      else
      {
        datasetX.push(parseInt(row[actualChart.x_axis.var]));
        datasetY.push(parseInt(row[actualChart.y_axis.var]));  
      }
      
      
    });
    
  };

  this.draw = function(div, dataset){
    console.log(this.div);
    console.log(datasetY.length);
    console.log(datasetX.length);
    
    var chartConfigs = {
         padding: {
        left: 100,
    },
        bindto: '#pc_chart_place',

        data: {
            xs: {
            'data1': 'x1',
            },
          columns: [
          datasetX,
           datasetY,

          ],
          types: {
            data1: 'bar',
            
          },
          
        },
        axis: {
          x: {
            type: 'categorized'
          }
        },
        zoom: {
          enabled: true,
        
        },
        
        
      };
    if (actualChart.x_axis.categorized)
    {
        var arr2 = datasetX.slice(0);
        arr2.shift();
        chartConfigs.axis.x.categories = arr2;
        chartConfigs.data.columns = [datasetY];
        chartConfigs.data.xs = {};




    }
    var chart = c3.generate(chartConfigs);
    
   }; 
};





