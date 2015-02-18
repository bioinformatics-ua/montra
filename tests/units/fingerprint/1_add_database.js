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
  "Adding a database" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .url(browser.launchUrl+"/add/49/0/")
      .waitForElementVisible('li[id="li_qs_1"]', 5000, 'Add database shell loads with success')
      .click('a[href$="add/49/1"]')
      .waitForElementVisible('input[id="question_1.01"]', 5000, 'Questionset 1 Loaded with success')
      .setValue('input[id="question_1.01"]', browser.globals.TUdatabase)
      .setValue('input[id="question_1.02"]', '')
      .click('input[type=submit]')
      .waitForElementVisible('div[id="success-message"]', 5000, 'Questionnaire creation with success')
      .end();
  }
};
