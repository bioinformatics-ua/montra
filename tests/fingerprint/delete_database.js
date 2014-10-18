module.exports = {
  "Deleting a database" : function (browser) {
    browser
      .url("http://127.0.0.1:8000/")
      .waitForElementVisible('body', 1000)
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 1000)
      .url("http://127.0.0.1:8000/databases/")
      .waitForElementVisible('input[id="database_name_filter"]', 1000)
      .setValue('input[id="database_name_filter"]', 'TestUnitDatabase')
      .waitForElementVisible('a[data-acronym="TestUnitDatabase"]', 3000)
      .click('a[data-acronym="TestUnitDatabase"]')
      .waitForElementVisible('a[id="managetoolbar"]', 1000)
      .click('a[id="managetoolbar"]')
      .click('a[id="delete_list_toolbar"]')
      .waitForElementVisible('a[id="delete_fingerprint"]', 1000)
      .click('a[id="delete_fingerprint"]')
      .pause(3000)
      .end();
  }
};
