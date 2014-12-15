exports.command = function(fingerprint_name, callback) {
  var self = this;
  callback = callback || function() {};

  return self.url(self.launchUrl+"/databases/")
      .waitForElementVisible('input[id="database_name_filter"]', 5000, 'Personal Database Listing successful')
      .setValue('input[id="database_name_filter"]', fingerprint_name)
      .waitForElementVisible('a[data-acronym="'+fingerprint_name+'"]', 5000, 'Filtering works, and database "'+fingerprint_name+'" exists')
      .click('a[data-acronym="'+fingerprint_name+'"]')
      .waitForElementVisible('a[id="managetoolbar"]', 5000, 'Database Summary for "'+fingerprint_name+'" loads');
};
