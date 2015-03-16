"use strict";



var GlobalProxy = (
    function( window, undefined ) {
        var instance;
        var memoizer= {};
        var __init__ = function() {

            var inCache = function(url){
                var cache = memoizer[url];
                if(cache)
                    return new Promise(function (fulfill, reject){
                        fulfill(cache);
                    });

                return undefined;
            };

            var getRequest = function(url){
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
            }

            return {
                databaseSchemas : function(){
                    return getRequest('/developer/api/databaseSchemas/');
                },
                getProfileInformation : function(){
                    return getRequest('/developer/api/getProfileInformation/');
                },
                getFingerprints: function(schema){
                    schema = schema || '';

                    return getRequest('/developer/api/getFingerprints/'+schema);
                },
                query: function(query, schema){

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
