module.exports = {
  "Login Existing User" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .end();
  }
};
