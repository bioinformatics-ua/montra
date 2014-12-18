module.exports = {
  "Redo a free text search through Search History" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .waitForElementVisible('#actions a[href="advsearch/history"]', 10000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advsearch/history"]')
      .waitForElementVisible('#simple', 10000, 'Free Search history loads with success')
      .waitForElementVisible('.btn-info', 10000, 'Free Search History entries exist')
      .click('.btn-info:first-child')
      .waitForElementVisible('#loading',10000, 'Result loaded for simple search')
      .end();
  }
};
