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
