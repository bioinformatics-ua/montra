"use strict";

var Requester = (
    function( window, undefined ) {
        var instance;
        var memoizer= {};

        var __init__ = function(){

            var inCache = function(url){
                var cache = memoizer[url];
                if(cache)
                    return new Promise(function (fulfill, reject){
                        fulfill(cache);
                    });

                return undefined;
            };

            return {
                getRequest: function(url){
                    var cache = inCache(url);
                        if(cache)
                            return cache;

                    return Promise.resolve($.get(url).done(
                        function(result){
                            memoizer[url] = result;
                            return result;
                        }).fail(function(ex){
                            return ex;
                        })
                    );
                },
                postRequest: function(url, data){
                    data = data || {};

                    var cache = inCache(url+JSON.stringify(data));
                        if(cache)
                            return cache;

                    return Promise.resolve($.post(url, data).done(
                        function(result){
                            memoizer[url+JSON.stringify(data)] = result;
                            return result;
                        }).fail(function(ex){
                            return ex;
                        })
                    );
                }
            }
        }
        return {
            getInstance : function() {
                if( ! instance ) {
                    instance = new __init__();
                }
                return instance;
            }
        };
    }
)(window);

var GlobalProxy = (
    function( window, undefined ) {
        var instance;

        var __init__ = function() {
            var rq = Requester.getInstance();

            return {
                databaseSchemas : function(){
                    return rq.getRequest('/developer/api/databaseSchemas/');
                },
                getProfileInformation : function(){
                    return rq.getRequest('/developer/api/getProfileInformation/');
                },
                getFingerprints: function(schema){
                    schema = schema || '';

                    return rq.getRequest('/developer/api/getFingerprints/'+schema);
                },
                query: function(options){
                    var settings = $.extend({
                        'search': '',
                        'rows': 10,
                        'offset': 0,
                        'sort_field': 'name',
                        'sort_order': 'asc',
                        'schema': null
                    }, options);


                    return rq.postRequest('/api/searchdatabases', settings);
                },
                advancedQuery: function(query, schema){

                },
                getStore: function(){

                }
            };
        };

        return {
            getInstance : function() {
                if( ! instance ) {
                    instance = new __init__();
                }
                return instance;
            }
        };
    }
)(window);

var FingerprintProxy = (
    function( window, undefined ) {
        var instance;
        var __init__ = function() {
            return {
                getSchema: function(){

                },
                getAnswers: function(){

                },
                getStore: function(){

                }
            };
        };

        return {
            getInstance : function() {
                if( ! instance ) {
                    instance = new __init__();
                }
                return instance;
            }
        };
    }
)(window);
