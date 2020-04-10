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


function remove_item(link) {
    let item = link.parentElement;
    let list = item.parentElement.children;
    let item_nr = parseInt(item.children[0].id.match(/[a-zA-Z]+-(\d+)-[a-zA-Z]+/)[1]);
    if (item_nr < list.length - 1) { // Item is not last
        for (let i = item_nr + 1; i < list.length; i++) {
            for (let j = 0; j < list[i].children.length - 1; j++) { // Last child is anchor
                let new_id = list[i].children[j].id.replace(i, i-1);
                list[i].children[j].id = new_id;
                list[i].children[j].name = new_id;
            }
        }
    }
    item.remove();
}


function add_item() {
    let list = document.getElementById('social_media');
    let item_id = 'media-' + list.children.length;
    let select = document.getElementById('all_media').cloneNode(true);
    select.setAttribute('style', 'margin-bottom: 0.5em');
    select.setAttribute('id', item_id + '-web');
    select.setAttribute('name', item_id + '-web');
    let input = document.createElement('input');
    input.setAttribute('id', item_id + '-username');
    input.setAttribute('name', item_id + '-username');
    input.setAttribute('type', 'text');
    input.setAttribute('placeholder', 'Nombre de usuario');
    input.required = true;
    let anchor = document.createElement('a');
    anchor.setAttribute('onclick', 'remove_item(this)');
    anchor.innerHTML = 'Borrar cuenta';
    let item = document.createElement('li');
    item.setAttribute('style', 'margin-bottom: 2em');
    item.appendChild(select);
    item.appendChild(input);
    item.appendChild(anchor);
    list.appendChild(item);
}