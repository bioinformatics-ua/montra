module.exports = {
  "Delete a private link from a database" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('#managetoolbar')
      .click('#publiclink_toolbar')
      .waitForElementVisible('#public_link_description', 5000, 'Private links popup loads')
      .waitForElementVisible('#public_links_table', 5000, 'Private link appears')
      .click('#public_links_table .privatedelete')
      .pause(1000)
      .waitForElementNotPresent('#public_links_table .privatedelete', 5000, 'Private link removed with success')
      .end();
  }
};
