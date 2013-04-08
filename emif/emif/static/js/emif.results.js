


/* Search function - consume web services */ 

EMIF.Search = Backbone.Router.extend({
    routes: {
        "/quicksearch": "quicksearch",
        "/": "listProducts"
    },
    //initialize: function (options) {},
    quicksearch: function () {
        var productsList = new PX.ProductListView({
            "container": $('#container'),
            "collection": PX.products
        });
        PX.products.deferred.done(function () {
            productsList.render();
        });
    }

    quicksearch: function () {
        var productsList = new PX.ProductListView({
            "container": $('#container'),
            "collection": PX.products
        });
        PX.products.deferred.done(function () {
            productsList.render();
        });
    }


});