/**********************************************************************
# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
***********************************************************************/


/** This counters was added here by:
 * Bastiao, Feb 26, 2014
 *
 * The structure will be a dictionary with number of total questions and number of filled questions.
 * In modern browsers:  questionSets[qId].count and questionSets[qId].filledQuestions
 */
var questionSetsCounters = {};


/**
* Responsabible to keep the counting of each filled questions versus numbe 
* of total questions
*
* @class CounterCore
* @constructor
* @param {Integer} questionnaireId The id of the questionnaire type. 
  It matches with the primary key of the template. - Not mandatory
*/
function CounterCore(questionnaireId) {
    this.questionnaireId = questionnaireId;

    /**
     * This method counts the number of total questions of a question set
     *
     * @method countQuestionSet
     * @param {Integer} qId Identifier of Question Set (sort to keep the order )
     * @return {Integer} Returns the number of questions that the question set have.
     */
    this.countQuestionSet = function(qId) {
        var counter = 0;
        // Go for each question set and counts the questions 
        $('#qs_' + qId + ' .question').each(function(question) {
            counter = counter + 1;

        });
        return counter;
    };

    /**
    * This method counts the number of filled questions of a question set
    * It should be only used in the edit/or view, whatever.
    *
    * @method countFilledQuestionSet
    * @param {Integer} qId Identifier of Question Set (sort to keep the order )
    * @return {Integer} Returns the number of questions that are filled 
      in the question set.
    */
    this.countFilledQuestionSet = function(qId) {
        var counter = 0;
        // Go for each question set and counts the questions 
        $('#qs_' + qId + ' .hasValue').each(function(question) {

            counter = counter + 1;
        });

        return counter;

    };


    /**
     * This methods fill the global array to count all questions/filled.
     *
     * @method countFilledQuestionSet
     * @param {Integer} qId Identifier of Question Set (sort to keep the order )
     */
    this.fullCount = function(qId) {
        var filled = this.countFilledQuestionSet(qId);
        var all = this.countQuestionSet(qId);
        questionSetsCounters[qId] = {
            filledQuestions: filled,
            count: all
        };
        return questionSetsCounters[qId];

    };
};


/**
* Calls the tasks for all qsets
*
* @class CounterUI
* @constructor
* @param {Integer} questionnaireId The id of the questionnaire type. 
  It matches with the primary key of the template.
*/
function CounterUI() {

    this.handlers = [];


    /**
     * This class update the counts in the graphical interface
     *
     * @method updateCounters
     * @param {Integer} qId Identifier of Question Set (sort to keep the order )
     * @param {Dictionary} counters dicionary with the values filledQuestions and count.
     */
    this.updateCounters = function(qId, counters) {
        var filled = counters['filledQuestions'];
        var total = counters['count'];

        var percentage = Math.round((filled / total) * 100);

        $('#qs_' + qId + ' .questionset-title label').html(filled + ' of ' + total + ' - ' + percentage + '%');

        var this_label0 = $('#counter0_' + qId);
        var this_label1 = $('#counter1_' + qId);

        this_label0.html("&nbsp;(" + filled + "/" + total + ")");
        this_label0.removeClass('hidden');
        this_label1.html(percentage + '%');
        this_label1.removeClass('hidden');
    };


    /**
     * This class update the counts in the graphical interface
     *
     * @method updateCounters
     * @param {Integer} qId Identifier of Question Set (sort to keep the order )
     * @param {Dictionary} counters dicionary with the values filledQuestions and count.
     */
    this.updateCountersClean = function(qId) {
        console.log(qId);
        this.updateCounters(qId, questionSetsCounters[qId]);
    };




};


/**
* Calls the tasks for all qsets
*
* @class CounterTasker
* @constructor
* @param {CounterUI} ui The wrapper to update the UI.
* @param {Integer} questionnaireId The id of the questionnaire type. 
  It matches with the primary key of the template. Not mandatory
*/
function CounterTasker(ui, questionnaireId) {

    this.POLL_MAX = 20;
    this.questionnaireId = questionnaireId;
    this.ui = ui;


    /**
     * Run all the task for update counters at init process
     *
     * @method run
     
     */
    this.run = function() {
        var threadpool = new ThreadPool(this.POLL_MAX);
        var core = new CounterCore(this.questionnaireId);

        function count(_core, qId, _ui) {

            // Execute update 
            var counters = _core.fullCount(qId);
            _ui.updateCounters(qId, counters);
            // Set this task to be completed. 
            this.complete();
        }
        var self = this;
        $('.questionset').each(function(qsetId) {
            if (qsetId != 0 && qsetId != 99) {
                var runnable = new Runnable(count, 1, core, qsetId, self.ui);
                threadpool.run(runnable);
            }
        });
        threadpool.destroy();

    };


};

$(document).ready(function() {
    var core = new CounterCore();
    var ui = new CounterUI();
    var tasker = new CounterTasker(ui, 0);
    tasker.run();

});