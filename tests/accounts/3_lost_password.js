module.exports = {
  "Recover Password" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .click('a[href="accounts/password/reset/"]')
      .setValue('input[id=id_email]', 'ribeiro.r@ua.pt')
      .click('input[type=submit]')
      .waitForElementVisible('div[id=resetcomplete]', 1000, 'Login successful')
      .assert.urlContains('done')
      .end();
  }
};
