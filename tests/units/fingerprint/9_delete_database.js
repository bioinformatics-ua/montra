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
  "Deleting a database" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('a[id="managetoolbar"]')
      .click('a[id="delete_list_toolbar"]')
      .waitForElementVisible('a[id="delete_fingerprint"]', 5000, 'Delete popup loads')
      .click('a[id="delete_fingerprint"]')
      .pause(3000)
      .end();
  }
};
