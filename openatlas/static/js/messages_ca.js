/*
 * Translated default messages for the jQuery validation plugin.
 * Locale: CA (Catalan, Català)
 */
(function ($) {
    $.extend($.validator.messages, {
        required: "Aquest camp és obligatori",
        maxlength: $.validator.format("{0} caràcters máxims permesos"),
        minlength: $.validator.format("Introdueixi {0} caràcters almenys."),
        rangelength: $.validator.format("Introdueixi almenys {0} y com a màxim {1} caràcters."),
        email: "Si us plau, introdueixi una adreça de correu electrónic vàlida.",
        url: "Si us plau introdueixi una URL vàlida.",
        date: "Si us plau introdueixi una data vàlida.",
        number: "Si us plau, introdueixi un número",
        digits: "Si us plau, només introdueixi dígits.",
        equalTo: "Si us plau, repeteixi el mateix valor.",
        fileSize: "Aquest fitxer és massa gran, el màxim permès és de {0} MB",
        range: $.validator.format("Introdueixi un valor entre {0} y {1}."),
        max: $.validator.format("Introdueixi un valor inferior o igual a {0}."),
        min: $.validator.format("Introdueixi un valor superior o igual a {0}."),
    });
}(jQuery));
