confs = {
    icon: '<i class="fa fa-smile-o"></i>',
    name: "Who Am I"
};
plugin = function(sdk) {
    sdk.html('Checking who I am...');
    sdk.refresh();

    var gp = GlobalProxy.getInstance();

    gp.getProfileInformation().then(function(response){
        var profile = response.profile;

        var me = 'I am '+profile.user.first_name+' '+profile.user.last_name+'.<br /> <br />\
        I belong to '+profile.organization+' and am interested in '+ profile.interests.reduce(function(prev, curr) {
          return prev + curr.name+',';
        }, '')+ '<br /><br />';

        if(profile.mails_news){
            me += 'I want to receive mailing newsletters weekly.';
        } else {
            me += "I don't want to receive newsletters weekly in my mail.";
        }

        me+= '<br />I like my paginations to have '+profile.paginator+' results.';

        sdk.html(me);

        sdk.refresh();
    }).catch(function(exc){
        sdk.html("Can't figure out who I am!");
        sdk.refresh();
    });

};
