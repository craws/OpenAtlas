
$(document).ready(function () {
    $('#tabs').tabs();
    $('#show_passwords').show();
    $('label[for="show_passwords"]').css('display', 'block');
    $('#show_passwords').change(function() {
        $('#password')[0].type = this.checked ? 'text' : 'password';
        $('#password2')[0].type = this.checked ? 'text' : 'password';
        $('#password_old')[0].type = this.checked ? 'text' : 'password';
    });

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
