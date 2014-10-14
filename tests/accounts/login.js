module.exports = {
  "Login Test" : function (browser) {
    browser
      .url("http://127.0.0.1:8000/")
      .waitForElementVisible('body', 1000)
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 1000)
      .end();
  }
};
