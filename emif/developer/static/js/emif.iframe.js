$(function(){

    var resize = function(self) {
         self.css('height', $(document).height()-200);
    };
    resize($('#tframe'));
    $( window ).resize(function() {
      resize($('#tframe'));
    });

});
