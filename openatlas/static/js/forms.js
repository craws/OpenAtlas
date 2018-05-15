
$(document).ready(function () {
    $.validator.setDefaults({
        ignore: [], // enable validation for hidden fields
    });
    $.validator.addMethod('notEqual', function(value, element, param) {
        return this.optional(element) || value != $(param).val();
    }, 'This has to be different');
    $.validator.addMethod('fileSize', function (value, element, param) {
        return this.optional(element) || element.files[0].size <= param;
    }, 'This file it too large, allowed are ' + maxFileSize + ' MB');

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
            password: {minlength: minimumPasswordLength, notEqual: "#password_old"},
            password2: {equalTo: "#password"},
        }
    });
    $("#password-reset").validate({
        rules: {
            email: {email: true}
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
    $('#file-form').validate({
        rules: {
            file: {
                fileSize: maxFileSize  * 1024 * 1024,
            }
        },
    });
    $.validator.addClassRules({
        year: {number: true, min: -4713, max: 9999},
        month: {digits: true, min: 1, max: 12},
        day: {digits: true, min: 1, max: 31}
    });
    $("form").each(function () {
        $(this).validate();
    });
});
