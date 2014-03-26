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
  this.legend = false;
  this.self = this;

  this.init = function(){
    // Just init the parameters, if it is really necessary.
  };

  this.translateData = function(objects){
    

    /*** Lets translate our data model to the d3 support data model */ 
    xscale = {'bins':5}
    xscale.bins = 25;
    var i = 1;
    legend = actualChart.legend;
    datasetY = [actualChart.title['var']];
    datasetX = ['x'];
    
    datasetYs = [];
    var i = 0;
    
    if (actualChart.y_axis.multivalue)
      {
        actualChart.y_axis['var'].forEach(function(a){
          i = i +1;
          datasetYs.push([a]);
        });
        datasetX = ['x'];
      }
    
    objects.values.forEach(function(row){
      /*datasetX.push(parseInt(row.Value1));
      datasetY.push(parseInt(row.Count));*/
      
      if (actualChart.x_axis.categorized )
      {
        if ( row[actualChart.x_axis['var']] != ""){
          datasetX.push(row[actualChart.x_axis['var']]);  
          datasetY.push(parseFloat(row[actualChart.y_axis['var']]));  
        }
        
      }
      
      else if (actualChart.y_axis.multivalue)
      {
        
        var k = 0;
        datasetX.push(row[actualChart.x_axis['var']]);  
        actualChart.y_axis['var'].forEach(function(a){
          datasetYs[k].push(parseFloat(row[a.trim()]));  
          k = k +1 ;
        });
          
      }
      else
      {
        datasetX.push(parseInt(row[actualChart.x_axis['var']]));
        datasetY.push(parseFloat(row[actualChart.y_axis['var']]));  
      }
      
      
    });
    
  };

  this.draw = function(div, dataset){
    var tmpValue = actualChart.title['var'];
    var chartConfigs = {
         padding: {
        left: 100,

    },
        bindto: '#pc_chart_place',

        data: {
          x : 'x',

            
          columns: [
          datasetX,
           datasetY,

          ],
          types: {
           // data1: 'bar',
            
          },
          
        },
        axis: {
          x: {
            //type: 'categorized',
            label_position : {},
            tick: { format: function (x) {
             // console.log(x)
              if ($.type(x) === "string")  return x; 

            return parseInt(x);
            } 
          },

          },
          y: {
            label_position : {}
            
          }
        },
        zoom: {
          enabled: true,
        
        }
        
      };
    chartConfigs.data.types[tmpValue] = 'bar';

    if (actualChart.x_axis.categorized)
    {
        var arr2 = datasetX.slice(0);
        arr2.shift();
        chartConfigs.axis.x.type = 'categorized';
        chartConfigs.axis.x.categories = arr2;
        chartConfigs.data.columns = [datasetY];
        chartConfigs.data.xs = {};
        
    }
    if (actualChart.y_axis.multivalue)
    {
      
      var arrX = datasetX.slice(0);
      var arrYs = datasetYs.slice(0);
      arrYs.push(arrX);

      chartConfigs = {
         padding: {
        left: 100,

    },
        bindto: '#pc_chart_place',

        data: {
          x : 'x',
            
          columns: 
            arrYs,
          
          
        },
        axis: {
          x: {
            label_position : {},
            tick: { format: function (x) {return parseInt(x)}
          },

          },
          y: {
            label_position : {}
            
          }
        },
        zoom: {
          enabled: true,
        
        }
        
      };
      
    }
    chartConfigs.axis.x['label'] = actualChart.x_axis['label'];
    chartConfigs.axis.y['label'] =actualChart.y_axis['label'];
    chartConfigs.axis.x['label_position']['dy'] = "3.5em";
    chartConfigs.axis.y['label_position']['dx'] = "-5.2em";
    chartConfigs.axis.y['label_position']['dy'] = "-6.5em";
    chartConfigs.axis.x['tick']['culling'] = true;
    chartConfigs.legend = {}
    chartConfigs.legend['show'] = legend;
    
    
    try{var chart = c3.generate(chartConfigs);}
    catch(ex)
    {
      // Handle the shit here!
    }
   }; 
};





