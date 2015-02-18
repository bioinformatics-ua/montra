/*
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
*/
var util = require('util');
exports.assertion = function(selector, className, msg) {

  var MSG_ELEMENT_NOT_FOUND = 'Testing if element <%s> has download attribute. ' +
    'Element could not be located.';

  this.message = msg || util.format('Testing if element <%s> has download attribute.', selector);

  this.expected = function() {
    return 'has ' + className;
  };

  this.pass = function(value) {
    return value != '';
  };

  this.failure = function(result) {
    var failed = result === false || result && result.status === -1;
    if (failed) {
      this.message = msg || util.format(MSG_ELEMENT_NOT_FOUND, selector);
    }
    return failed;
  };

  this.value = function(result) {
    return result.value;
  };

  this.command = function(callback) {
    return this.api.getAttribute(selector, 'download', callback);
  };

};
