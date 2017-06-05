$(document).ready(function () {
    $("#tabs").tabs();
    $("form").each(function() {
        $(this).validate({errorClass: 'error'});
    });
});
