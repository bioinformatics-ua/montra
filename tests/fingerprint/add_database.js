module.exports = {
  "Adding a database" : function (browser) {
    browser
      .url("http://127.0.0.1:8000/")
      .waitForElementVisible('body', 1000)
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 1000)
      .url("http://127.0.0.1:8000/add/49/0/")
      .waitForElementVisible('li[id="li_qs_1"]', 1000)
      .click('a[href="add/49/1"]')
      .waitForElementVisible('input[id="question_1.01"]', 1000)
      .setValue('input[id="question_1.01"]', 'TestUnitDatabase')
      .click('input[type=submit]')
      .waitForElementVisible('div[id="success-message"]', 5000)
      .end();
  }
};
