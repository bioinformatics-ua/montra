module.exports = {
  "Datatable, getting table" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('a[href="alldatabases/data-table"]', 3000, 'Dashboards opens and link is visible')
      .click('a[href="alldatabases/data-table"]')
      .waitForElementVisible('button[data-id="db_type"]', 3000, 'Compare Datatable opens')
      .click('button[data-id="db_type"]')
      .pause(500)
      .click('.dropdown-menu li[rel="1"] a')
      .pause(500)
      .click('#q_select_49 a[data-toggle="dropdown"]')
      .click('.qset_option:nth-child(1)')
      .pause(1000)
      .click('#update_table_button')
      .waitForElementVisible('#table_databases_names', 2000, 'Comparison Table shows up after selecting options')
      .end();
  }
};

