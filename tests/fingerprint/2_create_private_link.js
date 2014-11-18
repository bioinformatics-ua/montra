module.exports = {
  "Create a private link for a database" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 2000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 5000, 'Login successful')
      .url(browser.launchUrl+"/databases/")
      .waitForElementVisible('input[id="database_name_filter"]', 5000, 'Personal Database Listing successful')
      .setValue('input[id="database_name_filter"]', 'TestUnitDatabase')
      .waitForElementVisible('a[data-acronym="TestUnitDatabase"]', 5000, 'Filtering works, and database "TestUnitDatabase" exists')
      .click('a[data-acronym="TestUnitDatabase"]')
      .waitForElementVisible('a[id="managetoolbar"]', 5000, 'Database Summary for "TestUnitDatabase" loads')
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
