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
function generateUUID(){
    var d = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x7|0x8)).toString(16);
    });
    return uuid;
};

module.exports = {
  "Create User" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .click('a[href$="/accounts/signup/"]')
      .setValue('input[id=id_first_name]', 'Test')
      .setValue('input[id=id_last_name]', 'User')
      .setValue('input[id=id_organization]', 'Test Unit lda')
      .setValue('input[id=id_email]', 'longinus525+'+generateUUID()+'@gmail.com')
      .setValue('input[id=id_password1]', 'emif')
      .setValue('input[id=id_password2]', 'emif')
      .click('input[id=id_profiles_1]')
      .click('input[id=id_profiles_2]')
      .click('input[id=id_interests_1]')
      .click('input[id=id_interests_2]')
      // Cant do this so we dont spam users
      //.click('button[type=submit]')
      //.waitForElementVisible('div[id=signupcomplete]', 3000, 'Signup Result Page Opens')
      //.assert.urlContains('complete', 'Creating user ends with success')
      .end();
  }
};
