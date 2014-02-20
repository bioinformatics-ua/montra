
    function exampleData() {
      return  [ 
         {
           key: "Cumulative Return",
           values: [
             { 
               "label" : "2000" ,
               "value" : 30000,
               "color" : "#0000ff",
             } , 
             { 
               "label" : "2001" , 
               "value" : 35000,
               "color" : "#0000ff",
             } , 
             { 
               "label" : "2002" , 
               "value" : 25000,
               "color" : "#0000ff",
             } , 
             { 
               "label" : "2003" , 
               "value" : 29000,
               "color" : "#0000ff",
             } , 
             { 
               "label" : "2004" ,
               "value" : 31000,
               "color" : "#0000ff",
             } , 
             { 
               "label" : "2005" , 
               "value" : 35000,
               "color" : "#0000ff",
             } , 
             { 
               "label" : "2006" , 
               "value" : 40000,
               "color" : "#0000ff",
             } , 
             { 
               "label" : "2007" , 
               "value" : 60000,
               "color" : "#0000ff",

             }
           ]
         }
       ];
     };




function GraphicChartD3(divArg, dataArg)
{
  /** Passes the initial arguments required to start and d3
  Also , this should be used to know if 
  */
  var div = divArg; 
  var dataValues = dataArg;
  var self = this;
  this.init = function(){
    
    console.log('this in GraphCharD3'  + this);
  };

  this.translate_data = function(objects){
    

    /*** Lets translate our data model to the d3 support data model */ 


  };

  this.draw = function(div, dataset){
     nv.addGraph(function() {
               var chart = nv.models.discreteBarChart()
                   .x(function(d) { return d.label })
                   .y(function(d) { return d.value })
                   .staggerLabels(false)
                   .tooltips(true)
                   .showValues(true)
             
               d3.select('#chart svg')
                   .datum(exampleData())
                 .transition().duration(500)
                   .call(chart);
             
               nv.utils.windowResize(chart.update);
             
               return chart;
             });
             
            $("#chart h1").append("Number of patients yearly")
      

   }; 
};





