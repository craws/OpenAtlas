/*
 * Translated default messages for the jQuery validation plugin.
 * Locale: ES (Spanish, Español)
 */
(function ($) {
    $.extend($.validator.messages, {
        required: "Este campo es un campo requerido",
        maxlength: $.validator.format("{0} caracteres máximos permitidos"),
        minlength: $.validator.format("Introduzca al menos {0} caracteres."),
        rangelength: $.validator.format("Introduzca al menos {0} y como máximo {1} caracteres."),
        email: "Por favor, introduce una dirección de correo electrónico válida.",
        url: "Por favor introduzca una URL válida.",
        date: "Por favor introduzca una fecha válida.",
        number: "Por favor, introduzca un número",
        digits: "Por favor, solo introduzca dígitos.",
        equalTo: "Por favor, repita el mismo valor.",
        fileSize: "Este archivo es demasiado grande, se permiten {0} MB",
        range: $.validator.format("Introduzca un valor entre {0} y {1}."),
        max: $.validator.format("Introduzca un valor inferior o igual a {0}."),
        min: $.validator.format("Introduzca un valor superior o igual a {0}."),
    });
}(jQuery));
