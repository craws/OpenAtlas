
tinymce.init({
    menubar: false,
    relative_urls : false,
    mode: "specific_textareas",
    editor_selector: "tinymce",
    resize: "both",
    toolbar_items_size : 'small',
    plugins: "link code textcolor colorpicker",
    toolbar: "bold italic underline strikethrough alignleft aligncenter alignright alignjustify undo redo link " +
        "unlink fontselect fontsizeselect forecolor code",
});

function resizeText(multiplier) {
    if (document.body.style.fontSize === "") {
        document.body.style.fontSize = "1.0em";
    }
    document.body.style.fontSize = parseFloat(document.body.style.fontSize) + (multiplier * 0.2) + "em";
}
