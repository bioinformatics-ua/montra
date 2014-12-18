module.exports = {
  "Redo a advanced search through Search History" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .waitForElementVisible('#actions a[href="advsearch/history"]', 10000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advsearch/history"]')
      .waitForElementVisible('a[href="#advanced"]', 10000, 'History loads with success')
      .click('a[href="#advanced"]')
      .waitForElementVisible('#advanced .btn-info', 10000, 'Free Search History entries exist')
      .click('#advanced .btn-info')
      .assert.elementPresent('#results_size', 'Result loaded for advanced search')
      .end();
  }
};
