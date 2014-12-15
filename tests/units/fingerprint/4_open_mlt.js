module.exports = {
  "Open more like this for a database" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .fingerprint(browser.globals.TUdatabase)
      .click('#morelikethis_toolbar')
      .pause(2000)
      .assert.elementPresent('#results_size', 'More like this opens')
      .end();
  }
};
