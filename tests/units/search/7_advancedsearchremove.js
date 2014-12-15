module.exports = {
  "Remove a advanced search from Search History" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .waitForElementVisible('#actions a[href="advsearch/history"]', 10000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advsearch/history"]')
      .waitForElementVisible('a[href="#advanced"]', 10000, 'History loads with success')
      .click('a[href="#advanced"]')
      .waitForElementVisible('#advanced .removebtn', 10000, 'Free Search History entries exist')
      .click('#advanced .removebtn')
      .waitForElementVisible('#advanced', 10000, 'Deleted with success')
      .end();
  }
};
