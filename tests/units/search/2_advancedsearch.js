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
module.exports = {
  "Searching using Advanced Search" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .waitForElementVisible('#actions a[href="advancedSearch/49/1"]', 10000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advancedSearch/49/1"]')
      .waitForElementVisible('li[id="li_qs_1"]', 10000, 'Advanced search loads with success')
      .waitForElementVisible('input[id="question_1.01"]', 10000, 'Questionset 1 Loaded with success')
      .clearValue('input[id="question_1.01"]')
      .setValue('input[id="question_1.01"]', 'ARS')
      .click('button[type=submit]')
      .waitForElementVisible('a[data-acronym="ARS"]', 10000, 'Search Returned with success')
      .end();
  }
};
