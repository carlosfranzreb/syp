/*jshint esversion: 6 */


$(document).ready(function() {
    // On first load, remove Ingredient(...) from name
    // The check is necessary because it shouldn't be cut when the form is validated
    var ingredients = $(".ul_pepper").children("li");
    if (
        ingredients
            .first()
            .find("input:visible:first")
            .val()
            .includes("Ingredient(")
    ) {
        ingredients.each(function() {
            ingredient = $(this).find("input:visible:first");
            ing_val = ingredient.val();
            ingredient.val(ing_val.substring(12, ing_val.length - 2));
        });
    }
    // Disable submit on enter
    $(window).keydown(function(event) {
        if (event.keyCode == 13) {
            event.preventDefault();
            return false;
        }
    });
    // Adjust step height
    let elements = document.querySelectorAll('textarea');
    elements.forEach(elem => auto_grow(elem));
    // Add 'Receta: ' before subrecipes. CSS ::before not working.
    $("#steps")
        .find("textarea")
        .each(function() {
            if ($(this).hasClass("is_subrecipe")) {
                $(this).text("Receta: " + $(this).text());
            }
        });
});


function add_ingredient() {
    let ingredient_list = document.getElementById('ingredients_list');
    let ings_length = ingredient_list.getElementsByTagName('li').length;
    let item_id = 'ingredients-' + ings_length;  // last field missing
    let ing_label = document.createElement('label');
    ing_label.setAttribute('for', item_id + '-ingredient');
    ing_label.innerHTML = 'Ingrediente:';
    let ing_field = document.createElement('span');
    ing_field.innerHTML = `<input 
        autocomplete="off" 
        id="` + item_id + `-ingredient" 
        list="all_ingredients" 
        name="` + item_id + `-ingredient" 
        type="text" 
        required
    >`;
    let amount_label = document.createElement('label');
    amount_label.setAttribute('for', item_id + '-amount');
    amount_label.innerHTML = 'Cantidad:';
    let amount_field = document.createElement('input');
    amount_field.setAttribute('id', item_id + '-amount');
    amount_field.setAttribute('name', item_id + '-amount');
    amount_field.setAttribute('type', 'text');
    amount_field.required = true;
    let unit_label = document.createElement('label');
    unit_label.setAttribute('for', item_id + '-unit');
    unit_label.innerHTML = 'Unidad:';
    let unit_field = document.getElementById('all_units').cloneNode(true);
    unit_field.setAttribute('id', item_id + '-unit');
    unit_field.setAttribute('name', item_id + '-unit');
    unit_field.setAttribute('style', '');
    let anchor = document.createElement('a');
    anchor.setAttribute('onclick', 'remove_item(this)');
    anchor.innerHTML = 'Borrar ingrediente';
    let item = document.createElement('li');
    item.className = 'ingredient_item';
    item.appendChild(ing_label);
    item.appendChild(ing_field);
    item.appendChild(amount_label);
    item.appendChild(amount_field);
    item.appendChild(unit_label);
    item.appendChild(unit_field);
    item.appendChild(anchor);
    ingredient_list.append(item);
}


function add_step() {
    let step_list = document.getElementById('steps').children[1];
    let steps_length = step_list.getElementsByTagName('li').length;
    let textarea = document.createElement('textarea');
    textarea.setAttribute('class', 'recipe_step');
    textarea.setAttribute('oninput', 'auto_grow(this)');
    textarea.setAttribute('id', 'steps-' + steps_length + '-step');
    textarea.setAttribute('name', 'steps-' + steps_length + '-step');
    let anchor = document.createElement('a');
    anchor.setAttribute('onclick', 'remove_item(this)');
    anchor.innerHTML = 'Borrar paso';
    let item = document.createElement('li');
    item.setAttribute('class', 'step_item');
    item.appendChild(textarea);
    item.appendChild(anchor);
    step_list.append(item);
    return item;
}


function remove_item(link) {
    let items = "";
    let section = $(link)
        .closest("article")
        .attr("id");
    if (section == "steps") {
        items = $(link)
            .closest("ol")
            .children("li");
    } else {
        items = $(link)
            .closest("ul")
            .children("li");
    }
    let item_id = $(link)
        .siblings("input, textarea")
        .attr("id");
    let item_nr = parseInt(item_id.match(/[a-zA-Z]+-(\d+)-[a-zA-Z]+/)[1]);
    let item = "";
    if (item_nr < items.length - 1) {
        for (idx = item_nr + 1; idx < items.length; idx++) {
            item = items.eq(idx);
            item.find("input, select, textarea").each(function() {
                let old_id = $(this).attr("id");
                let new_id = old_id.replace(idx, idx-1);
                $(this).attr("id", new_id);
                $(this).attr("name", new_id);
            });

            //Change for attribute of associated label
            item.find("label").each(function() {
                let old_id = $(this).attr("for");
                let new_id = old_id.replace(idx, idx-1);
                $(this).attr("for", new_id);
            });
        }
    }
    $(link).parent().remove();
}


function toggle_subrecipe_input() {
    $("#choose_subrecipe").toggle();
    $("#subrecipe_button").toggle();
    $("#anchor_add_step").toggle();
    let anchor = $("#anchor_add_subrecipe");
    anchor.text(anchor.text() == "Cancelar" ? "Añadir subreceta" : "Cancelar");
}


function add_subrecipe() {
    let input = $("#choose_subrecipe");
    let subrecipe = input.val();
    let obj = $("#all_subrecipes").find("option[value='" + subrecipe + "']");
    if (obj != null && obj.length > 0) {
        let added_item = add_step();
        input.val(""); // Remove input.
        toggle_subrecipe_input();
        let textarea = added_item.firstChild;
        textarea.innerHTML = "Receta: " + subrecipe;
        textarea.setAttribute("readonly", true);
        textarea.className += " is_subrecipe";
    } else {  // don't allow submission
        alert("La subreceta que has escrito no existe. Elige una de la lista.");
    }
}


function update_video() {
    $(".video-container")
        .find("iframe")
        .attr("src", $("#link_video").val());
}

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";    
}

function check_size(field) {
    if (field.files[0].size > 19456) {  // 19MB
        window.alert('¡La imagen no puede pesar más de 19 MB!');
        field.value = '';
    }
}