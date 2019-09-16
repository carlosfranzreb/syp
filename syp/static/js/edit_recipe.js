// "Añadir subreceta" no cambia a "Subrecetas incluidas" cuando debe.
// datalist subrecipes not working

$(document).ready(function() {
  $(".ul_pepper").children("li").each(function() {
    ingredient = $(this).find('input:visible:first');
    ing_val = ingredient.val();
    ingredient.val(ing_val.substring(12, ing_val.length - 2));
  });
  // Remove set subrecipes from options
  $('#subrecipes li input').each(function() {
    $("#all_subrecipes option[value='" + $(this).val() + "']").remove();
  });
  update_subrecipe_options();
});

/* ELSE IF was not working, don't know why. */
$(window).on('resize load', function(){
  var width = $(window).width();
  if (width < 450) {
    $('#textarea_h4').attr("rows", "6");
    $('#textarea_p').attr("rows", "40");
    $('.recipe_step').attr("rows", "15");
  }
  if (width >= 450) {
    $('#textarea_h4').attr("rows", "5");
    $('#textarea_p').attr("rows", "30");
    $('.recipe_step').attr("rows", "10");
  }
  if (width >= 580) {
    $('#textarea_h4').attr("rows", "3");
    $('#textarea_p').attr("rows", "24");
    $('.recipe_step').attr("rows", "8");
  }
  if (width >= 1280) {
    $('#textarea_h4').attr("rows", "2");
    $('#textarea_p').attr("rows", "14");
    $('.recipe_step').attr("rows", "5");

  }
});


function add_item(link) {
  var list = '';
  var div = $(link).parent().attr('id');
  if (div == 'steps') {
    list = $(link).siblings('ol');
  }
  else {
    list = $(link).siblings('ul');
  }
  var items = list.children('li');
  var n_items = items.length;
  var first_item = items.first();
  if (n_items == 1 && first_item.css('display') == 'none') {
    first_item.css('display', 'block');
  }
  else {
    if (div == 'subrecipes') {
      var new_item = $('#blueprint_subrecipes').children(0).clone();
    }
    else {
      var new_item = first_item.clone();
    }
    // Change values
    new_item.find('input, textarea').each(function() {
      $(this).val('');
    });
    new_item.find('select').first().val('0');
    // Change IDS and names
    new_item.find('input, select, textarea').each(function() {
      var old_id = $(this).attr("id");
      var new_id = old_id.replace(
        /([a-zA-Z]+-)(\d+)(-[a-zA-Z]+)/,
        "$1" + n_items + "$3"
      );
      $(this).attr("id", new_id);
      $(this).attr("name", new_id);
    });

    //Change for attribute of associated label
    new_item.find('label').each(function() {
      var old_id = $(this).attr("for");
      var new_id = old_id.replace(
        /([a-zA-Z]+-)(\d+)(-[a-zA-Z]+)/,
        "$1" + n_items + "$3"
      );
      $(this).attr("for", new_id);
    });

    list.append(new_item);
  }
}

function remove_item(link) {
  var items = '';
  if ($(link).closest('article').attr('id') == 'steps') {
    items = $(link).closest('ol').children('li');
  }
  else {
    items = $(link).closest('ul').children('li');
  }
  var n_items = items.length;
  if (n_items == 1) {
    i = items.first();
    i.find('input, textarea').each(function() {
      $(this).val('');
    });
    i.find('select').first().val('0');
    i.css('display', 'none');
  }
  else {
    var item_id = $(link).siblings('input, textarea').attr('id');
    var item_nr = parseInt(item_id.match(/[a-zA-Z]+-(\d+)-[a-zA-Z]+/)[1]);
    var item = '';
    if (item_nr < n_items - 1) {
      for (idx = item_nr + 1; idx < n_items; idx++) {
        item = items.eq(idx);
        item.find('input, select, textarea').each(function() {
          var old_id = $(this).attr("id");
          var new_id = old_id.replace(
            /([a-zA-Z]+-)(\d+)(-[a-zA-Z]+)/,
            "$1" + (idx-1).toString() + "$3"
          );
          $(this).attr("id", new_id);
          $(this).attr("name", new_id);
        });

        //Change for attribute of associated label
        item.find('label').each(function() {
          var old_id = $(this).attr("for");
          var new_id = old_id.replace(
            /(ingredients-)(\d+)(-[a-zA-Z]+)/,
            "$1" + (idx-1).toString() + "$3"
          );
          $(this).attr("for", new_id);
        });
      }
    }
    $(link).parent().remove();
  }
}


