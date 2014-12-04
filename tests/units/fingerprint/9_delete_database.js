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
