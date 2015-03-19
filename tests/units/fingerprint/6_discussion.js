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
  "Add a discussion comment" : function (browser) {
    fs = require('fs')
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('[href="#discussion"]')
      .setValue('#id_comment', "Example of a discussion comment on a fingerprint.")
      .click('#submit_button')
      .waitForElementVisible('#commentInserted', 5000, 'Commented inserted with success')
      .end();
  }/*,
  "Remove a discussion comment": function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('[href="#discussion"]')
      .end();
  }*/
};
