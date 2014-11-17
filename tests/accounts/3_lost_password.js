module.exports = {
  "Recover Password" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 3000, 'Page loads')
      .pause(1000)
      .click('a[href$="accounts/password/reset/"]')
      .setValue('input[id=id_email]', 'ribeiro.r@ua.pt')
      .click('input[type=submit]')
      .waitForElementVisible('div[id=resetcomplete]', 5000, 'Login successful')
      .assert.urlContains('done')
      .end();
  }
};
