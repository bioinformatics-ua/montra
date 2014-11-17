module.exports = {
  "Redo a advanced search through Search History, refining it" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 3000, 'Login successful')
      .waitForElementVisible('#actions a[href="advsearch/history"]', 3000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advsearch/history"]')
      .waitForElementVisible('a[href="#advanced"]', 5000, 'History loads with success')
      .click('a[href="#advanced"]')
      .waitForElementVisible('#advanced .btn-block', 5000, 'Free Search History entries exist')
      .click('#advanced .btn-block')
      .waitForElementVisible('li[id="li_qs_1"]', 5000, 'Advanced search loads with success')
      .waitForElementVisible('input[id="question_1.01"]', 5000, 'Questionset 1 Loaded with success')
      .setValue('input[id="question_1.02"]', 'Agenzia regionale di sanità della Toscana')
      .click('button[type=submit]')
      .assert.elementPresent('#results_size', 'Result loaded for advanced search')
      .end();
  }
};
