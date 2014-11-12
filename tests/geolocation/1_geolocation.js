module.exports = {
  "Check if geolocation is working" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('a[href="geo"]', 3000, 'Dashboards opens and link is visible')
      .click('a[href="geo"]')
      .waitForElementVisible('.gmnoprint', 3000, 'Compare Geolocation opens')
      .end();
  }
};

