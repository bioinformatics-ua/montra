module.exports = {
  "Create a private link for a database" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('#managetoolbar')
      .click('#publiclink_toolbar')
      .waitForElementVisible('#public_link_description', 5000, 'Create Private link popup loads')
      .setValue('#public_link_description', 'Example of description of public link.')
      .pause(500)
      .click('#createpubliclink')
      .waitForElementVisible('#public_links_table .pub_link:first-child', 5000, 'Private link appears')
      .click('#public_links_table .pub_link:first-child')
      .waitForElementVisible('a[href="#collapseDatabaseAdministrativeInformation"]', 5000, 'Private link Loaded with success')
      .end();
  }
};
