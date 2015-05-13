confs = {
    icon: '<i class="fa fa-smile-o"></i>',
    name: "Hello world Global App"
};
plugin = function(sdk) {
    sdk.html('Hello world');
    sdk.refresh();
};
