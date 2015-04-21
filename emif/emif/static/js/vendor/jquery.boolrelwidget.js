/**********************************************************************
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
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
# */
(function($) {
    $.fn.boolrelwidget = function(options) {
        // so we dont lose track of who we are, and used to ensure chainability
        var self = this;
        var basic_blocks = [];
        var used_blocks = [];
        var expanded_containers = [];
        var mastergroup = null;
        // Default Options
        var settings = $.extend({
            expand_text: 'To define the relations between the terms click here',
            expand_text_read: 'To see the relations defined in this search click here',
            collapse_text: 'Click here to close this panel',
            collapse_text_read: 'Query in effect (Click here to close this panel)',
            query_text: 'Start filling the questionnary to start building a query...',
            form_anchor: null,
            auto_add: true,
            default_relation: BOOL['AND'],
            hide_concepts: true,
            view_only: false,
            view_serialized_string: null,
            help: null,
            link_back: null,
            inplace: false
        }, options);

        var funcs = {
            isEmpty: function() {
                return used_blocks.length == 0;
            },
            push: function(ident, rep, answer) {
                var bt = new BooleanTerminal(ident, rep, answer);

                if (bt.isNull())
                    return null;

                var block = this.pushWithoutDraw(bt);
                /* Only auto-add in case auto-add is on */

                if ((settings.auto_add == true) && (block != null)) {
                    var sliced = this.spliceById(block.id);

                    used_blocks.push(sliced);

                    if (mastergroup == null)
                        mastergroup = new BooleanGroup(sliced.copy());
                    else mastergroup.addById(mastergroup.id, sliced.copy(), settings.default_relation);
                }

                this.draw();

                return block;
            },
            pushWithDelegate: function(ident, rep, answer, delegate) {
                var bt = new BooleanTerminal(ident, rep, answer, delegate);

                if (bt.isNull())
                    return null;

                var block = this.pushWithoutDraw(bt);
                /* Only auto-add in case auto-add is on */

                if ((settings.auto_add == true) && (block != null)) {
                    var sliced = this.spliceById(block.id);

                    used_blocks.push(sliced);

                    if (mastergroup == null)
                        mastergroup = new BooleanGroup(sliced.copy());
                    else mastergroup.addById(mastergroup.id, sliced.copy(), settings.default_relation);
                }
                this.draw();

                return block;
            },
            pushWithoutDraw: function(bt) {
                if (this.getBooleanIndex(bt) != -1) {
                    console.warn('Variable ' + bt + ' already on basic blocks pool.');
                    return null;
                }
                if (this.getUsedIndex(bt) != -1) {
                    console.warn('Variable ' + bt + ' already on used basic blocks pool.');
                    return null;
                }
                var block = new BooleanGroup(bt);

                basic_blocks.push(block);
                console.warn('Pushed new variable ' + bt + ' to basic blocks pool.');

                return block;
            },
            pushBooleanGroup: function(obj) {
                if (!(obj instanceof BooleanGroup && obj.variables.length == 1)) {
                    console.warn('When adding, a valid simple BooleanGroup child must be found.');
                    return false;
                }
                if (!(obj.variables[0] instanceof BooleanTerminal && this.getBooleanIndex(obj.variables[0]) == -1)) {
                    console.warn('Variable ' + obj + ' already on basic blocks pool.');
                    return false;
                }

                basic_blocks.push(obj);
                console.log('Pushed new variable ' + obj + ' to basic blocks pool.');

                this.draw();

                return true
            },
            pushUsedBooleanGroup: function(obj) {
                if (!(obj instanceof BooleanGroup && obj.variables.length == 1)) {
                    console.warn('When adding, a valid simple BooleanGroup child must be found.');
                    return false;
                }
                if (!(obj.variables[0] instanceof BooleanTerminal && this.getUsedIndex(obj.variables[0]) == -1)) {
                    console.warn('Variable ' + obj + ' already on used blocks pool.');
                    return false;
                }

                used_blocks.push(obj);
                console.log('Pushed new variable ' + obj + ' to used blocks pool.');

                this.draw();

                return true
            },
            splice: function(ident, rep, answer) {
                var bt = new BooleanTerminal(ident, rep, answer);
                if (bt.isNull())
                    return null;

                var block;
                var id = this.getBooleanIndex(bt);
                if (id < 0) {

                    // If it fails, lets check if its being used
                    var other_id = this.getUsedIndex(bt);
                    if (other_id < 0) {
                        console.warn('No basic block ' + bt + ' from basic blocks pool to slice out.');
                        return null;
                    }

                    console.log('Variable is being used, removing it from mastergroup and removing it from used variables');
                    block = used_blocks.splice(other_id, 1)[0];

                    // Try to remove from mastergroup (if there is a mastergroup)
                    if (mastergroup != null)
                        mastergroup.removeById(block.id);

                    this.draw();

                    return block;
                }
                block = basic_blocks.splice(id, 1)[0];
                console.log('Sliced out variable ' + bt + ' from basic blocks pool.');

                this.draw();

                return block;
            },
            // ONLY ALLOWS SIMPLE BOOLEANS I define this manually because IE<=8 js lists doesnt have the method indexOF()
            getBooleanIndex: function(element) {

                var i = 0;
                console.log(basic_blocks);
                for (i = 0; i < basic_blocks.length; i++) {
                    // We must check this is a "empty" container with only one element (the one we want).
                    if (basic_blocks[i].containsOnly(element))
                        return i;
                }
                return -1;
            },
            // GENERIC I define this manually because IE<=8 js lists doesnt have the method indexOF()
            getIndex: function(list, element) {
                // Ref from: http://stackoverflow.com/questions/1058427/how-to-detect-if-a-variable-is-an-array
                if (!(Object.prototype.toString.call(list) === '[object Array]')) {
                    console.warn('Tried to pass a list which is not a list');
                }
                console.log(list);

                var i = 0;
                for (i = 0; i < list.length; i++) {
                    // We must check this is a "empty" container with only one element (the one we want).
                    if(list[i] instanceof BooleanGroup)
                        if (list[i].containsOnly(element))
                            return i;
                    else
                        if(list[i] === element)
                            return i;
                }
                return -1;
            },
            getUsedIndex: function(element) {
                var i = 0;
                for (i = 0; i < used_blocks.length; i++) {
                    // We must check this is a "empty" container with only one element (the one we want).
                    if (used_blocks[i].containsOnly(element))
                        return i;
                }

                return -1;
            },
            spliceById: function(number) {
                var id = this.getIndexById(number);
                if (id < 0) {
                    console.warn('No basic block with id ' + number + ' from basic blocks pool to slice out.');
                    return null;
                }
                var block = basic_blocks.splice(id, 1)[0];
                console.warn('Sliced out variable with id ' + number + ' from basic blocks pool.');

                return block;
            },
            // I define this manually because IE<=8 js lists doesnt have the method indexOF()
            getIndexById: function(id) {
                var i = 0;
                for (i = 0; i < basic_blocks.length; i++) {
                    // We must check this is a "empty" container with only one element (the one we want).
                    if (basic_blocks[i].id == id)
                        return i;
                }
                return -1;
            },
            draw: function() {
                //$('#boolrelwidget-basicblocks').html('');
                //$('#boolrelwidget-query').html('');
                // Drawing concepts


                if (!settings.hide_concepts) {
                    var little_boxes = [];

                    var i = 0;
                    for (i = 0; i < basic_blocks.length; i++) {
                        little_boxes.push('<span unselectable="on" class="btn-group boolrelwidget-block">');
                        little_boxes.push('<span id="boolrelwidget-bb-');
                        little_boxes.push(basic_blocks[i].id);
                        little_boxes.push('" class="btn boolrelwidget-block-inner">');
                        little_boxes.push('<div class="boolrelwidget-simple" data-toggle="tooltip" title="');
                        little_boxes.push(basic_blocks[i].variables[0].toString());
                        little_boxes.push('">');

                        little_boxes.push(basic_blocks[i].variables[0].toString());
                        little_boxes.push('</div>');
                        little_boxes.push('</span>');
                        //little_boxes.push('<span class="btn btn-danger boolrelwidget-delete">');
                        //little_boxes.push('X');
                        //little_boxes.push('</span>');
                        little_boxes.push('</span>');

                    }

                    if (little_boxes.length == 0) {
                        $('#boolrelwidget-basicblocks', self).html("This box shows unused terms that have a value filled but are not being used on the query (when any).");
                    } else {
                        $('#boolrelwidget-basicblocks', self).html(little_boxes.join(''));
                        // Make them draggable

                        if (!settings.view_only) {
                            // Clone makes ie7 crash and burn
                            $(".boolrelwidget-block-inner", self).draggable({
                                containment: "#boolrelwidget-panel",
                                revert: true,
                                opacity: 0.9,
                                /*helper: "clone",*/
                                cursor: "move",
                                cursorAt: {
                                    top: 10,
                                    left: 50
                                }
                            });
                        }
                    }
                } else {
                    $('#boolrelwidget-basicblocks-out', self).fadeOut('fast');
                }

                // Drawing query itself(if any already)
                if (mastergroup && mastergroup.variables.length > 0) {
                    var big_box = [];
                    var i = 0;
                    this.harvest(mastergroup, big_box, 0);

                    $('#boolrelwidget-query', self).html(big_box.join(''));

                    var master = this;
                    if (!settings.view_only) {
                        $(".boolrelwidget-query-dropper", self).droppable({
                            hoverClass: "boolrelwidget-query-hover",
                            drop: function(event, ui) {
                                $(".boolrelwidget-query-dropper", self).tooltip('disable');
                                var drag = ui.draggable.attr('id');
                                // If coming from basic blocks
                                if (typeof drag != 'undefined' && drag.lastIndexOf('boolrelwidget-bb-', 0) === 0) {
                                    var droper = Number(ui.draggable.attr('id').replace('boolrelwidget-bb-', ''));
                                    var dropee = Number($(this).attr('id').replace('boolrelwidget-dp-', ''));
                                    console.log("Event drop 1: " + droper + " on " + dropee);

                                    var sliced = master.spliceById(droper);

                                    used_blocks.push(sliced);
                                    // Try to add this to the master group
                                    // If we cant, we insert the basic block back into the basic_blocks list
                                    if (!mastergroup.addById(dropee, sliced.copy(), settings.default_relation)) {
                                        master.pushBooleanGroup(sliced);
                                    } else {
                                        used_blocks.push(sliced);
                                    }
                                }
                                // If comming from the query itself
                                else {
                                    var droper = Number(ui.draggable.attr('id').replace('boolrelwidget-ii-', ''));
                                    var dropee = Number($(this).attr('id').replace('boolrelwidget-dp-', ''));
                                    console.log("Event drop 2: " + droper + " on " + dropee);

                                    // Makes no sense to move self to self
                                    if (droper != dropee) {
                                        var sliced = mastergroup.removeById(droper);

                                        mastergroup.addById(dropee, sliced, settings.default_relation);

                                    }

                                }
                                $(".tooltip", self).remove();

                                master.draw();

                            }
                        });
                        $(".boolrelwidget-query-dropper", self).tooltip({
                            container: 'body',
                            delay: {
                                show: 500,
                                hide: 0
                            }
                        });

                    }
                    /* Firefox has a problem with the container if its not cloned ... */
                    if (!settings.view_only) {
                        if (navigator.userAgent.indexOf("Firefox") != -1) {
                            $(".boolrelwidget-query-box > .boolrelwidget-simple", self).parent().draggable({
                                containment: "#boolrelwidget-panel",
                                revert: true,
                                opacity: 0.9,
                                cursor: "move",
                                cursorAt: {
                                    top: 10,
                                    left: 50
                                },
                                helper: 'clone'
                            });
                        } else {
                            $(".boolrelwidget-query-box > .boolrelwidget-simple", self).parent().draggable({
                                containment: "#boolrelwidget-panel",
                                revert: true,
                                opacity: 0.9,
                                cursor: "move",
                                cursorAt: {
                                    top: 10,
                                    left: 50
                                }
                            });
                        }
                    }

                    // Add
                    $(".boolrelwidget-query-delete", self).click(function() {
                        var removed = Number($(this).attr('id').replace('boolrelwidget-dl-', ''));

                        var removed_bool = mastergroup.removeById(removed);

                        var contained = removed_bool.extractAllSimple();

                        for (var j = 0; j < contained.length; j++) {
                            if (settings.hide_concepts)
                                contained[j].callDelegate();
                            else
                                master.pushBooleanGroup(contained[j].copy());

                            var other_id = master.getUsedIndex(contained[j].variables[0]);
                            if (other_id > -1) {
                                used_blocks.splice(other_id, 1);

                            }
                        }
                        master.draw();
                    });
                    $(".boolrelwidget-select", self).change(function() {
                        console.log(mastergroup);

                        var changed = $(this).attr('id').replace('boolrelwidget-query-sl-', '');
                        changed = changed.split('-');
                        if (changed.length == 2) {
                            console.log('Changed relationship to ' + $(this).val() + ' in ' + changed[0] + ' at position ' + changed[1]);

                            mastergroup.changeRelation(Number(changed[0]), Number(changed[1]), BOOL[$(this).val()]);

                            console.log(mastergroup);

                        } else {
                            console.error('Impossible to select correctly a relation');
                        }
                    });
                    $(".boolrelwidget-collapser", self).click(function() {

                        var collapsing = Number($(this).attr('id').replace('boolrelwidget-cl-', ''));
                        if ($(this).hasClass("boolrelwidget-collapsed")) {
                            $(this).removeClass('boolrelwidget-collapsed');
                            $(this).addClass('boolrelwidget-expanded');
                            $(this).html('<i class="icon-zoom-in"></i>Expand');
                            $("#" + $(this).parent().attr('id') + ' > .boolrelwidget-expandable', self).fadeOut('fast');
                            master.removeExpandedContainer($(this).parent().attr('id'));
                        } else {
                            $(this).removeClass('boolrelwidget-expanded');
                            $(this).addClass('boolrelwidget-collapsed');
                            $(this).html('<i class="icon-zoom-out"></i> Collapse');
                            $("#" + $(this).parent().attr('id') + ' > .boolrelwidget-expandable', self).fadeIn('fast');
                            $("#" + $(this).parent().attr('id') + ' > .boolrelwidget-expandable', self).css("display", "table-cell");
                            master.addExpandedContainer($(this).parent().attr('id'));
                        }
                    });


                } else {
                    var master = this;
                    mastergroup = null;
                    $('#boolrelwidget-query', self).html('<div class="boolrelwidget-first-droppable">' + settings.query_text + '</div>');
                    if (!settings.view_only) {
                        $(".boolrelwidget-first-droppable", self).droppable({
                            hoverClass: "boolrelwidget-query-hover",
                            drop: function(event, ui) {

                                var droper = Number(ui.draggable.attr('id').replace('boolrelwidget-bb-', ''));
                                console.log("Event drop0: " + droper + " on empty space, creating new booleangroup.");

                                var sliced = master.spliceById(droper);

                                // Try to add this to the master group
                                // If we cant, we insert the basic block back into the basic_blocks list
                                mastergroup = sliced.copy();

                                // Put in used blocks
                                $(".tooltip").fadeOut('fast');

                                master.draw();

                            }
                        });
                    }
                }
                $(".boolrelwidget-simple", self).tooltip({
                    container: 'body',
                    delay: {
                        show: 500,
                        hide: 0
                    }
                }).css('z-index', '2001');

                // If we have collapsing preferences, apply them
                if (this.getCookie('boolrelwidget-collapse-preferences')) {
                    if (this.getCookie('boolrelwidget-collapse-preferences') == 'expanded') {
                        var context = $('boolrelwidget-collapseall', self);
                        $('#boolrelwidget-collapseall', self).text('Collapse All');
                        $('#boolrelwidget-collapseall', self).addClass('boolrelwidget-all-expanded');

                        this.collapseAll(context);
                    }
                }

                // Expand all already open if memorized
                master.expandAllMemorized();
            },
            // This recursive functions runs down in the BooleanGroups and puts everything on the big box.
            // I pass a counter to be able to style differently (so i know the recursion level couldnt find a better way to style it different
            harvest: function(something, big_box, counter) {
                if (something instanceof BooleanTerminal) {
                    big_box.push('<div class="boolrelwidget-simple" data-toggle="tooltip" title="' +
                        something.toString() + ' ' + something.val + '">');

                    if (settings.view_only)
                        big_box.push('<strong>');
                    big_box.push(something.toString());
                    if (settings.view_only)
                        big_box.push(':</strong><br />' + something.val);

                    big_box.push('</div>');
                } else if (something instanceof BooleanGroup) {
                    var k = 0;

                    // First one doesnt have a operator associated
                    big_box.push('<span class="btn-group boolrelwidget-query-box-outer" id="boolrelwidget-ob-');
                    big_box.push(something.id);
                    big_box.push('">');
                    if (counter % 2 == 0) {
                        if (!something.isSimple() && counter > 0) {
                            big_box.push('<div class="btn boolrelwidget-collapser boolrelwidget-collapsed" id="boolrelwidget-cl-');
                            big_box.push(something.id);
                            big_box.push('"><i class="icon-zoom-in"></i> Expand</div>');
                        }
                        big_box.push('<div class="btn boolrelwidget-odd boolrelwidget-query-box');
                        if (counter > 0 && !something.isSimple())
                            big_box.push(' boolrelwidget-expandable');
                        big_box.push('" id="boolrelwidget-ii-');
                        big_box.push(something.id);
                        big_box.push('">');
                    } else {
                        if (!something.isSimple() && counter > 0) {
                            big_box.push('<div class="btn btn-inverse boolrelwidget-collapser" id="boolrelwidget-cl-');
                            big_box.push(something.id);
                            big_box.push('"><i class="icon-zoom-in"></i> Expand</div>');
                        }
                        big_box.push('<div class="btn btn-inverse boolrelwidget-even boolrelwidget-query-box');
                        if (counter > 0 && !something.isSimple())
                            big_box.push(' boolrelwidget-expandable');
                        big_box.push('" id="boolrelwidget-ii-');
                        big_box.push(something.id);
                        big_box.push('">');
                    }
                    this.harvest(something.variables[k++], big_box, counter + 1);

                    // All others in the big box have
                    for (k = 1; k < something.variables.length; k++) {
                        // Add relation box
                        big_box.push(this.operator_selectbox(something, k - 1, counter));

                        this.harvest(something.variables[k], big_box, counter + 1);
                    }
                    big_box.push("</div>");
                    if (!settings.view_only) {
                        big_box.push('<div id="boolrelwidget-dp-');
                        big_box.push(something.id);
                        if (counter % 2 == 0) {
                            big_box.push('" title="Drag other concepts here, to nest a relation with this concept. See help for more details." data-toggle="tooltip" class="btn boolrelwidget-query-dropper');

                            if (!something.isSimple() && counter > 0)
                                big_box.push(' boolrelwidget-expandable');
                            big_box.push('"><div class="boolrelwidget-query-dropper-odd">&nbsp;&nbsp;</div></div>');
                        } else {
                            big_box.push('" title="Drag other concepts here, to nest a relation with this concept. See help for more details." data-toggle="tooltip" class="btn btn-inverse boolrelwidget-query-dropper');
                            if (!something.isSimple() && counter > 0)
                                big_box.push(' boolrelwidget-expandable');
                            big_box.push('"><div class="boolrelwidget-query-dropper-even">&nbsp;&nbsp;</div></div>');
                        }
                    }
                    // Cant delete mastergroup, other can be deleted
                    if (!settings.view_only) {
                        if (counter != 0) {
                            if (counter % 2 == 0)
                                big_box.push('<div class="btn boolrelwidget-query-delete');
                            else
                                big_box.push('<div class="btn btn-inverse boolrelwidget-query-delete');

                            if (!something.isSimple())
                                big_box.push(' boolrelwidget-expandable');

                            big_box.push('" id="boolrelwidget-dl-');
                            big_box.push(something.id);

                            if (counter % 2 == 0)
                                big_box.push('"><div class="boolrelwidget-query-delete-odd"></div></div>');
                            else
                                big_box.push('"><div class="boolrelwidget-query-delete-even"></div></div>');
                        }
                    }
                    big_box.push('</span>');
                } else {
                    console.error(something + ' cant be put in the big_box, because its not of type string nor BooleanGroup.');
                }
            },
            operator_selectbox: function(something, selected, counter) {
                var select = [];
                var relation = something.relations[selected].name;

                select.push('<span class="boolrelwidget-query-operator"><select id="boolrelwidget-query-sl-');
                select.push(something.id);
                select.push('-');
                select.push(selected);
                if (settings.view_only)
                    select.push('" class="boolrelwidget-select" disabled="disabled">');
                else
                    select.push('" class="boolrelwidget-select">');

                for (var index in BOOL) {
                    if (BOOL[index].name == relation)
                        select.push('<option selected="selected">');
                    else
                        select.push('<option>');
                    select.push(BOOL[index].name);
                    select.push('</option>');
                }
                select.push('</select></span>');

                return select.join('');
            },
            reset: function() {
                if (settings.hide_concepts) {
                    if(mastergroup != null){
                        var contained = mastergroup.extractAllSimple();

                        for (var j = 0; j < contained.length; j++) {
                            if (settings.hide_concepts)
                                contained[j].callDelegate();
                            else
                                this.pushBooleanGroup(contained[j].copy());

                            var other_id = this.getUsedIndex(contained[j].variables[0]);
                            if (other_id > -1) {
                                used_blocks.splice(other_id, 1);
                            }
                        }
                        this.draw();
                    }
                } else {
                    if (mastergroup != 'null') {
                        var simples = mastergroup.extractAllSimple();
                        mastergroup = null;
                        used_blocks = [];
                        for (var i = 0; i < simples.length; i++)
                            this.pushBooleanGroup(simples[i]);
                    }
                }

                console.log(mastergroup);
                console.log(basic_blocks);
                console.log(used_blocks);
            },
            opAll: function(func) {
                if (!isBool(func)) {
                    console.error('Tried to make a op_all operatiom with a invalid bool enum');
                    return false;
                }
                // First we reset
                this.reset();

                // Then we add all to a new mastergroup
                if (basic_blocks.length > 0) {
                    var j = 0;
                    mastergroup = new BooleanGroup(basic_blocks[j++]);
                    for (var j = 1; j < basic_blocks.length; j++) {
                        mastergroup.addBoolean(func, basic_blocks[j]);
                    }

                    used_blocks = basic_blocks;
                    basic_blocks = [];
                }
                this.draw();

                return true;
            },
            /* Ref on this on : http://stackoverflow.com/questions/1458724/how-to-set-unset-cookie-with-jquery */
            setCookie: function(key, value) {
                var expires = new Date();
                expires.setTime(expires.getTime() + (1 * 24 * 60 * 60 * 1000));
                document.cookie = key + '=' + value + ';path=/' + ';expires=' + expires.toUTCString();
            },
            getCookie: function(key) {
                var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
                return keyValue ? keyValue[2] : null;
            },
            collapseAll: function(context) {

                if ($(context).hasClass('boolrelwidget-all-expanded')) {

                    $('.boolrelwidget-expandable', self).fadeOut('fast');
                    $("#" + $('.boolrelwidget-expandable', self).parent().attr('id') + ' > .boolrelwidget-collapser').html('<i class="icon-zoom-in"></i> Expand');

                    $(context).text('Expand All');
                    $(context).removeClass('boolrelwidget-all-expanded');

                    funcs.setCookie('boolrelwidget-collapse-preferences', 'collapsed');
                } else {

                    $('.boolrelwidget-expandable', self).fadeIn('fast').css('display', 'table-cell');
                    $("#" + $('.boolrelwidget-expandable', self).parent().attr('id') + ' > .boolrelwidget-collapser').html('<i class="icon-zoom-out"></i> Collapse');
                    $(context).text('Collapse All');
                    $(context).addClass('boolrelwidget-all-expanded');

                    funcs.setCookie('boolrelwidget-collapse-preferences', 'expanded');
                }

            },
            expandPanel: function() {
                $('#boolrelwidget-expand', self).toggle();
                $('#boolrelwidget-collapse', self).toggle();
                $('#boolrelwidget-panel', self).toggle();
                funcs.setCookie('boolrelwidget-panel-open', 'true');
            },
            collapsePanel: function() {
                $('#boolrelwidget-expand', self).toggle();
                $('#boolrelwidget-collapse', self).toggle();
                $('#boolrelwidget-panel', self).toggle();

                funcs.setCookie('boolrelwidget-panel-open', 'false');
            },
            addExpandedContainer: function(container) {
                console.log('ADD EXPANDED CONTAINER');
                if (this.getIndex(expanded_containers, container) == -1) {
                    expanded_containers.push(container);
                } else {
                    console.log('-- Expanded container is already on the list');
                }
            },
            removeExpandedContainer: function(container) {

                var index = this.getIndex(expanded_containers, container);
                if (index != -1) {
                    expanded_containers.splice(index, 1);
                } else {
                    console.log('-- Expanded container is not on the list');
                }
            },
            expandAllMemorized: function() {
                for (var j = 0; j < expanded_containers.length; j++) {
                    // Lets check if this container really exists (it can be erased by inference)
                    if (!this.containerExists(expanded_containers[j]))
                        expanded_containers.splice(j, 1);
                    else {
                        $("#" + expanded_containers[j] + ' > .boolrelwidget-expandable', self).fadeIn('fast');
                        $("#" + expanded_containers[j] + ' > .boolrelwidget-expandable', self).css("display", "table-cell");
                    }
                }
            },
            containerExists: function(container_id) {
                if ($('#' + container_id).length)
                    return true;

                return false;
            },
            readyToSubmit: function() {
                if (mastergroup != null && mastergroup != 'null') {
                    $('#boolrelwidget-boolean-representation').val(mastergroup.toQuery());
                    $('#boolrelwidget-boolean-serialization').val(mastergroup.serialize());
                } else {
                    $('#boolrelwidget-boolean-representation').val('');
                    $('#boolrelwidget-boolean-serialization').val('');
                }
            }
        };

        // Murphy's law says people will forget to pass a div container, give helpful hint
        if (!this.is('div')) {
            console.error('You must specify a div container to add the boolean relations widget!');
            return this;
        }
        // If its a div lets prepare the widget and add functions to it

        // Lets style the div properly
        if(!settings.inplace)
            self = self.addClass('boolrelwidget-container');

        // Let it be empty
        self = self.html('');

        // Now lets add the toolbar
        var toolbar_content = '<ul id="boolrelwidget-expand" class="boolrelwidget-menu-container"><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-l"><div class="boolrelwidget-arrow-up"></div></div></li><li class="boolrelwidget-menu">';

        if (settings.view_only)
            toolbar_content += settings.expand_text_read;
        else toolbar_content += settings.expand_text;

        toolbar_content += '</li><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-r"><div class="boolrelwidget-arrow-up"></div></div></li></ul><ul id="boolrelwidget-collapse" class="boolrelwidget-menu-container-panel"><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-l"><div class="boolrelwidget-arrow-down"></div></div></li><li class="boolrelwidget-menu">';

        if (settings.view_only)
            toolbar_content += settings.collapse_text_read;
        else
            toolbar_content += settings.collapse_text;

        toolbar_content += '</li><li class="boolrelwidget-menu"><div class="boolrelwidget-arrow-r"><div class="boolrelwidget-arrow-down"></div></div></li></ul><div id="boolrelwidget-panel"><div id="boolrelwidget-basicblocks-out"><strong>Unused Terms</strong><div id="boolrelwidget-basicblocks" class="well well-small">Loading...</div></div><div class="clearfix">';


        if (!settings.view_only) {
            toolbar_content += '<div class="boolrelwidget-menu pull-left"><strong>Boolean Query</strong></div><div class="pull-right boolrelwidget-menu btn-group">';

            toolbar_content += '<a href="#boolrelwidgethelper" role="button" class="btn" data-toggle="modal"><i class="icon-question-sign"></i> Help</a>';

            if (settings.form_anchor) {
                toolbar_content += '<button id="boolrelwidget-search" class="btn">Search</button>';

                // Also add the hidden input to the form
                $(settings.form_anchor).append('<input type="hidden" id="boolrelwidget-boolean-representation" name="boolrelwidget-boolean-representation" value=" " />');
                $(settings.form_anchor).append('<input type="hidden" id="boolrelwidget-boolean-serialization" name="boolrelwidget-boolean-serialization" value=" " />');
            }

            toolbar_content += '<button id="boolrelwidget-collapseall" class="btn">Expand All</button><button class="btn" id="boolrelwidget-orall">Or All Concepts</button><button class="btn" id="boolrelwidget-andall">And All Concepts</button><button class="btn" id="boolrelwidget-clear">Reset</button></div>';
        } else {
            if(!settings.norefine)
                toolbar_content += '<button onclick="window.location.replace(\'' + settings.link_back + '\'); return false;" class="pull-right btn">Refine Search</button>';
        }
        if(settings.inplace){
            toolbar_content += '</div><div id="boolrelwidget-query">Loading...</div></div>';
        } else {
            toolbar_content += '</div><div id="boolrelwidget-query" class="well well-small">Loading...</div></div>';
        }

        toolbar_content += '<!-- Modal --><div id="boolrelwidgethelper" class="boolrelwidgethelpercontainer modal hide fade" tabindex="-1" role="dialog" aria-labelledby="boolrelwidgethelperLabel" aria-hidden="true">  <div class="modal-header">    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>    <h3 id="boolrelwidgethelperLabel">Help</h3>  </div>  <div class="boolrelwidgethelper modal-body">' + settings.help + '</div>  <div class="modal-footer">    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button></div></div>'

        self = self.append(toolbar_content);

        // Lets add the event handlersx
        $('#boolrelwidget-expand', self).click(function() {
            funcs.expandPanel();
        });
        $('#boolrelwidget-collapse', self).click(function() {
            funcs.collapsePanel();
        });
        if (funcs.getCookie('boolrelwidget-panel-open') == 'true' || settings.inplace == true) {
            funcs.expandPanel();
        }
        $('#boolrelwidget-search', self).click(function() {
            funcs.readyToSubmit();

            $(settings.form_anchor).submit();
        });
        $('#boolrelwidget-collapseall', self).click(function() {
            funcs.collapseAll(this);
        });
        $('#boolrelwidget-orall', self).click(function() {
            funcs.opAll(BOOL['OR']);
        });
        $('#boolrelwidget-andall', self).click(function() {
            funcs.opAll(BOOL['AND']);
        });
        //if (settings.hide_concepts) {
        //    $('#boolrelwidget-clear').fadeOut('fast');
        //}
        $('#boolrelwidget-clear', self).click(function() {
            funcs.reset();
        });

        if(settings.inplace === true){
            $('#boolrelwidget-collapse', self).hide();
            $('#boolrelwidget-panel', self).css('background-color', 'transparent');
        }

        if (settings.view_serialized_string) {
            var temp = new BooleanGroup(null).deserialize(settings.view_serialized_string);
            var simple_ones = temp.extractAllSimple();
            for (var i = 0; i < simple_ones.length; i++)
                funcs.pushUsedBooleanGroup(simple_ones[i].copy());

            mastergroup = temp;
        }
        // Draw things up
        funcs.draw();

        return funcs;
    };
}(jQuery));


