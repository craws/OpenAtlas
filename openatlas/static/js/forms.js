
$(document).ready(function () {
    $('#tabs').tabs();
    $('#insert_and_continue').click(function() {
        $('#continue_').val('yes');
        $('form').submit();
        return false;
    })

    $("#password-form").validate({
        rules: {
            password: {minlength: minimumPasswordLength},
            password2: {equalTo: "#password"}
        }
    });
    $("#profile-form").validate({
        rules: {
            email: {email: true}
        }
    });
    $('#user-form').validate({
        rules: {
            password: {minlength: minimumPasswordLength},
            password2: {equalTo: '#password'},
            email: {email: true}
        }
    });

    $("form").each(function () {
        $(this).validate();
    });
});
