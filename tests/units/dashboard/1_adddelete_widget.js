module.exports = {
  "Dashboard Widget Removal/Addition" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .click('#feed .removewidget')
      .pause(1000)
      .click('a[data-handler="1"]')
      .pause(1000)
      .assert.elementNotPresent('#feed .removewidget', 'Feed widget is succesfully removed')
      .pause(1000)
      .click('#add_list_toolbar')
      .click('a[data-widgetname="feed"]')
      .assert.elementPresent('#feed .removewidget', 'Feed widget is succesfully added back again')
      .pause(2000)
      .end();
  }
};
