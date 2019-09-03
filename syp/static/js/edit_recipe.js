$(document).ready(function() {
  // Delete Ingredient('...')
  $(".ul_pepper").children("li").each(function() {
    ingredient = $(this).find('input:visible:first');
    ing_val = ingredient.val();
    ingredient.val(ing_val.substring(12, ing_val.length - 2))
  });
});

/* ELSE IF was not working, don't know why. */
$(window).on('resize load', function(){
  var width = $(window).width()
  if (width < 450) {
    $('#textarea_h4').attr("rows", "6");
    $('#textarea_p').attr("rows", "40");
  }
  if (width >= 450) {
    $('#textarea_h4').attr("rows", "5");
    $('#textarea_p').attr("rows", "30");
  }
  if (width >= 580) {
    $('#textarea_h4').attr("rows", "3");
    $('#textarea_p').attr("rows", "24");
  }
  if (width >= 1280) {
    $('#textarea_h4').attr("rows", "2");
    $('#textarea_p').attr("rows", "14");
  }
});


function add_ingredient() {
  var idx = $('#ingredients_list li').length;
  var new_ing = $('.ingredient_item').first().clone();
  // Change values
  new_ing.find('input').each(function() {
    $(this).val('');
  });
  new_ing.find('select').first().val('0');
  // Change IDS and names
  new_ing.find('input, select').each(function() {
    var old_id = $(this).attr("id");
    var new_id = old_id.replace(
      /(ingredients-)(\d+)(-[a-zA-Z]+)/,
      "$1" + idx + "$3"
    );
    $(this).attr("id", new_id);
    $(this).attr("name", new_id);
  });

  //Change for attribute of associated label
  new_ing.find('label').each(function() {
    var old_id = $(this).attr("for");
    var new_id = old_id.replace(
      /(ingredients-)(\d+)(-[a-zA-Z]+)/,
      "$1" + idx + "$3"
    );
    $(this).attr("for", new_id);
  });

  new_ing.attr("id", "ingredients-" + idx + "-ingredient")
  new_ing.attr("name", "ingredients-" + idx + "-ingredient")
  $('#ingredients_list').append(new_ing);
}

function remove_ingredient(link) {
  var n_items = $('#ingredients_list li').length;
  var item_id = $(link).siblings('select').attr('id');
  var item_nr = parseInt(item_id.match(/ingredients-(\d+)-[a-zA-Z]+/)[1]);
  if (item_nr < n_items - 1) { // This was not the last element
    for (idx = item_nr + 1; idx < n_items; idx++) {
      var item = $('#ingredients_list li').eq(idx);
      item.find('input, select').each(function() {
        var old_id = $(this).attr("id");
        var new_id = old_id.replace(
          /(ingredients-)(\d+)(-[a-zA-Z]+)/,
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


function add_subrecipe() {
    var new_sub = $('.subrecipe_item').first().clone();
    new_sub.find('input').first().val('');
    $('#subrecipes_list').append(new_sub);
}

function remove_subrecipe(link) {
  $(link).parent().remove();
}

// TODO: Every time an element is removed, the larger indices have to be reduced.
