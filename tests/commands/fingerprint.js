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
exports.command = function(fingerprint_name, callback) {
  var self = this;
  callback = callback || function() {};

  return self.url(self.launchUrl+"/databases/")
      .waitForElementVisible('input[id="database_name_filter"]', 5000, 'Personal Database Listing successful')
      .setValue('input[id="database_name_filter"]', fingerprint_name)
      .waitForElementVisible('a[data-acronym="'+fingerprint_name+'"]', 5000, 'Filtering works, and database "'+fingerprint_name+'" exists')
      .click('a[data-acronym="'+fingerprint_name+'"]')
      .waitForElementVisible('a[id="managetoolbar"]', 5000, 'Database Summary for "'+fingerprint_name+'" loads');
};
