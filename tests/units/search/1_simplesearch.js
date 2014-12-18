module.exports = {
  "Do simple freetext searches" : function (browser) {
    browser
      .login(browser.globals.username, browser.globals.password)
      .setValue('#edit-search-block-form--3', 'cardiac')
      .click('.canclear_search .icon-search')
      .waitForElementVisible('#loading', 10000, 'Result loaded for simple search: cardiac')
      .setValue('#edit-search-block-form--3', "'''%&£ \"\"\"")
      .click('.canclear_search .icon-search')
      .waitForElementVisible('#loading', 10000, 'Result loaded for simple search with characters that should be escaped')
      .end();
  }
};

