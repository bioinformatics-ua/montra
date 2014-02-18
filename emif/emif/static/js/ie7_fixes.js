// no console command on ie 7/8/9
if (typeof console == "undefined") {
    this.console = {log: function() {}, warn: function(){}, error: function(){}};
}

// ie 8 and 7 never heard of trimming apparently...
if(typeof String.prototype.trim !== 'function') {
  String.prototype.trim = function() {
    return this.replace(/^\s+|\s+$/g, ''); 
  }
}