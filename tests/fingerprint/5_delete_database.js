module.exports = {
  "Deleting a database" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 1000, 'Login successful')
      .url(browser.launchUrl+"/databases/")
      .waitForElementVisible('input[id="database_name_filter"]', 1000, 'Personal Database Listing successful')
      .setValue('input[id="database_name_filter"]', 'TestUnitDatabase')
      .waitForElementVisible('a[data-acronym="TestUnitDatabase"]', 3000, 'Filtering works, and database "TestUnitDatabase" exists')
      .click('a[data-acronym="TestUnitDatabase"]')
      .waitForElementVisible('a[id="managetoolbar"]', 1000, 'Database Summary for "TestUnitDatabase" loads')
      .click('a[id="managetoolbar"]')
      .click('a[id="delete_list_toolbar"]')
      .waitForElementVisible('a[id="delete_fingerprint"]', 1000, 'Delete popup loads')
      .click('a[id="delete_fingerprint"]')
      .pause(3000)
      .end();
  }
};
