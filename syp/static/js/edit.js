/*jshint esversion: 6 */

$(document).ready(function() {
    // Adjust textarea heights to their contents
    let elements = document.querySelectorAll('textarea');
    elements.forEach(elem => auto_grow(elem));
    // Disable submit on enter
    $('form input').keydown(function (e) {
        if (e.keyCode == 13) {
            var inputs = $(this).parents("form").eq(0).find(":input");
            if (inputs[inputs.index(this) + 1] != null) {                    
                inputs[inputs.index(this) + 1].focus();
            }
            e.preventDefault();
            return false;
        }
    });
});

/** Adapt field height to content. */
function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";    
}

/** Check file size doesn't exceed 19MB, as 20MB is the server limit. */
function check_size(field) {
    if (field.files[0].size > 19000000) {  // 19MB
        window.alert('¡La imagen no puede pesar más de 19 MB!');
        field.value = '';
    }
}