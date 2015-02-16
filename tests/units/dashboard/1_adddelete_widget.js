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
  "Dashboard Widget Removal/Addition" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .click('#feed .removewidget')
      .pause(1000)
      .click('a[data-handler="1"]')
      .pause(1000)
      .assert.elementNotPresent('#feed .removewidget', 'Feed widget is succesfully removed')
      .pause(1000)
      .click('#add_list_toolbar')
      .click('a[data-widgetname="feed"]')
      .assert.elementPresent('#feed .removewidget', 'Feed widget is succesfully added back again')
      .pause(2000)
      .end();
  }
};
