confs = {
    name: "My Chart",
    extracss: ["//cdn.jsdelivr.net/chartist.js/latest/chartist.min.css"],
    extralibs: ["//cdn.jsdelivr.net/chartist.js/latest/chartist.min.js"]
};
plugin = function(sdk){
    sdk.html('Loading chart...');
    sdk.refresh();
    var context = sdk.container();

    // Simulating getting data from somewhere (could be from proxies)
    setTimeout(function(){
        sdk.html('<div class="ct-chart ct-golden-section" id="chart1"></div>');
        sdk.refresh();
        var data = {
            // A labels array that can contain any sort of values
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            // Our series array that contains series objects or in this case series data arrays
            series: [
              [5, 2, 4, 2, 0]
            ]
        };
        new Chartist.Line('.ct-chart', data);
    }, 2000);
};
