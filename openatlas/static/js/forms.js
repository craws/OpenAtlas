$(document).ready(function () {
    $("#tabs").tabs();
    $("form").each(function() {
        $(this).validate({errorClass: 'error'});
    });
    $("#insert_and_continue").click(function() {
        $('#continue_').val('yes');
        $('form').submit();
        return false;
    })
});
