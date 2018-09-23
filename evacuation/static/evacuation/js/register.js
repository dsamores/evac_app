
$(document).ready(function($) {
    $('form').submit(function() {
        var email = $.trim($('#email').val());

        if (!/@unimelb.edu.au\s*$/.test(email) && !/@student.unimelb.edu.au\s*$/.test(email)) {
           $('#email').addClass('is-invalid');
           alert("Please check the form errors");
           return false;
        }
        return true;
    });
});