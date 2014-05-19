
$('#modal-from-dom').bind('show', function() {
    var id = $(this).data('id'),
        removeBtn = $(this).find('.btn-danger'),
        href = removeBtn.attr('href');
    console.log('id' + id);

    removeBtn.attr('href', href.replace('ref', '' + id));
});


$('.confirm-delete').click(function(e) {
    e.preventDefault();

    var id = $(this).data('id');
    var name = $(this).data('name');
    $('#db-name').html(name);
    $('#modal-from-dom').data('id', id).modal('show');
});

/* WHAT IN THE HELL, THIS DOESNT BELONG HERE THIS IS FROM SHARE WIDGET


$('#modal-from-dom-share').bind('show', function() {
    var id = $(this).data('id'),
        removeBtn = $(this).find('.sharedb2'),
        href = removeBtn.attr('href');

    removeBtn.attr('href', href.replace('ref', '' + id));
});

$(".sharedb" ).click(function(e)
{
  e.preventDefault();
  var id = $(this).data('id');
  $('#modal-from-dom-share').data('id', id).modal('show');

});
$(".sharedb2" ).click(function(e)
{
  e.preventDefault();
  post_to_url($(this).attr('href'), {"email": $("#share_email").val(), "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').prop('value')});

});

*/