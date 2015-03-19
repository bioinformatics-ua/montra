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
  "Add Population Characteristics for the first time" : function (browser) {
    fs = require('fs')
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('[href="#populationcharacteristics"]')
      .setValue('#fileupload_hook', require('path').resolve(__dirname + '/resources/DB1_DataProfile_2014-03-17_15-38-07_v2.3.2.4.txt'))
      .pause(500)
      .click('#jerboafiles .btn-primary:first-child')
      .waitForElementVisible('#pc_list', 10000, 'Upload ended with success.')
      .click('.graphTypes:first-child')
      .waitForElementVisible('#pc_chart_place', 5000, 'Charts are visible.')
      .end();
  },
  "Update Existing Population Characteristics file with a new one": function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('[href="#populationcharacteristics"]')
      .click('#upload_popchar')
      .pause(500)
      .setValue('#fileupload_hook', require('path').resolve(__dirname + '/resources/DB1_DataProfile_2014-03-17_15-38-07_v2.3.2.4.txt'))
      .pause(500)
      .click('#jerboafiles .btn-primary:first-child')
      .waitForElementVisible('#pc_list', 10000, 'Upload ended with success.')
      .click('.graphTypes:first-child')
      .waitForElementVisible('#pc_chart_place', 5000, 'Charts are visible.')
      .end();
  },
  "Add a comment to a chart on Population Characteristics": function(browser){
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('[href="#populationcharacteristics"]')
      .waitForElementVisible('#pc_chart_place', 5000, 'Loaded first chart.')
      .setValue('[name="pc_chart_comment_name"]', 'Title of a example comment')
      .setValue('[name="pc_chart_comment_description"]', 'Example commentary')
      .click('#pc_chart_comment_submit')
      .waitForElementVisible('#pc_comments_placeholder blockquote', 5000, 'Comment added with success')
      .end();
  },
  "Remove a comment from a chart on Population Characteristics": function(browser){
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('[href="#populationcharacteristics"]')
      .waitForElementVisible('#pc_chart_place', 5000, 'Loaded first chart.')
      .click('#pc_comments_placeholder .delete_comment:first-child')
      .waitForElementNotPresent('#pc_comments_placeholder .delete_comment:first-child', 5000, 'Comment removed with success')
      .end();
  },
  "Export Population Characteristics chart as png": function(browser){
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('[href="#populationcharacteristics"]')
      .waitForElementVisible('#pc_chart_place', 5000, 'Loaded first chart.')
      .click('.exportmychart a:first-child')
      .click('#downloadpng')
      .assert.chartDownload("#downloadpng", 'Has download attribute')
      .pause(4000)
      .end();
  },
  "Manipulate Population Characteristics tabular view": function(browser){
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('[href="#populationcharacteristics"]')
      .waitForElementVisible('#pc_chart_place', 5000, 'Loaded first chart.')
      .click('#tabularlink')
      .waitForElementVisible('#pc_tabular_place', 5000, 'Opened tabular view')
      .assert.containsText(".sorting_1:first-child", "1990", "Table is showing")
      .click('#tabular_table thead th:first-child')
      .assert.containsText(".sorting_1:first-child", "2009", "Table is able to sort")
      .end();
  }/*,
  "Export Population Characteristics chart in Tabular View": function(browser){
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('[href="#populationcharacteristics"]')
      .waitForElementVisible('#pc_chart_place', 5000, 'Loaded first chart.')
      .click('#tabularlink')
      .waitForElementVisible('#pc_tabular_place', 5000, 'Opened tabular view')
      .click('#export_btns a:first-child')
      ... <- i cant do anything with the flash container...
      .end();
  }*/
};
