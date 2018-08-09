
$(document).ready(function($) {
    $('form').submit(function() {
        var email = $.trim($('#email').val());

        if (!/@unimelb.edu.au\s*$/.test(email) && !/@student.unimelb.edu.au\s*$/.test(email)) {
           $('#email-error').text('Please enter a @unimelb.edu.au or @student.unimelb.edu.au email');
           $('#email').addClass('is-invalid');
           return false;
        }
        return true;
    });
});