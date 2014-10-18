function generateUUID(){
    var d = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x7|0x8)).toString(16);
    });
    return uuid;
};

module.exports = {
  "Create User" : function (browser) {
    browser
      .url("http://127.0.0.1:8000/")
      .waitForElementVisible('body', 1000)
      .pause(1000)
      .click('a[href="/accounts/"]')
      .setValue('input[id=id_first_name]', 'Test')
      .setValue('input[id=id_last_name]', 'User')
      .setValue('input[id=id_organization]', 'Test Unit lda')
      .setValue('input[id=id_email]', 'longinus525+'+generateUUID()+'@gmail.com')
      .setValue('input[id=id_password1]', 'emif')
      .setValue('input[id=id_password2]', 'emif')
      .click('input[id=id_profiles_1]')
      .click('input[id=id_profiles_2]')
      .click('input[id=id_interests_1]')
      .click('input[id=id_interests_2]')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=signupcomplete]', 1000)
      .assert.urlContains('complete')
      .end();
  }
};
