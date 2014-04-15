/*
 * This widget, marks up patterns, in a plugin-defined manner

 * Author: Ricardo Ribeiro <ribeiro.r@ua.pt> 
 */

var PatternRecognizer = function(pattern, target){
    this.pattern = pattern;
    this.target = target;
    this.matches = [];
}.addToPrototype({
    "match": function(){
        var self = this;

        self.matches = [];

        $(self.target).filter(function() {
            var result = $(this).html().match(self.pattern);
            return result;
        }).each(function() {
            //$(this).html($(this).html().replace(this.pattern, "<a href=\"mailto:$1\">$1</a>"));
            self.matches.push(this);
        });
        //console.log('-- Match '+ self.pattern + ' into '+self.target+', found '+ this.matches.length +' matches.');

        return this.matches.length;
    },
    "applyMasks": function(){
        //console.log('-- Applying masks');

        for(var i=0;i<this.matches.length;i++){
            this.mask(this.matches[i]);
        }
    },
    "mask": function(element){
        console.error('This is an abstract method, the method \'mask\' must be overriden.');
    }
});

/* Plugin for email recognizing */ 
var EmailRecognizer = function(target){
    EmailRecognizer._base.apply(this, [/([\w-.]+@[\w.]+)/g, target]);
}.inherit(PatternRecognizer).addToPrototype({
    // override mask
    "mask": function(element){
        $(element).html($(element).html().replace(this.pattern, "<a href=\"mailto:$1\">$1</a>"));
    }
});
/* Plugin for link recognizing */ 
var LinkRecognizer = function(target){
    LinkRecognizer._base.apply(this, [/(http:\/\/[\w.\/]+)/g, target]);
}.inherit(PatternRecognizer).addToPrototype({
    // override mask
    "mask": function(element){
        $(element).html($(element).html().replace(this.pattern, "<a href=\"$1\">$1</a>"));
    }
});