function add_subrecipe_steps() {
    $('#choose_subrecipe').css('display', 'block');
}

function set_subrecipe_step() {
  // Subrecipe is added to the steps and removed from the options
  var select = $('#choose_subrecipe');
  add_item(select.siblings('a:contains(paso)'));
  select.css('display', 'none');
  var selected_option = select.find('option:selected');

  var added_item = $('#steps ol li').last();
  added_item.find('textarea')
    .val(selected_option.text())
    .attr('readonly', true)
    .addClass('is_subrecipe');
  added_item.children('a').attr(
    'onclick',
    'remove_item(this); update_subrecipe_options()'
  );
  selected_option.remove();
  select.val(select.children('option').first().val());
  update_subrecipe_anchor();
}


function remove_subrecipe(link) {
  var subrecipe = $(link).siblings('input').val();
  var is_removable = true;
  $('#steps ol li textarea').filter('.is_subrecipe').each(function() {
    if ($(this).val() == subrecipe) {
      is_removable = false;
      alert('No se puede borrar ' + subrecipe +
        ', porque está en los pasos de la receta.');
    }
  });
  if (is_removable == true) {
    $('#all_subrecipes').append(new Option(subrecipe));
    // Remove subrecipe from step options
    // $("#choose_subrecipe option[value='" + subrecipe + "']").remove();
    $("#choose_subrecipe option").each(function() {
      if ($(this).val() == subrecipe) {
        $(this).remove();
      }
    });
    update_subrecipe_anchor();
    remove_item(link);
  }
}


function add_subrecipe_to_step_options(link) {
  var subrecipe = $(link).siblings('textarea').val();
  var select = $("#choose_subrecipe");
  select.append(new Option(subrecipe));
  select.val(select.children('option').first().val());
  update_subrecipe_anchor();
}


function update_subrecipe_options() {
  // Update subrecipe options for the subrecipes
  var caca = $('#subrecipes_list li');
  $("#all_subrecipes option[value='" + caca + "']").remove();

  // Update subrecipe options for the steps
  var select = $('#choose_subrecipe');
  var all_subrecipes = [];
  $('#subrecipes ul li').each(function() {
    all_subrecipes.push($(this).find('input').val());
  });
  var used_subrecipes = [];
  $('#steps ol li textarea').filter('.is_subrecipe').each(function() {
    used_subrecipes.push($(this).val());
  });
  var subrecipes = all_subrecipes.filter(x => !used_subrecipes.includes(x));
  select.children('option:not(:first)').remove();
  for (idx = 0; idx < subrecipes.length; idx++) {
    select.append(new Option(subrecipes[idx]));
  }
  select.val(select.children('option').first().val());
  update_subrecipe_anchor();
}


function update_subrecipe_anchor() {
  var select = $('#choose_subrecipe');
  select.css('display', 'none');
  var link = $('#anchor_add_subrecipe');
  var options = select.children('option');
  if (options.length == 1 && link.text() == "Añadir subreceta") {
    link.text('Subrecetas incluidas')
        .css('color', '#599A00')
        .attr('onclick', '');
  }
  else if (options.length > 1 && link.text() == "Subrecetas incluidas") {
    link.text('Añadir subreceta')
        .css('color', '#F56A6A')
        .attr('onclick', 'add_subrecipe_steps()');
  }
}
