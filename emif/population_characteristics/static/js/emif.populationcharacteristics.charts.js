// Load the configurations 

/***
* This configuration will say what type of charts the tool will draw
* 
*/

function PCConfs () 
{
    this.getSettings = function(fingerprintId){
          var result = {}
          
        $.ajax({
          dataType: "json",
          url: "population/settings/+"+fingerprintId+"+/",
          async: false,
          data: result,
          success: function (data){result=data;},
        });
        return JSON.parse(result.conf).charts;
        
    };
};

function ChartLayout () 
{
    var configs = null
    this.getChartTitles = function(fingerprintId){
        var configs = new PCConfs();
        var charts = configs.getSettings();
        var charts_titles = []
        charts.forEach(function(a){
            console.log(a)
            charts_titles.push(a.title.var)
        });
        return charts_titles;
    };



};



