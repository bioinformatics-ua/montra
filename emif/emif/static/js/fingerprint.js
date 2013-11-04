var getPlacement = function($el) {
    var offset = $el.offset(),
        top = offset.top,
        left = offset.left,
        height = $(document).outerHeight(),
        width = $(document).outerWidth(),
        vert = 0.5 * height - top,
        vertPlacement = vert > 0 ? 'bottom' : 'top',
        horiz = 0.5 * width - left,
        horizPlacement = horiz > 0 ? 'right' : 'left',
        placement = Math.abs(horiz) > Math.abs(vert) ?  horizPlacement : vertPlacement;
    return placement
};

function help_text_popover() {
    $('.qtext').each(function () {
        var $this = $(this);
        $this.popover({

            trigger: 'hover',
            placement: getPlacement($this),
            html: true,
            content: $this.find('.question-help-text').html()
//      content: 'body'
        });
    });
}


    <!-- Begin -- Check if user has unsaved changes -->
 var formHasChanged = false;
 var submitted = true;
$(document).ready(function () {
    window.onbeforeunload = function (e) {
        if (formHasChanged && !submitted) {
            var message = "You have unsaved changes!", e = e || window.event;
            if (e) {
                e.returnValue = message;
            }
            return message;
        }
    }
 $(document).on('change', '#qform input, #qform select, #qform textarea', function (e) {
    formHasChanged = true;
    submitted = false;
});

 $("#qform").submit(function() {
     submitted = true;
     formHasChanged = false;
     });
});
<!-- End -- Check if user has unsaved changes -->

