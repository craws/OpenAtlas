
$(document).ready(function () {
    $.validator.setDefaults({
        ignore: [], // enable validation for hidden fields
    });
    $('#tabs').tabs();
    $('#show_passwords').show();
    $(".date-switch").addClass('display-none');
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
    });
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
    $.validator.addClassRules({
        year: {number: true, min: 1},
        month: {digits: true, max: 12},
        day: {digits: true, max: 31}
    });
    $("form").each(function () {
        $(this).validate();
    });
});
