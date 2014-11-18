module.exports = {
  "Delete a private link from a database" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 1000, 'Page loads')
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
      .waitForElementVisible('#public_link_description', 5000, 'Private links popup loads')
      .waitForElementVisible('#public_links_table', 5000, 'Private link appears')
      .click('#public_links_table .privatedelete')
      .pause(1000)
      .waitForElementNotPresent('#public_links_table .privatedelete', 5000, 'Private link removed with success')
      .end();
  }
};
