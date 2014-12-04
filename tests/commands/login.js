exports.command = function(username, password, callback) {
  var self = this;
  callback = callback || function() {};

  return self.url(self.launchUrl)
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', username)
      .setValue('input[name=password]', password)
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 5000, 'Login successful')
};
