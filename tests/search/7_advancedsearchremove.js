module.exports = {
  "Remove a advanced search from Search History" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 1000, 'Login successful')
      .waitForElementVisible('#actions a[href="advsearch/history"]', 3000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advsearch/history"]')
      .waitForElementVisible('a[href="#advanced"]', 2000, 'History loads with success')
      .click('a[href="#advanced"]')
      .waitForElementVisible('#advanced .removebtn', 2000, 'Free Search History entries exist')
      .click('#advanced .removebtn')
      .waitForElementVisible('#advanced', 2000, 'Deleted with success')
      .end();
  }
};
