module.exports = {
  "Adding a database" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 3000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 3000, 'Login successful')
      .url(browser.launchUrl+"/add/49/0/")
      .waitForElementVisible('li[id="li_qs_1"]', 3000, 'Add database shell loads with success')
      .click('a[href$="add/49/1"]')
      .waitForElementVisible('input[id="question_1.01"]', 3000, 'Questionset 1 Loaded with success')
      .setValue('input[id="question_1.01"]', 'TestUnitDatabase')
      .click('input[type=submit]')
      .waitForElementVisible('div[id="success-message"]', 5000, 'Questionnaire creation with success')
      .end();
  }
};
