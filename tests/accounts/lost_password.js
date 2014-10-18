module.exports = {
  "Recover Password" : function (browser) {
    browser
      .url("http://127.0.0.1:8000/")
      .waitForElementVisible('body', 1000)
      .pause(1000)
      .click('a[href="accounts/password/reset/"]')
      .setValue('input[id=id_email]', 'ribeiro.r@ua.pt')
      .click('input[type=submit]')
      .waitForElementVisible('div[id=resetcomplete]', 1000)
      .assert.urlContains('done')
      .end();
  }
};
