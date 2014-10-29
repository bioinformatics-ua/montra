module.exports = {
  "Searching using Advanced Search" : function (browser) {
    browser
      .url("http://127.0.0.1:8000/")
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 1000, 'Login successful')
      .waitForElementVisible('#actions a[href="advancedSearch/49/1"]', 3000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advancedSearch/49/1"]')
      .waitForElementVisible('li[id="li_qs_1"]', 2000, 'Advanced search loads with success')
      .waitForElementVisible('input[id="question_1.01"]', 2000, 'Questionset 1 Loaded with success')
      .setValue('input[id="question_1.01"]', 'ARS')
      .click('button[type=submit]')
      .waitForElementVisible('a[data-acronym="ARS"]', 5000, 'Search Returned with success')
      .end();
  }
};
