module.exports = {
  "Open more like this for a database" : function (browser) {
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
      .click('#morelikethis_toolbar')
      .pause(2000)
      .assert.elementPresent('#results_size', 'More like this opens')
      .end();
  }
};
