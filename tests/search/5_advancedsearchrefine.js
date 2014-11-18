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
      .waitForElementVisible('#actions a[href="advsearch/history"]', 10000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advsearch/history"]')
      .waitForElementVisible('a[href="#advanced"]', 10000, 'History loads with success')
      .click('a[href="#advanced"]')
      .waitForElementVisible('#advanced .btn-block', 10000, 'Advanced Search History entries exist')
      .click('#advanced .btn-block')
      .waitForElementVisible('li[id="li_qs_1"]', 10000, 'Advanced search loads with success')
      .waitForElementVisible('input[id="question_1.01"]', 10000, 'Questionset 1 Loaded with success')
      .setValue('input[id="question_1.02"]', 'Agenzia regionale di sanità della Toscana')
      .click('button[type=submit]')
      .waitForElementVisible('#loading',10000, 'Result loaded for advanced search')
      .end();
  }
};
