
$(document).ready(function($) {
    var notification_ids = $.map( $('[name="notification_id"]'), function( n, i ) {
      return n.value;
    });
    $.post("/read_notifications", { notification_ids: notification_ids })
        .done(function( response ) {
            console.log(response);
        });
});