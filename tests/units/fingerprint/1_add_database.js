module.exports = {
  "Adding a database" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .url(browser.launchUrl+"/add/49/0/")
      .waitForElementVisible('li[id="li_qs_1"]', 5000, 'Add database shell loads with success')
      .click('a[href$="add/49/1"]')
      .waitForElementVisible('input[id="question_1.01"]', 5000, 'Questionset 1 Loaded with success')
      .setValue('input[id="question_1.01"]', browser.globals.TUdatabase)
      .setValue('input[id="question_1.02"]', '')
      .click('input[type=submit]')
      .waitForElementVisible('div[id="success-message"]', 5000, 'Questionnaire creation with success')
      .end();
  }
};
