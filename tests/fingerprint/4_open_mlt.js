module.exports = {
  "Open more like this for a database" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 3000, 'Login successful')
      .url(browser.launchUrl+"/databases/")
      .waitForElementVisible('input[id="database_name_filter"]', 3000, 'Personal Database Listing successful')
      .setValue('input[id="database_name_filter"]', 'TestUnitDatabase')
      .waitForElementVisible('a[data-acronym="TestUnitDatabase"]', 3000, 'Filtering works, and database "TestUnitDatabase" exists')
      .click('a[data-acronym="TestUnitDatabase"]')
      .waitForElementVisible('a[id="managetoolbar"]', 3000, 'Database Summary for "TestUnitDatabase" loads')
      .click('#morelikethis_toolbar')
      .pause(2000)
      .assert.elementPresent('#results_size', 'More like this opens')
      .end();
  }
};
