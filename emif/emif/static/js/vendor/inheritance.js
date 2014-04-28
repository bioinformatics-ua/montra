/*
 * Author: Ricardo Ribeiro <ribeiro.r@ua.pt> 
 */
/* The ways of assuring inheritance, is heavily documented 
 * on the book "Javascript" by Luis Abreu from MyTi publisher.
 * 
 * That is the main inspiration for this approach, so i can't take full credit.
 * I did decide to extend on the concept and allow the definition of several 
 * methods to add to the prototype, instead of just one */

if(typeof Function.prototype.inherit !== 'function') {
    Function.prototype.inherit = function(parentFn) {

        if(typeof parentFn === 'function'){
             // field _base keeps ref for parent function
             this._base = parentFn;
             // get prototype from base and add to this one
             this.prototype = new parentFn();

             // reset prototype constr. (above we replaced it by the parent one, must point to this function)
             this.prototype.constructor = this;

             // field _super keeps ref for parent object (object !== function)
             this._super = parentFn.prototype;

             return this;

        }
        else {
            console.error('Tried to create inheritance from something that is not a function.');
            return null;
        }

    }
}
/* This allows to add a dictionary of methods to prototype, without removing the ones already there, 
 * just incrementing, useful for inheritance */
if(typeof Function.prototype.addToPrototype !== 'function') {
    Function.prototype.addToPrototype = function(dict) {
        for(entry in dict){                       
            this.prototype[entry] = dict[entry];   
        }
        
        return this;
    }   
}