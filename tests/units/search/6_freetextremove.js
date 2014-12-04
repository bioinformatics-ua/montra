module.exports = {
  "Erase a free text search through Search History" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .waitForElementVisible('#actions a[href="advsearch/history"]', 5000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advsearch/history"]')
      .waitForElementVisible('#simple', 5000, 'Free Search history loads with success')
      .waitForElementVisible('#simple .btn-info', 5000, 'Free Search History entries exist')
      .click('#simple .removebtn')
      .waitForElementVisible('#simple', 5000, 'Deleted with success')
      .end();
  }
};
