const variables = {}
/* Show and hide function for value type input fields. Has to be outside of $(document).ready() */
function switch_value_type(id, el) {
    if (el.hasAttribute('show')) {
        el.removeAttribute('show');
        $(`.value-type-field.sub-of-${id}`).each(function () {
            this.classList.add('d-none');
        });
        $(`.value-type-field.sub-of-${id} .value-type-switcher`).each(function () {
            this.removeAttribute('show');
        });
    } else {
        $(`.value-type-field.direct-sub-of-${id}`).each(function () {
            this.classList.remove('d-none');
        });
        el.setAttribute('show', '');
    }
}

$(document).ready(function () {

    /* Write selected DataTables checkboxes to hidden input */
    $('#checkbox-form').submit((a) => {
        ids = [];
        $('#checkbox-form .dataTable').DataTable().rows().nodes().to$().find('input[type="checkbox"]').each(
            function () {
                if ($(this).is(':checked')) {
                    ids.push($(this).attr('value'));
                }
            });
        $('#checkbox_values').val(ids.length > 0 ? '[' + ids + ']' : '');
    });

    /* Needed for ajax bookmark functionality */
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", bookmark_csrf_token);
            }
        }
    });

    /* Show and hide function for reference systems */
    $("#reference-system-switcher").click(function () {
        $(".reference-system-switch").toggleClass('display-none');
        $(this).text(function (i, text) {
            return $.trim(text) === show ? hide : show;
        })
    });
    $('.reference-system-switch').addClass('display-none');

    /* Show and hide function for date input fields */
    $("#date-switcher").click(function () {
        $(".date-switch").toggleClass('d-none');
        $(this).text(function (i, text) {
            return $.trim(text) === show ? hide : show;
        })
    });

    /* Hide date fields if there are any and if they are empty */
    if ($('#begin_year_from').length &&
        $('#begin_year_from').val() == '' && $('#end_year_from').val() == '') {
        $('.date-switch').addClass('d-none');
    }

    /* Hide value type fields with class* wildcard selector */
    $('[class*="value-type-switch"]').addClass('display-none');

    $('label[for="show_passwords"]').css('display', 'block');
    $('#show_passwords').show()

    .change(function () {
        $('#password')[0].type = this.checked ? 'text' : 'password';
        $('#password2')[0].type = this.checked ? 'text' : 'password';
        if (document.getElementById('password_old')) {
            $('#password_old')[0].type = this.checked ? 'text' : 'password';
        }
    });

    /* Below section sets up validation for various forms */
    // Enable validation for hidden fields
    let v = $.validator;
    v.setDefaults({
        ignore: [],
    });

    v.addClassRules({
        year: {number: true, min: -4713, max: 9999},
        month: {digits: true, min: 1, max: 12},
        day: {digits: true, min: 1, max: 31},
        hour: {digits: true, min: 0, max: 23},
        minute: {digits: true, min: 0, max: 59},
        second: {digits: true, min: 0, max: 59},
        integer: {digits: true},
        signed_integer: {signedInteger: true},
        email: {email: true},
        "value-type": {number: true}
    });

    v.addMethod('notEqual', function (value, element, param) {
        return this.optional(element) || value != $(param).val();
    }, 'This has to be different');

    v.addMethod('fileSize', function (value, element, param) {
        return this.optional(element) || element.files[0].size <= param;
    }, 'This file it too large, allowed are ' + maxFileSize + ' MB');

    v.addMethod("signedInteger", function (value, element) {
        return /^-?\d+$/i.test(value);
    }, 'Please enter a valid integer.');

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
            file: {fileSize: maxFileSize * 1024 * 1024}
        },
    });

    $("form").on('click', '#generate-password', function () {
        charset = '123456789abcdefghjklmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ';
        random_password = '';
        for (var i = 0; i < minimumPasswordLength; i++) {
            index = Math.floor(Math.random() * (charset.length));
            random_password += charset[index];
        }
        $("#password").val(random_password);
        $("#password2").val(random_password);
    })

    // Adding a generic submit handler to form validation
    .each(function () {
        $(this).validate({
            submitHandler: function (form) {
                if (this.submitButton.id === "insert_and_continue") $('#continue_').val('yes');
                if (this.submitButton.id === "insert_continue_sub") $('#continue_').val('sub');
                if (this.submitButton.id === "insert_continue_human_remains") $('#continue_').val('human_remains');
                $('input[type="submit"]').prop("disabled", true).val('... in progress');
                form.submit();
            },
        });
    });

    //add required to reference precision if reference is set
    $("[id^=reference_system_value]").on('change', function () {
        const select = $(`#reference_system_precision_${this.id.split('_').pop()}`);
        if (!this.value?.length)
            select.removeClass('required');
        else
            select.addClass('required');
    });

    $("div[id*='-modal']").on('shown.bs.modal', function () {
        $("input[id*='-tree-search']").focus();
        $("input[type='search']").focus();
    });

    $('.extend-icon').click((a) => {
        if(a.currentTarget.id === 'extend-form-icon') {
            $('#extend-form-icon').hide();
            $('#extend-map-icon').show();
            $('.col-xl-4').toggleClass("col-xl-4").toggleClass("col-xl-10");
            $('.col-xl-8').toggleClass("col-xl-8").toggleClass("col-xl-2");
            return;
        }
        $('#extend-form-icon').show();
        $('#extend-map-icon').hide();
        $('.col-xl-10').toggleClass("col-xl-10").toggleClass("col-xl-4");
        $('.col-xl-2').toggleClass("col-xl-2").toggleClass("col-xl-8");
    });

    $( ".modal" ).on('shown.bs.modal', function(){
        $(`#${this.id} input`)?.get(0)?.focus() 
    });

});
