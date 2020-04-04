/*jshint esversion: 6 */

function repeat_password(field) {
    let repeat = field.cloneNode();
    repeat.placeholder = 'Escríbela de nuevo aquí';
    repeat.value = '';
    repeat.style.marginTop = '1em';
    repeat.setAttribute("onchange", "match_passwords(this)");
    field.setAttribute("onchange", "clear_repeat_password(this)");
    field.parentNode.appendChild(repeat);
    let span = document.createElement('span');
    span.innerHTML = 'Las contraseñas no son iguales';
    span.style.color = '#991D1D';
    field.parentNode.appendChild(span);
    document.getElementById('save_btn').disabled = true;
}

function clear_repeat_password(field) {
    field.nextElementSibling.value = '';
    let span = field.nextElementSibling.nextElementSibling;
    span.innerHTML = 'Las contraseñas no son iguales';
    span.style.color = '#991D1D';
    document.getElementById('save_btn').disabled = true;
}

function match_passwords(repeat) {
    let span = repeat.nextSibling;
    console.log(span.style.color);
    if (repeat.previousElementSibling.value == repeat.value) {
        span.innerHTML = 'Las contraseñas son iguales';
        span.style.color = '#599a00';
        document.getElementById('save_btn').disabled = false;
    } else if (span.style.color == 'rgb(89, 154, 0)') {
        span.innerHTML = 'Las contraseñas no son iguales';
        span.style.color = '#991D1D';
        document.getElementById('save_btn').disabled = true;
    }
}