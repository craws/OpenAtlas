$(document).ready(function () {
    $("form").each(function() {
        $(this).validate({errorClass: 'error'});
    });
});
