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
  "Datatable, getting table" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .waitForElementVisible('a[href="alldatabases/data-table"]', 5000, 'Dashboards opens and link is visible')
      .click('a[href="alldatabases/data-table"]')
      .waitForElementVisible('button[data-id="db_type"]', 5000, 'Compare Datatable opens')
      .click('button[data-id="db_type"]')
      .pause(500)
      .click('.dropdown-menu li[rel="1"] a')
      .pause(500)
      .click('#q_select_49 a[data-toggle="dropdown"]')
      .click('.qset_option:nth-child(1)')
      .pause(1000)
      .click('#update_table_button')
      .waitForElementVisible('#table_databases_names', 5000, 'Comparison Table shows up after selecting options')
      .end();
  }
};

