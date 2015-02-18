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
  "Erase a free text search through Search History" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .waitForElementVisible('#actions a[href="advsearch/history"]', 5000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advsearch/history"]')
      .waitForElementVisible('#simple', 5000, 'Free Search history loads with success')
      .waitForElementVisible('#simple .btn-info', 5000, 'Free Search History entries exist')
      .click('#simple .removebtn')
      .waitForElementVisible('#simple', 5000, 'Deleted with success')
      .end();
  }
};
