module.exports = {
  "Check if geolocation is working" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .waitForElementVisible('a[href="geo"]', 10000, 'Dashboards opens and link is visible')
      .click('a[href="geo"]')
      .waitForElementVisible('.gmnoprint', 10000, 'Compare Geolocation opens')
      .end();
  }
};

