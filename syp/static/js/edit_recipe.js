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


function add_item(link) {
  var list = $(link).siblings('ul');
  var items = list.children('li');
  var n_items = items.length;
  var first_item = items.first();
  if (n_items == 1 && first_item.css('display') == 'none') {
    first_item.css('display', 'block');
  }
  else {
    var new_ing = first_item.clone();
    // Change values
    new_ing.find('input').each(function() {
      $(this).val('');
    });
    new_ing.find('select').first().val('0');
    // Change IDS and names
    new_ing.find('input, select').each(function() {
      var old_id = $(this).attr("id");
      var new_id = old_id.replace(
        /([a-zA-Z]+-)(\d+)(-[a-zA-Z]+)/,
        "$1" + n_items + "$3"
      );
      $(this).attr("id", new_id);
      $(this).attr("name", new_id);
    });

    //Change for attribute of associated label
    new_ing.find('label').each(function() {
      var old_id = $(this).attr("for");
      var new_id = old_id.replace(
        /([a-zA-Z]+-)(\d+)(-[a-zA-Z]+)/,
        "$1" + n_items + "$3"
      );
      $(this).attr("for", new_id);
    });

    list.append(new_ing);
  }
}

function remove_item(link) {
  var items = $(link).closest('ul').children('li');
  var n_items = items.length;
  if (n_items == 1) {
    i = items.first();
    i.find('input').each(function() {
      $(this).val('');
    });
    i.find('select').first().val('0');
    i.css('display', 'none');
  }
  else {
    var item_id = $(link).siblings('input').attr('id');
    var item_nr = parseInt(item_id.match(/[a-zA-Z]+-(\d+)-[a-zA-Z]+/)[1]);
    var item = '';
    if (item_nr < n_items - 1) {
      for (idx = item_nr + 1; idx < n_items; idx++) {
        item = items.eq(idx);
        item.find('input, select').each(function() {
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
