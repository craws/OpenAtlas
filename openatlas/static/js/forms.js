
$(document).ready(function () {
    $.validator.setDefaults({
        ignore: [], // Enable validation for hidden fields
    });

    $.validator.addMethod('notEqual', function(value, element, param) {
        return this.optional(element) || value != $(param).val();
    }, 'This has to be different');

    $.validator.addMethod('fileSize', function (value, element, param) {
        return this.optional(element) || element.files[0].size <= param;
    }, 'This file it too large, allowed are ' + maxFileSize + ' MB');

    $.validator.addMethod("signedInteger", function(value, element) {
        return /^-?\d+$/i.test(value);
    }, 'Please enter a valid integer.');

    $('#show_passwords').show();

    // Hide date fields if there are any and if they are empty
    if ($('#begin_year_from').length &
        $('#begin_year_from').val() == '' & $('#end_year_from').val() == '') {
        $('.date-switch').addClass('display-none');
    }

    $('.value-type-switch').addClass('display-none');
    $('label[for="show_passwords"]').css('display', 'block');
    $('#show_passwords').change(function() {
        $('#password')[0].type = this.checked ? 'text' : 'password';
        $('#password2')[0].type = this.checked ? 'text' : 'password';
        if (document.getElementById('password_old')) {
            $('#password_old')[0].type = this.checked ? 'text' : 'password';
        }
    });

    $("form").on('click', '#generate-password', function() {
        charset = '123456789abcdefghjklmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ';
        random_password = '';
        for (var i=0; i< minimumPasswordLength; i++) {
            index = Math.floor(Math.random() * (charset.length));
            random_password += charset[index];
        }
        $("#password").val(random_password);
        $("#password2").val(random_password);
    })

    $('#insert_and_continue').click(function() {
        $('#continue_').val('yes');
        $('form').submit();
    });

    $("#password-form").validate({
        rules: {
            password: {minlength: minimumPasswordLength, notEqual: "#password_old"},
            password2: {equalTo: "#password"},
        }
    });

    $('#user-form').validate({
        rules: {
            password: {minlength: minimumPasswordLength},
            password2: {equalTo: '#password'}
        }
    });

    $('#file-form').validate({
        rules: {
            file: {fileSize: maxFileSize  * 1024 * 1024}
        }
    });

    $.validator.addClassRules({
        year: {number: true, min: -4713, max: 9999},
        month: {digits: true, min: 1, max: 12},
        day: {digits: true, min: 1, max: 31},
        integer: {digits: true},
        signed_integer: {signedInteger: true},
        email: {email: true},
        "value-type": {number: true}
    });

    $("form").each(function () {
        $(this).validate();
    });
});