/*
 *  Possible Boolean Operations Enumerable and validator
 *  Since i have to support IE7, BOOL['TYPE'] has to be used everywhere instead of BOOL.TYPE
 *  This must be because if we try a BOOL.TYPE that doesn't exist on ie 7 everything crashes (oh my life...)
 */
var BOOL = {
    // NOP   : { value: -1, name: "NOP"}, // No operation, means its a edge branch
    AND: {
        value: 0,
        name: "AND"
    },
    OR: {
        value: 1,
        name: "OR"
    }
    /*,
  XOR   : { value: 2, name: "XOR"},
  NOR   : { value: 3, name: "NOR"},
  NAND  : { value: 4, name: "NOR"},
*/
};

function isBool(op) {
    if (!op) return false;

    for (var index in BOOL) {
        if (op.value == BOOL[index].value)
            return true;
    }
    return false;
}

/* Defining a unique counter of ids to attribute booleanVariable instances
 * (this is used to facilitate encountering nested references */

var boolrelwidgetuniqueidcounter = 10000;


function BooleanTerminal(identificator, representation, value, deldelegate) {
    this.id = null;
    this.text = null;
    this.val = null;
    this.delete_delegate = null;

    if (identificator == null && representation == null && value == null) {
        // nothing
    } else {
        if (!(typeof identificator == 'string' || identificator instanceof String)) {
            console.warn('Identificator on BooleanTerminal must be a string');
            return null;
        }
        if (!(typeof representation == 'string' || representation instanceof String)) {
            console.warn('Representation on BooleanTerminal must be a string');
            return null;
        }
        if (!(typeof value == 'string' || value instanceof String)) {
            console.warn('Value on BooleanTerminal must be a string');
            return null;
        }
        if (identificator == '' || representation == '') {
            console.warn('Tried to add a BooleanTerminal with empty identificator or representation, that is impossible, the only possible empty variable is value.');
            return null;
        }
        this.id = identificator;
        this.text = representation;
        this.val = value;
        this.delete_delegate = deldelegate;
    }
}
BooleanTerminal.prototype = {
    toString: function() {
        return this.text;
    },
    toQuery: function() {
        var suffix="]";
        if (this.id && this.val){
            if(this.val.lastIndexOf("[") == 0 &&
                this.val.indexOf(suffix, this.val.length - suffix.length) !== -1)
                return this.id + ": " + this.val.replace(/"/g, '\\"');
            else
                return this.id + ': "' + this.val.replace(/"/g, '\\"') + '"';
        } else return '';
    },
    serialize: function() {
        return 'T;;;;;' + encodeURI(this.id) + ';;;;;' + encodeURI(this.text) + ';;;;;'
        + encodeURI(this.val) + ';;;;;' + encodeURI(this.delete_delegate);
    },
    deserialize: function(str) {
        str = str.split(';;;;;');
        if (str.length != 5)
            console.error("Couldn't parse Bolean Terminal prototype");
        else {
            this.id = decodeURI(str[1]);
            this.text = decodeURI(str[2]);
            this.val = decodeURI(str[3]);
            this.delete_delegate = decodeURI(str[4]);
        }
        return this;
    },
    equals: function(other_bt) {
        if (!(other_bt instanceof BooleanTerminal))
            return false;

        if (this.id != other_bt.id)
            return false;

        return true;
    },
    /* Since this language is prototype based, i cant just return null on a constructor (since there's none)
        i have to make a method to acertain nullity then
    */
    isNull: function() {
        if (!(this.id && this.text))
            return true;

        return false;
    }
}

function BooleanGroup(obj1) {
    if (!(obj1 instanceof BooleanGroup || obj1 instanceof BooleanTerminal || obj1 == null)) {
        console.warn('First operator of Boolean Group object must be a BooleanGroup or a BooleanTerminal');
        return null;
    }
    this.id = boolrelwidgetuniqueidcounter++;
    this.variables = [];
    this.relations = [];

    if (obj1 != null)
        this.variables.push(obj1);
}
BooleanGroup.prototype = {
    addBoolean: function(op, obj1) {

        if (!(obj1 instanceof BooleanGroup || obj1 instanceof BooleanTerminal)) {
            console.warn('Operator of Boolean Group object must be a BooleanGroup or a booleanterminal.');
            return null;
        }
        if (!isBool(op)) {
            console.warn('Relation between operators must be of a BOOL valid type.');
            return null;
        }
        this.variables.push(obj1);
        this.relations.push(op);
    },
    /* This returns a string representation of this object in boole's arithmetic format */
    toString: function() {
        var output = this.variables[0].toString();
        var i = 0;
        for (i = 1; i < this.variables.length; i++) {
            output += " " + this.relations[i - 1].name + " " + this.variables[i].toString();
        }
        if (this.variables.length > 1)
            output = "(" + output + ")";

        return output;
    },
    /* This returns a string representation of this object in query format */
    toQuery: function() {
        var output = this.variables[0].toQuery();
        var i = 0;
        for (i = 1; i < this.variables.length; i++) {
            output += " " + this.relations[i - 1].name + " " + this.variables[i].toQuery();
        }
        if (this.variables.length > 1)
            output = "(" + output + ")";

        return output;
    },
    /* While i realize this approach isnt the best, i was having problems with the recursivity and this worked
     * Maybe to review with more time at a later time
     */
    removeById: function(other_id) {
        var returnable = [];
        this.removeByIdAux(null, null, other_id, returnable);

        if (returnable.length == 2) {
            this.removeUnnecessary(returnable[1]);
            return returnable[0];
        } else if (returnable.length == 1)
            return returnable[0];
        else
            return null;

    },
    removeByIdAux: function(parent, branch, other_id, returnable) {
        if (typeof other_id != 'number') {
            console.warn('When removing by id, a number value must be specified. Found type ' + typeof other_id);
        } else {
            if (this.id == other_id) {
                returnable.push(this);

                // If not on root remove reference
                if (parent) {
                    parent.variables.splice(branch, 1);

                    if (branch = 0)
                        parent.relations.splice(branch, 1);
                    else
                        parent.relations.splice(branch - 1, 1);

                    // I also return this, to be able to later remove unnecessary
                    returnable.push(parent.id);
                }


            }
            var k = 0;
            for (k = 0; k < this.variables.length; k++) {
                if (this.variables[k] instanceof BooleanGroup) {
                    this.variables[k].removeByIdAux(this, k, other_id, returnable);
                }
            }
        }
    },
    removeUnnecessary: function(id_to_check) {
        this.removeUnnecessaryAux(null, null, id_to_check);
    },
    removeUnnecessaryAux: function(parent, branch, other_id) {
        if (typeof other_id != 'number') {
            console.warn('When removing unnecessary by id, a number value must be specified. Found type ' + typeof other_id);
        } else {
            if (this.id == other_id) {
                // If has root
                if (parent) {
                    // If this has only 1 element and is complexe, theres no need for this, we can revert back to
                    //only one level
                    if (this.variables.length == 1 && !(this.variables[0] instanceof BooleanTerminal)) {
                        parent.variables[branch] = this.variables[0];
                    }
                }
            }
            var k = 0;
            for (k = 0; k < this.variables.length; k++) {
                if (this.variables[k] instanceof BooleanGroup) {
                    this.variables[k].removeUnnecessaryAux(this, k, other_id);
                }
            }
        }

    },
    addById: function(parent_id, child, relation) {
        if (!(child instanceof BooleanGroup)) {
            console.warn('When adding, a valid BooleanGroup child must be found.');
        } else if (!isBool(relation)) {
            console.warn('The relation must be a valid BOOL enum.');

        }

        return this.addByIdAux(parent_id, child, relation);
    },
    addByIdAux: function(parent_id, child, relation) {
        if (typeof parent_id != 'number') {
            console.warn('When adding by id, a number value must be specified. Found type ' + typeof parent_id);
        } else {
            if (this.id == parent_id) {
                if (this.isSimple()) {
                    this.variables[0] = new BooleanGroup(this.variables[0]);
                }
                //Add reference
                this.relations.push(relation);
                this.variables.push(child);

                return true;
            }
            var returnable = false;
            var k = 0;
            for (k = 0; k < this.variables.length; k++) {
                if (this.variables[k] instanceof BooleanGroup) {
                    returnable = this.variables[k].addByIdAux(parent_id, child, relation);
                }
            }
            return returnable;
        }
    },
    changeRelation: function(container_id, index, new_value) {
        if (typeof container_id != 'number') {
            console.warn('When changing a relation the id must be a number. Found type ' + typeof parent_id);
        } else if (typeof index != 'number') {
            console.warn('When changing a relation the index must be a number. Found type ' + typeof parent_id);
        } else if (!isBool(new_value)) {
            console.warn('When changing a relation the new value must be a valid BOOL enum.');

        } else {
            //console.log("IDs: "+this.id+'=='+ container_id);

            if (this.id == container_id) {

                if (this.variables.length > index) {
                    this.relations[index] = new_value;
                    //  this.relations.splice(index,1,new_value);
                }
                return;
            }
            for (var k = 0; k < this.variables.length; k++) {
                if (this.variables[k] instanceof BooleanGroup) {
                    this.variables[k].changeRelation(container_id, index, new_value);
                }
            }
        }
    },
    containsOnly: function(bt) {
        if (this.variables.length > 1)
            return false;
        if (this.variables[0] instanceof BooleanGroup)
            return false;

        // If it equals, lets update the answer
        if (this.variables[0].equals(bt)) {
            this.variables[0].val = bt.val;
            return true;
        }

        return false;
    },
    isSimple: function() {
        if (this.variables.length == 1 && this.variables[0] instanceof BooleanTerminal)
            return true;

        return false;
    },
    extractAllSimple: function() {
        var returnable = [];

        if (this.isSimple())
            returnable.push(this);
        else
            this.extractAllSimpleAux(returnable);

        return returnable;
    },
    extractAllSimpleAux: function(returnable) {

        var k = 0;
        for (k = 0; k < this.variables.length; k++) {
            if (this.variables[k].isSimple())
                returnable.push(this.variables[k]);
            else
                this.variables[k].extractAllSimpleAux(returnable);
        }

    },
    destroy: function() {
        this.variables = null;
        this.relations = null;
    },
    serialize: function() {
        var serialized_string = "BEGIN_BG_" + this.id + "BEGIN_VAR_" + this.id;

        for (var i = 0; i < this.variables.length; i++) {
            serialized_string = serialized_string + this.variables[i].serialize() + "OTHER_" + this.id;
        }
        serialized_string = serialized_string + "END_VAR_" + this.id + "BEGIN_REL_" + this.id;
        for (var i = 0; i < this.relations.length; i++) {
            serialized_string = serialized_string + this.relations[i].name + ",";
        }
        serialized_string = serialized_string + "END_REL_" + this.id + "END_BG_" + this.id;

        return serialized_string;
    },
    deserialize: function(str) {
        // id, variables, rel

        if (str.indexOf('BEGIN_BG_') == 0) {
            // get id
            var identification = str.substring(9, 14);
            this.id = Number(identification);

            // get relations
            var init_relations = str.indexOf('BEGIN_REL_' + this.id) + 15;
            var end_relations = str.indexOf('END_REL_' + this.id);

            var relations_to_parse = str.substring(init_relations, end_relations).split(',');
            for (var i = 0; i < relations_to_parse.length - 1; i++)
                this.relations.push(BOOL[relations_to_parse[i]]);

            // get variables (that can be nested)
            var init_variables = str.indexOf('BEGIN_VAR_' + this.id) + 15;
            var end_variables = str.indexOf('END_VAR_' + this.id);

            var variables_to_parse = str.substring(init_variables, end_variables).split('OTHER_' + this.id);



            for (var i = 0; i < variables_to_parse.length - 1; i++) {
                if (variables_to_parse[i].indexOf('T;;;;;') == 0)
                    this.variables.push(new BooleanTerminal(null, null, null).deserialize(variables_to_parse[i]));
                else
                    this.variables.push(new BooleanGroup(null).deserialize(variables_to_parse[i]));
            }
        } else {
            console.error('Impossible to parse BooleanGroup object');
        }

        return this;
    },
    /* This only does shallow copies */
    copy: function() {
        var bg = new BooleanGroup(this.variables[0]);
        bg.id = this.id;

        for (var i = 1; i < this.variables.length; i++) {
            bg.variables.push(this.variables[i]);
        }
        for (var i = 1; i < this.relations.length; i++) {
            bg.relations.push(this.relations[i]);
        }

        return bg;
    },
    /* Probability should think of a better way of doing this, but since i want to allow it to be used to pass complete calls with parameters, as usual, i didnt find any other better way. Other solutions would envolve also keeping an array of parameters, and isnt much safer than doing this directly. since i could simple pass evals in this array of parameters and it would execute as a function anyway...
     */
    callDelegate: function() {
        if (this.isSimple() && this.variables[0].delete_delegate != null && (typeof this.variables[0].delete_delegate == 'string' || this.variables[0].delete_delegate instanceof String)) {

            eval(this.variables[0].delete_delegate);

        }
    }
};
