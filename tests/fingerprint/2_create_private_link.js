module.exports = {
  "Create a private link for a database" : function (browser) {
    browser
      .url("http://127.0.0.1:8000/")
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 1000, 'Login successful')
      .url("http://127.0.0.1:8000/databases/")
      .waitForElementVisible('input[id="database_name_filter"]', 1000, 'Personal Database Listing successful')
      .setValue('input[id="database_name_filter"]', 'TestUnitDatabase')
      .waitForElementVisible('a[data-acronym="TestUnitDatabase"]', 3000, 'Filtering works, and database "TestUnitDatabase" exists')
      .click('a[data-acronym="TestUnitDatabase"]')
      .waitForElementVisible('a[id="managetoolbar"]', 1000, 'Database Summary for "TestUnitDatabase" loads')
      .click('#managetoolbar')
      .click('#publiclink_toolbar')
      .waitForElementVisible('#public_link_description', 1000, 'Create Private link popup loads')
      .setValue('#public_link_description', 'Example of description of public link.')
      .pause(500)
      .click('#createpubliclink')
      .waitForElementVisible('#public_links_table', 1000, 'Private link appears')
      .click('#public_links_table a')
      .waitForElementVisible('a[href="#collapseDatabaseAdministrativeInformation"]', 1000, 'Private link Loaded with success')
      .end();
  }
};
