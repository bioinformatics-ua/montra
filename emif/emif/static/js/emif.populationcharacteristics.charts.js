


function Title()
{


}


function Axis()
{

    
}

function MyClass(){
    this._attr = "foo";
    this.getAttr = function(){
        return this._attr;
    }
}
MyClass.prototype.toJSON() {
    return {attr: this.getAttr()}; // everything that needs to get stored
};
MyClass.fromJSON = function(obj) {
    if (typeof obj == "string") obj = JSON.parse(obj);
    var instance = new MyClass;
    instance._attr = obj.attr;
    return instance;
};