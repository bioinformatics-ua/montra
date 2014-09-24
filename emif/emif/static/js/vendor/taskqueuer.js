/**********************************************************************
# Copyright (C) 2014 Luís A. Bastião Silva and Eriksson Monteiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
           Eriksson Monteiro <eriksson.monteiro@ua.pt>
#

The MIT License (MIT)


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
#
/*********************************************************************/



/********************************************************************
****** TaskQueuer ***************************************************
*********************************************************************/
/**
* The idea of this class is to create a task queuer to management many
* tasks
*
* @class TaskQueuer
* @constructor
* @param {Integer} size It contains the number of tasks that will execute 
* at the same time
* @param {Integer} timeout It contains the timeout that the queue is waiting 
* to get more tasks from the queue. 600 is the default timeout.
*/
function TaskQueuer(size, timeout, onAbort) {
    var TIMEOUT = 600; 
    this.poolSize = size;
    this.pool = [];
    this.die = false;
    this.onDie = null;
    this.__abort = false;
    this.onAbort = null;
    this.running_pool = [];

    if (timeout === undefined)
    {
        timeout = TIMEOUT; 
    };
    if(onAbort !== undefined && typeof(onAbort) == "function"){
        this.onAbort = onAbort;
    }
    this.timeout = timeout;
    this._init();
};

TaskQueuer.prototype = { 

    /**
    * This methods puts a task in task queuer to run.
    *
    * @method run
    * @param {Runnable} runnable This is a Runnable object which contains the link
    * to the function and also the priority
    */

    run : function(runnable) {
        this.pool.push(runnable);

    },


    /**
    * This methods contains the loop to start the TaskQueuer. 
    * Note: it is a private method
    * @method _init
    */
    _init : function(){
        var self =  this; // This is very nice advise by Eriksson Monteiro! :D 
        this.poolHandler = setInterval(function() {
            if ( self.__abort === true)
            {
                clearInterval(self.poolHandler) // this code remmember me Python.

                // If any onAbort defined
                if(self.onAbort != null)
                    self.onAbort();

                return; 
            }
            if ( self.pool.length == 0 && self.die)
            {
                clearInterval(self.poolHandler) // this code remmember me Python.

                // If any onDie defined
                if(self.onDie != null)
                    self.onDie();

                return; 
            }

            for(var i = 0; i < self.running_pool.length; i++){
                if(self.running_pool[i].isCompleted()===true){
                    self.running_pool.splice(i, 1);
                }
            }

            if(self.running_pool.length >= self.poolSize){
                return;
            }

            self.pool = self.pool.sort(function (x, y) {
                return x.priority - y.priority;
            } );

            var items_count = self.poolSize - self.running_pool.length;
            for (var i = 0; i < items_count && i < self.pool.length ; i++){
                var r = self.pool.shift();
                self.running_pool.push(r);
                r.run();
            }
            

        }, this.timeout);
    },
    destroy : function(cb) {
        this.onDie = cb;
        this.die = true;
    },
    abort   : function() {
        this.__abort=true;
    }
};


/********************************************************************
****** Runnable *****************************************************
*********************************************************************/
/**
* This class accept the task to run. 
* This contains the function and priority. For instance, if the priority is 
* bigger than the others in the queue, the task will be executed firstly.
*
* @class Runnable
* @constructor
* @param fRun {function} the function to run the task
* @param priority {Integer} priority of this task. 1 is the default priority
*/

function Runnable(fRun, priority ){
    
    if (priority===undefined)
    {
        priority = 1; 
    }
    this.args = Array.prototype.slice.call(arguments,2);
    


    this.priority = priority;
    this.fRun = fRun;
    this.completed = false; 
}


Runnable.prototype = { 
    /**
    * This methods should be called when the task is completed. 
    *
    * @method complete
    */

    complete : function() {
        this.completed = true;
    },
    /**
    * This methods returns if the task is already complete or not. 
    *
    * @method isCompleted
    * @return {Boolean} returns if the task is completed or not.
    */

    isCompleted : function() {
        return this.completed;
    },
    /**
    * Change priority to this task.
    *
    * @method setPriority
    * @param {Integer} priority Change the priority of then task
    */

    setPriority : function(priority) {
        this.priority = priority;
    },
    /**
    * This methods runs the task. Call the function fRun with the passed arguments. 
    *
    * @method run
    */
    run : function(){
        this.fRun.apply(this, this.args);
    }
};
